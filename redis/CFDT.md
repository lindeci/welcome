跨DC（数据中心）的数据同步是企业提升容灾实力的必备手段。

对于业务应用来讲，大量的业务逻辑是有状态的，仅仅做到服务的灵活拓展还不够，需要数据也拥有多站点共享的能力。

携程在2018年已经可以实现 Redis 单向跨区域同步，从上海将数据复制到美国加州，德国法兰克福，以及新加坡等众多海外站点，延迟稳定在 180ms左右，支持单个Redis 5MB/s 的传输带宽。

业务上有新的需求：能否在每个站点都可以独立地写入和读取，所有数据中心之间互相同步，而跨区域复制的一致性等问题，也可以由底层存储来解决？


## **二、技术选型**

所以，我们需要的是一个分布式的Redis存储，能够实现跨区域多向同步。面对大型分布式系统，不免要讨论CAP理论，在跨区域多活的场景下如何取舍？

显然P（网络分区）是首要考虑因素。其次，跨区域部署就是为了提高可用性，而且对于常见的一致性协议，不管是2PC、Paxos还是raft，在此场景下都要做跨区域同步更新，不仅会降低用户体验，在网络分区的时候还会影响可用性。

对于Redis这种毫秒级相应的数据库，应用希望能够在每个站点都可以“如丝般顺滑”地使用，因此C必定被排在最后。

那是不是C无法被满足了呢？事实并非如此，退而求其次，最终一致也是一种选择。经过调研，我们决定选用“强最终一致性”的理论模型来满足一致性的需求。[2]

关于“最终一致性”(Eventually Consistency) 和“强最终一致性”(Strong Eventually Consistency)，大家可以参考 wiki 百科给出的释义：

> (Strong
> Eventually Consistency) Whereas eventual consistency is only a liveness
> guarantee (updates will be observed eventually), strong eventual
> consistency (SEC) adds the safety guarantee that any two nodes that have
> received the same (unordered) set of updates will be in the same state.
> If, furthermore, the system is monotonic, the application will never
> suffer rollbacks.
>


## **三、问题**

有了目标，自然是开始计划和设计，那么在开始之前有什么问题呢？

### **3.1 跨数据中心双向同步共同的问题**

各种数据库在设计双向数据同步时，均会遇到的问题：

1）复制回源：A -> B -> A

数据从 A 复制到 B，B 收到数据后，再回源复制给 A 的问题。

2）环形复制：A -> B -> C -> A

我们可以通过标记来解决上一问题，然而系统引入更多节点之后，A 发送到 B 的数据，可能通过 C 再次回到 A。

3）数据一致性

网络传输具有延迟性和不稳定性，多节点的并发写入会造成数据不一致的问题。

4）同步时延（鉴于是跨国的数据同步，这一项我们先忽略）

### **3.2 Redis 的问题**

1）Redis 原生的复制模型，是不能够支持Multi-Master的理论架构的。

开源版的 Redis 只能支持 Master-Slave 的架构，并不能支持 Redis 之间互相同步数据。

2）Redis 特殊的同步方式（全量同步+增量同步），给数据一致性带来了更多挑战。

Redis 全量同步和增量同步都基于 replicationId + offset 的方式来做，在引入多个节点互相同步之后，如何对齐互相之间全量同步和增量同步的 offset 是一个巨大的问题。

3）同时支持原生的 Master-Slave 系统

在新版系统上，同时兼容现存的 Master-Slave 架构，两种同步方式和策略的异同，也带来了新的挑战。


## **四、解决方案**

由于篇幅的限制，这里只对数据一致性的解决方案做下介绍，对于分布式系统或者是双向同步感兴趣的同学，可以关注我们后续的技术文章和技术大会。

## **4.1 一致性的解决方案**

CRDT（Conflict-Free Replicated Data Type）[3] 是各种基础数据结构最终一致算法的理论总结，能根据一定的规则自动合并，解决冲突，达到强最终一致的效果。

2012年CAP理论提出者Eric

Brewer撰文回顾CAP[4]时也提到，C和A并不是完全互斥，建议大家使用CRDT来保障一致性。自从被大神打了广告，各种分布式系统和应用均开始尝试CRDT，redislabs[5]和riak[6]已经实现多种数据结构，微软的CosmosDB[7]也在azure上使用CRDT作为多活一致性的解决方案。

