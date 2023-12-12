rm -rf ../nodes-63*.conf
./redis-server --port 6380 --loglevel debug --cluster-enabled yes --cluster-config-file ../nodes-6380.conf
./redis-server --port 6381 --loglevel debug --cluster-enabled yes --cluster-config-file ../nodes-6381.conf
./redis-server --port 6382 --loglevel debug --cluster-enabled yes --cluster-config-file ../nodes-6382.conf
./redis-server --port 6383 --loglevel debug --cluster-enabled yes --cluster-config-file ../nodes-6383.conf

./redis-cli --cluster-replicas 0 --cluster create 127.0.0.1:6379 127.0.0.1:6380 127.0.0.1:6381 127.0.0.1:6382 127.0.0.1:6383

cluster nodes
371361e44496f56235fafd0ccafd57abb1b4f497 127.0.0.1:6379@16379 myself,master - 0 1679036307000 1 connected 0-3276
341a309f879dbf79129e3f864f8dd54fc70caf00 127.0.0.1:6382@16382 master - 0 1679036305684 4 connected 9830-13106
776d1ffd24984474474ce083b30d28ddfc74f2e9 127.0.0.1:6383@16383 master - 0 1679036306688 5 connected 13107-16383
4fc35726ee7c382b9a641dc3012c6c3df4562cf8 127.0.0.1:6381@16381 master - 0 1679036307694 3 connected 6554-9829
16cfdbb10694e8e6e9030fdb2fad677cc995b5c3 127.0.0.1:6380@16380 master - 0 1679036307000 2 connected 3277-6553

printf "type:%d, count:%d", ntohs(hdr->type), ntohs(hdr->count)
type:1, count:3

p *hdr
$6 = {sig = "RCmb", totlen = 134873088, ver = 256, port = 60952, type = 256, count = 768, currentEpoch = 360287970189639680, configEpoch = 288230376151711744, offset = 0, 
sender = "341a309f879dbf79129e3f864f8dd54fc70caf00", myslots = '\000' <repeats 1228 times>..., slaveof = '\000' <repeats 39 times>, myip = '\000' <repeats 45 times>, extensions = 0, 
notused1 = '\000' <repeats 29 times>, pport = 0, cport = 65087, flags = 4352, state = 0 '\000', mflags = "\000\000", data = {


-exec p hdr->data->ping->gossip[0]
$3 = {nodename = "371361e44496f56235fafd0ccafd57abb1b4f497", ping_sent = 0, pong_received = 2920223844, ip = "127.0.0.1", '\000' <repeats 36 times>, port = 60184, cport = 64319, flags = 256, pport = 0, notused1 = 0}
-exec p hdr->data->ping->gossip[1]
$4 = {nodename = "4fc35726ee7c382b9a641dc3012c6c3df4562cf8", ping_sent = 0, pong_received = 2937001060, ip = "127.0.0.1", '\000' <repeats 36 times>, port = 60696, cport = 64831, flags = 256, pport = 0, notused1 = 0}
-exec p hdr->data->ping->gossip[2]
$5 = {nodename = "16cfdbb10694e8e6e9030fdb2fad677cc995b5c3", ping_sent = 0, pong_received = 2920223844, ip = "127.0.0.1", '\000' <repeats 36 times>, port = 60440, cport = 64575, flags = 256, pport = 0, notused1 = 0}


11893:M 17 Mar 2023 14:58:55.882 . --- Processing packet of type pong, 2568 bytes
11893:M 17 Mar 2023 15:04:30.427 . pong packet received: 341a309f879dbf79129e3f864f8dd54fc70caf00
11893:M 17 Mar 2023 15:13:26.285 . GOSSIP 371361e44496f56235fafd0ccafd57abb1b4f497 127.0.0.1:6379@16379 master
11893:M 17 Mar 2023 15:16:11.466 . GOSSIP 4fc35726ee7c382b9a641dc3012c6c3df4562cf8 127.0.0.1:6381@16381 master
11893:M 17 Mar 2023 15:16:44.299 . GOSSIP 16cfdbb10694e8e6e9030fdb2fad677cc995b5c3 127.0.0.1:6380@16380 master

```cpp
typedef struct replBacklog {
    listNode *ref_repl_buf_node; /* Referenced node of replication buffer blocks,
                                  * see the definition of replBufBlock. */
    size_t unindexed_count;      /* The count from last creating index block. */
    rax *blocks_index;           /* The index of recorded blocks of replication
                                  * buffer for quickly searching replication
                                  * offset on partial resynchronization. */
    long long histlen;           /* Backlog actual data length */
    long long offset;            /* Replication "master offset" of first
                                  * byte in the replication backlog buffer.*/
} replBacklog;

typedef struct replBufBlock {
    int refcount;           /* Number of replicas or repl backlog using. */
    long long id;           /* The unique incremental number. */
    long long repl_offset;  /* Start replication offset of the block. */
    size_t size, used;
    char buf[];
} replBufBlock;



初始化
void createReplicationBacklog(void) {
    serverAssert(server.repl_backlog == NULL);
    server.repl_backlog = zmalloc(sizeof(replBacklog));
    server.repl_backlog->ref_repl_buf_node = NULL;
    server.repl_backlog->unindexed_count = 0;
    server.repl_backlog->blocks_index = raxNew();
    server.repl_backlog->histlen = 0;
    /* We don't have any data inside our buffer, but virtually the first
     * byte we have is the next byte that will be generated for the
     * replication stream. */
    server.repl_backlog->offset = server.master_repl_offset+1;
}

打印信息
 info = sdscatprintf(info,
            "master_failover_state:%s\r\n"
            "master_replid:%s\r\n"
            "master_replid2:%s\r\n"
            "master_repl_offset:%lld\r\n"
            "second_repl_offset:%lld\r\n"
            "repl_backlog_active:%d\r\n"
            "repl_backlog_size:%lld\r\n"
            "repl_backlog_first_byte_offset:%lld\r\n"
            "repl_backlog_histlen:%lld\r\n",
            getFailoverStateString(),
            server.replid,
            server.replid2,
            server.master_repl_offset,
            server.second_replid_offset,
            server.repl_backlog != NULL,
            server.repl_backlog_size,
            server.repl_backlog ? server.repl_backlog->offset : 0,
            server.repl_backlog ? server.repl_backlog->histlen : 0);


```