携程的框架部门最终也选择站在巨人的肩膀上，通过 CRDT 这种数据结构，来实现自己的Redis跨区域多向同步。

## **4.2 CRDT**

CRDT 同步方式有两种：

1）state-based replication

发送端将自身的“全量状态”发送给接收端，接收端执行“
merge” 操作，来达到和发送端状态一致的结果。state-base replication
适用于不稳定的网络系统，通常会有多次重传。要求数据结构能够支持
associative（结合律）/commutative（交换律）/idempotent（幂等性）。

2）operation-based replication

发送端将状态的改变转换为“操作”发送给接收端，接收端执行“update”操作，来达到和发送端状态一直的结果。op-based
replication 只要求数据结构满足 commutative 的特性，不要求
idempotent（大家可以想一想为什么）。op-based replication 在接收到 client
端的请求时，通常分为两步进行操作：

a. prepare 阶段：将 client 端操作转译为CRDT的操作；

b. effect 阶段：将转译后的操作 broadcast 到其他 server；

两者之间在实现上，界限比较模糊。一方面，state-based
replication可以通过发送 delta 减少网络流量，从而做到和 op-based replication
比较接近的效果；另一方面，op-based replication 可以通过发送 compact op-logs
将操作全集发送过去，来解决初始化的时候同步问题，从而达到类似于 state-based replication 的效果。

我们的系统需要借助两种同步方式，以适用于不同的场景中：

1) state-based replication 通常是基于“全量状态”进行同步，这样的结果是造成的网络流量太大，且同步的效率低下。在同步机制已经建立的系统中，我们更倾向于使用 op-based replication，以达到节省流量和快速同步的目的。
2) op-based replication 是基于 unbounded resource 的假设上进行论证的学术理念，在实践过程中，不可能有无限大的存储资源，将某个站点的全部数据缓存下来。

这样就带来一个问题，如果新加节点或者网络断开过久时，我们的存储资源不足以缓存所有值钱的操作，从而使得复制操作无法进行。此时，我们需要借助 state-based replication 进行多个站点之间，状态的merge操作。

### **4.3 CRDT 的数据结构**

Redis 的 String 类型对应的操作有 SET, DEL, APPEND, INCRBY 等等，这里我们只讲一下SET操作（INCRBY 会是不同的数据类型）。

### **Register**

先来讲一下，CRDT理论中如何处理Redis String 类型的同步问题。

Redis的String类型对应于CRDT里面的Register数据结构，对应的具体实现有两种比较符合我们的应用场景：

* MV(Multi-Value) Register：数据保留多份副本，客户端执行GET操作时，根据一定的规则返回值，这种类型比较适合INCRBY 的整型数操作。
* LWW(Last-Write-Wins) Register：数据只保留一份副本，以时间戳最大的那组数据为准，SET操作中，我们使用这种类型。

还记得上文提到的两种不同的同步方式么，关于两种不同的同步方式，对于LWW Register，实现方式会稍有不同。

### **Op-based LWW Register [8]**

![](https://pic2.zhimg.com/80/v2-2d69cbb57200d8835e620cc675463101_720w.webp)

### **State-based LWW Register [8]**

![](https://pic3.zhimg.com/80/v2-2469d98b62cd358f98be7864eb4419da_720w.webp)

![](https://pic2.zhimg.com/80/v2-fbcc7699fb76f284f67af4221961bb8d_720w.webp)

## **4.4 CRDT Register 在 Redis 中的落地**

讲完了 CRDT 的传输类型和一个基本的数据结构，那么具体这样的理论是如何落地到 Redis 中间的呢？

在最终的实现中，我们采用了OR-Set(Observed-Remove Set) + LWW(Last-Write-Wins) Register 来实现 Redis 中的 String 操作。

### **4.4.1 Redis K/V**

以下是理论上的数据结构，并不是 redis 中真正的结构体，仅仅作为说明使用。

```text
struct CRDT.Register { 
      string key; 
      string val; 
      TAG delete-tag; 
      int timestamp; 
}
```

1）key 既是SET操作中的 key

2）val 用来存储相应的 value

3）delete-tag 是逻辑删除的标记位，具体的理论来源是 [OR(Observed-Remove) Set](https://link.zhihu.com/?target=https%3A//www.youtube.com/watch%3Fv%3DPmJEMCBCv7k)

4）timestamp 用于LWW(Last Write Wins)机制，来解决并发冲突

由于目前我们的多写 Redis 还没有开源，这里我们拿 Java 程序举个栗子[9] [详细可以访问 github](https://link.zhihu.com/?target=https%3A//github.com/netopyr/wurmloch-crdt)。

LWW Register

processCommand 是这个 CRDT 框架的核心函数，基本定义了每一种类型，是如何进行 merge/update 等操作的。

在这里我们可以看到，每一个 command 过来时，会携带一个自身的时钟，由本地的程序进行判定，如果时钟符合偏序(partial ordered)，就进行 merge 操作，并储存元素。

```text
java
public class LWWRegister extends 
AbstractCrdt<LWWRegister, LWWRegister.SetCommand> {

private T value;
private StrictVectorClock clock;

public LWWRegister(String nodeId, String crdtId) {
    super(nodeId, crdtId, BehaviorProcessor.create());
    this.clock = new StrictVectorClock(nodeId);
}


protected Option<SetCommand<T>> processCommand(SetCommand<T> command) {
    if (clock.compareTo(command.getClock()) < 0) {
        clock = clock.merge(command.getClock());
        doSet(command.getValue());
        return Option.of(command);
    }
    return Option.none();
}


public T get() {
    return value;
}

public void set(T newValue) {
    if (! Objects.equals(value, newValue)) {
        doSet(newValue);
        commands.onNext(new SetCommand<>(
                crdtId,
                value,
                clock
        ));
    }
}

private void doSet(T value) {
    this.value = value;
    clock = clock.increment();
}

} 
```

OR-SET

而
Observed-Remove SET 相较 LWW-Register
就复杂一些，主要涉及两个概念，一个是正常的原生储存的地方，在Set<Element`<E>`>
elements中。而另一个重要的概念，是
tombstone（墓地），用来存放会删除的元素Set<Element`<E>`> tombstone OR-SET 的
tombstone，就可以解决并发删除的问题，而 LWW-Register 则可以解决并发添加的问题。

```text
java ublic class ORSet extends AbstractSet implements 
Crdt<ORSet, ORSet.ORSetCommand> /*, ObservableSet */ 
{private final String crdtId;
private final Set<Element<E>> elements = new HashSet<>();
private final Set<Element<E>> tombstone = new HashSet<>();
private final Processor<ORSetCommand<E>, ORSetCommand<E>> commands = ReplayProcessor.create();

public ORSet(String crdtId) {
    this.crdtId = Objects.requireNonNull(crdtId, "Id must not be null");
}

@Override
public String getCrdtId() {
    return crdtId;
}

@Override
public void subscribe(Subscriber<? super ORSetCommand<E>> subscriber) {
    commands.subscribe(subscriber);
}

@Override
public void subscribeTo(Publisher<? extends ORSetCommand<E>> publisher) {
    Flowable.fromPublisher(publisher).onTerminateDetach().subscribe(command -> {
        final Option<ORSetCommand<E>> newCommand = processCommand(command);
        newCommand.peek(commands::onNext);

    });
}

private Option<ORSetCommand<E>> processCommand(ORSetCommand<E> command) {
    if (command instanceof AddCommand) {
        return doAdd(((AddCommand<E>) command).getElement())? Option.of(command) : Option.none();
    } else if (command instanceof RemoveCommand) {
        return doRemove(((RemoveCommand<E>) command).getElements())? Option.of(command) : Option.none();
    }
    return Option.none();
}

@Override
public int size() {
    return doElements().size();
}

@Override
public Iterator<E> iterator() {
    return new ORSetIterator();
}

@Override
public boolean add(E value) {
    final boolean contained = doContains(value);
    prepareAdd(value);
    return !contained;
}

private static <U> Predicate<Element<U>> matches(U value) {
    return element -> Objects.equals(value, element.getValue());
}

private synchronized boolean doContains(E value) {
    return elements.parallelStream().anyMatch(matches(value));
}

private synchronized Set<E> doElements() {
    return elements.parallelStream().map(Element::getValue).collect(Collectors.toSet());
}

private synchronized void prepareAdd(E value) {
    final Element<E> element = new Element<>(value, UUID.randomUUID());
    commands.onNext(new AddCommand<>(getCrdtId(), element));
    doAdd(element);
}

private synchronized boolean doAdd(Element<E> element) {
    return (elements.add(element) | elements.removeAll(tombstone)) && (!tombstone.contains(element));
}

private synchronized void prepareRemove(E value) {
    final Set<Element<E>> removes = elements.parallelStream().filter(matches(value)).collect(Collectors.toSet());
    commands.onNext(new RemoveCommand<>(getCrdtId(), removes));
    doRemove(removes);
}

private synchronized boolean doRemove(Collection<Element<E>> removes) {
    return elements.removeAll(removes) | tombstone.addAll(removes);
}

}
```

### **4.4.2 用户视角**

### **正常同步的场景**

Data Type: Strings
Use Case: Common SETs Conflict Resolution: None

![](https://pic1.zhimg.com/80/v2-69997f2d802f65f8d27e63f925b913b4_720w.webp)

### **并发冲突的场景**

Data Type: Strings
Use Case: Concurrent SETs
Conflict Resolution: Last Write Wins (LWW)

![](https://pic2.zhimg.com/80/v2-d939f476b8122009dd184dd211c1c2ed_720w.webp)

## **五、未完待续**

由于篇幅限制，我们详细介绍了 CRDT 同步的理论基础以及一个Redis 的 K/V 数据结构在 CRDT 中是如何展现出来的。对 CRDT 或分布式数据库感兴趣的同学，请关注携程的公众号，也可以支持一下我们目前已经开源的的redis同步产品 -- [XPipe](https://link.zhihu.com/?target=https%3A//github.com/ctripcorp/x-pipe)([**https://****github.com/ctripcorp/x-****pipe**](https://link.zhihu.com/?target=https%3A//github.com/ctripcorp/x-pipe))。

## **附录**

[1] [携程Redis海外机房数据同步实践](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMjM5MDI3MjA5MQ%3D%3D%26mid%3D2697267768%26idx%3D1%26sn%3Dd8f38ab6e6e034ad36b9d1a47a792e45%26scene%3D21%23wechat_redirect)

[2] [CRDT——解决最终一致问题的利器](https://link.zhihu.com/?target=https%3A//yq.aliyun.com/articles/635632%3Futm_content%3Dm_1000015503)

[3] CRDT: [**https://****hal.inria.fr/inria-0060****9399/document**](https://link.zhihu.com/?target=https%3A//hal.inria.fr/inria-00609399/document)

[4] Eric Brewer: [**https://www.****infoq.com/articles/cap-****twelve-years-later-how-the-rules-have-changed**](https://link.zhihu.com/?target=https%3A//www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed)

[5] redislabs, Developing Applications with Geo-replicated CRDBs on Redis Enterprise Software(RS): [**https://****redislabs.com/redis-ent****erprise-documentation/developing/crdbs/**](https://link.zhihu.com/?target=https%3A//redislabs.com/redis-enterprise-documentation/developing/crdbs/)

[6] riak: [**https://****docs.basho.com/riak/kv/****2.0.0/developing/data-types/**](https://link.zhihu.com/?target=https%3A//docs.basho.com/riak/kv/2.0.0/developing/data-types/)

[7] cosmosDB: [**https://****docs.microsoft.com/en-u****s/azure/cosmos-db/multi-region-writers**](https://link.zhihu.com/?target=https%3A//docs.microsoft.com/en-us/azure/cosmos-db/multi-region-writers)

[8] A comprehensive study of Convergent and Commutative Replicated Data Types([**https://****links.jianshu.com/go?****to=http%3A%2F%2Fhal.upmc.fr%2Ffile%2Findex%2Fdocid%2F555588%2Ffilename%2Ftechreport.pdf**](https://link.zhihu.com/?target=https%3A//links.jianshu.com/go%3Fto%3Dhttp%253A%252F%252Fhal.upmc.fr%252Ffile%252Findex%252Fdocid%252F555588%252Ffilename%252Ftechreport.pdf))

[9] CRDT Java: [**https://****github.com/netopyr/wurm****loch-crdt**](https://link.zhihu.com/?target=https%3A//github.com/netopyr/wurmloch-crdt)

**【作者简介】** 祝辰，携程框架架构研发部资深研发工程师，主要负责Redis跨站点容灾方面的工作, 目前致力于研究分布式系统中的一致性问题以及相关理论和解决方案。此前曾就职于EMC混合云部门。对底层技术比较感兴趣，乐于研究操作系统和各种数据库的实现思路。
