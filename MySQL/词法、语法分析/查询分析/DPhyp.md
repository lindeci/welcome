# EnumerateCsgRec
is responsible for enumerating connected subgraphs.  
It does so by calculating the neighborhood and iterating over each of its subset.   
For each such subset `S_1`, it calls `EmitCsg`.

计算邻居，枚举所有的CSG,每个CSG中调用 EmitCsg

# EmitCsg
This member function is responsible for finding suitable complements.   
It does so by calling `EnumerateCmpRec`.

寻找cmp，然后调用 EnumerateCmpRec

# EnumerateCmpRec
recursively enumerates the complements `S_2` for the connected subgraph `S_1` found before.   
The pair (`S_1`, `S_2`) is a csg-cmp-pair.   
For every such pair, `EmitCsgCmp` is called.

对于之前找到的 S_1 ，递归的枚举它的 cmp 为 S_2，直至 S_2 跟 S_1 连通。 此时 (S_1, S_2) 是 csg-cmp-pair。   
对于每个 csg-cmp-pair，调用 EmitCsgCmp

# EmitCsgCmp
Its main responsibility is to consider a plan built up from the plans for `S_1` and `S_2`.

它的职责是计算 S_1 和 S_2 的执行计划代价

$$min(S) = \{s|s ∈ S, ∀s' ∈ S \space s ≠ s' ⇒ s ≺ s'\}$$
$$E↓'(S, X) = \{v|(u, v) ∈ E, u ⊆ S, v ∩ S = ∅, v ∩ X = ∅\}$$
Define $E↓(S, X)$ to be the minimal set of hypernodes such that for all $v ∈ E↓'(S, X)$ there exists a hypernode $v'$ in $E↓(S, X)$ such that $v' ⊆ v$. 
$$\mathcal{N}(S, X) = \underset{v∈E↓(S,X)}{∪}min(v)$$

# 伪代码
## Solve()
$$
\begin{align*}
&\text{Solve()} \\
&\text{for each } v \in V\quad \text{// initialize dpTable} \\
&\quad dpTable\{v\} = \text{plan for } v \\
&\text{for each } v \in V \text{ descending according to } \prec \\
&\quad EmitCsg\{v\} \quad \text{// process singleton sets} \\
&\quad EnumerateCsgRec\{v,\mathcal{B}_v\} \quad \text{// expand singleton sets} \\
&\text{return } dpTable[V]
\end{align*}
$$
在第一个循环中，它初始化动态规划表，为单个关系制定计划。在第二个循环中，它按照递减的顺序（根据≺）对查询图中的每个节点调用两个子程序 $EmitCsg$ 和 $EnumerateCsgRec$。算法对单个节点 $v ∈ V$ 调用 $EmitCsg(\{v\})$，通过调用 $EnumerateCsgCmp$ 和 $EmitCsgCmp$ 生成所有的 $csg{-}cmp{-}pairs (\{v\}, S_2)$，其中 $v ≺ min(S_2)$ 成立。这个条件意味着每个 $csg{-}cmp{-}pairs$ 只生成一次，不会生成对称的对。在图3中，这对应于单顶点图，例如步骤1和2。对 $EnumerateCsgRec$ 的调用将初始集 $\{v\}$ 扩展到更大的集合 $S_1$，然后找到其补集 $S_2$ 的连接子集，使得 $(S_1, S_2)$ 结果为一个$csg{-}cmp{-}pairs$。在图3中，这在步骤2中显示，例如，其中 $EnumerateCsgRec$ 从 $R_5$ 开始，并在步骤4中将其扩展到 $\{R5, R6\}$（步骤3是补集的构造）。为了避免在枚举过程中出现重复，所有按照 $≺$ 排在 $v$ 之前的节点在递归扩展过程中都被禁止。正式地，我们定义这个集合为 $B_v = \{w|w ≺ v\} ∪ \{v\}$。

## $EnumerateCsgRec(S_1, X)$
$$
\begin{align*}
&EnumerateCsgRec(S_1,X) \\
&\text{for each } N \in \mathcal{N}(S_1,X); N \neq \emptyset \\
&\quad \text{if } dpTable[S_1 \cup N] \neq \emptyset \\
&\quad \quad EmitCsg(S_1 \cup N) \\
&\text{for each } N \in \mathcal{N}(S_1,X); N \neq \emptyset \\
&\quad EnumerateCsgRec(S_1 \cup N,X \cup \mathcal{N}(S_1,X))
\end{align*}
$$
$EnumerateCsgRec$ 目的是扩展给定的集合 $S_1$，该集合在 $G$ 中引导出一个连通子图，以形成具有相同属性的更大的集合。它通过考虑 $S_1$ 的邻域的每个非空的、适当的子集来实现这一点。对于这些子集中的每一个 $N$，它检查 $S_1 ∪ N$ 是否是一个连通补集。这是通过查找 $dpTable$ 来完成的。如果这个测试成功，那么就找到了一个新的连通补集，并通过调用 $EmitCsg(S_1 ∪ N)$ 进行进一步处理。然后，在第二步中，对于邻域的所有这些子集 $N$，我们调用 $EnumerateCsgRec$，以便 $S_1 ∪ N$ 可以递归地进一步扩展。我们首先调用 $EmitCsg$ 然后再调用 $EnumerateCsgRec$ 的原因是，为了使枚举序列对动态规划有效，必须首先生成较小的集合。总结起来，代码如下：

看看步骤12。这个调用是由 $Solve$ 在 $S_1 = \{R_2\}$ 上生成的。邻域只包含 $\{R_3\}$，因为 $R_1$ 在 $X$ 中（$R_4，R_5，R_6$ 不在 $X$ 中，但是不可达）。$EnumerateCsgRec$ 首先调用 $EmitCsg$，它将创建可连接的补集（步骤13）。然后，它测试 $\{R_2, R_3\}$ 的连通性。相应的 $dpTable$ 条目是在步骤13中生成的。因此，这个测试成功，$\{R_2, R_3\}$ 通过对 $EnumerateCsgRec$ 的递归调用进行进一步处理（步骤14）。现在，扩展停止，因为 $\{R_2, R_3\}$ 的邻域是空的，因为 $R_1 ∈ X$。

##  EmitCsg
$$
\begin{align*}
&EmitCsg(S_1)  \\
&X = S_1 ∪ \mathcal{B}_{min(S_1)}  \\
&N = \mathcal{N} (S_1, X)  \\
&\text{for each } v ∈ N \text{ descending according to ≺}  \\
&\quad S_2 = \{v\}  \\
&\quad \text{if } ∃(u, v) ∈ E : u ⊆ S_1 ∧ v ⊆ S_2  \\
&\quad \quad EmitCsgCmp(S_1, S_2)  \\
&\quad EnumerateCmpRec(S_1, S_2, X)
\end{align*}
$$

$EmitCsg$ 接受一个非空的、适当的子集 $S_1$ 作为参数，该子集在 $V$ 中引导出一个连通子图。然后，它负责生成所有的 $S_2$ 的种子，使得 $(S_1, S_2)$ 成为一个 $csg{-}cmp{-}pairs$。不出所料，这些种子来自于 $S_1$ 的邻域。所有在 $S_1$ 中最小元素之前排序的节点（由集合 $\mathcal{B}_{min(S_1)}$ 捕获）都从邻域中移除，以避免重复的枚举[17]。由于邻域也包含超边 $(u, v)$ 的 $min(v)$，其中 $|v| > 1$，所以并不能保证 $S_1$ 与 $v$ 是连通的。为了避免生成错误的 $csg{-}cmp{-}pairs$，$EmitCsg$ 会检查连通性。然而，每一个单独的邻居都可能被扩展到 $S_1$ 的一个有效的补集 $S_2$。因此，在调用 $EnumerateCmpRec$ 之前，不需要进行这样的测试，$EnumerateCmpRec$ 会执行这个扩展。伪代码如下：

看看步骤20。当前的集合 $S_1$ 是 $S_1 = \{R_1, R_2, R_3\}$，邻域是 $\mathcal{N} = \{R_4\}$。由于没有超边连接这两个集合，所以没有调用 $EmitCsgCmp$。然而，集合 $\{R4\}$ 可以被扩展到一个有效的补集，即 $\{R_4, R_5, R_6\}$。适当地扩展补集的种子是在步骤21中对 $EnumerateCmpRec$ 的调用的任务。

## EnumerateCmpRec
$$
\begin{align*}
&EnumerateCmpRec(S_1, S_2, X)  \\
&\text{for each } N ⊆ \mathcal{N} (S_2, X): N ≠ ∅  \\
&\quad \text{if }dpTable[S_2 ∪ N] ≠ ∅ ∧ ∃(u, v) ∈ E : u ⊆ S_1 ∧ v ⊆ S_2 ∪ N  \\
&\quad \quad EmitCsgCmp(S_1, S_2 ∪ N)  \\
&X = X ∪ \mathcal{N} (S_2, X)  \\
&\text{for each } N ⊆ \mathcal{N} (S_2, X): N ≠ ∅  \\
&\quad EnumerateCmpRec(S_1, S_2 ∪ N, X)
\end{align*}
$$

$EnumerateCsgRec$ 有三个参数。第一个参数 $S_1$ 只用于传递给 $EmitCsgCmp$。第二个参数是一个集合 $S_2$，它是连通的，并且必须扩展直到达到一个有效的 $csg{-}cmp{-}pairs$。因此，它考虑 $S_2$ 的邻域。对于邻域的每一个非空的、适当的子集 $N$，它检查 $S_2 ∪ N$ 是否引导出一个连通的子集并且与 $S_1$ 连通。如果是这样，我们就有了一个有效的 $csg{-}cmp{-}pairs (S_1, S_2)$ 并且可以开始构造计划（在 $EmitCsgCmp$ 中完成）。无论测试的结果如何，我们都会递归地尝试扩展 $S_2$，以使这个测试成功。总的来说，$EnumerateCmpRec$ 的行为非常像$EnumerateCsgRec$。它的伪代码如下：

再看一下步骤21。参数是 $S_1 = \{R_1, R_2, R_3\}$ 和 $S_2 = \{R_4\}$。邻域由单一关系 $R_5$ 组成。集合 $\{R_4, R_5\}$ 引导出一个连通的子图。它在步骤6中被插入到 $dpTable$ 中。然而，没有超边将其连接到 $S_1$。因此，没有调用 $EmitCsgCmp$。接下来是步骤22中的递归调用，其中 $S_2$ 改变为 $\{R_4, R_5\}$。它的邻域是 $\{R_6\}$。集合 $\{R_4, R_5, R_6\}$ 引导出一个连通的子图。通过查找 $dpTable$ 进行的相应测试成功，因为相应的条目是在步骤7中生成的。测试的第二部分也成功，因为我们唯一的真正的超边将这个集合与 $S_1$ 连接起来。因此，步骤23中的调用 $EmitCsgCmp$ 发生，并生成包含所有关系的计划。

## EmitCsgCmp
$$
\begin{align*}
&EmitCsgCmp(S_1, S_2)  \\
&plan_1 = dpTable[S_1]  \\
&plan_2 = dpTable[S_2]  \\
&S = S_1 ∪ S_2  \\
&p = ∧_{(u_1,u_2)∈E,u_i⊆S_i}\mathcal{P}(u_1, u_2)  \\
&newplan = plan_1 \space ⨝_p \space plan_2  \\
&\text{if } dpTable[S]= ∅ ∨ cost(newplan) < cost(dpTable[S])  \\
&\quad dpTable[S] = newplan  \\
&newplan = plan_2 \space ⨝_p \space plan_1 \quad \text{// for commutative ops only}  \\
&\text{if } cost(newplan) < dpTable[S]  \\
&\quad dpTable[S] = newplan
\end{align*}
$$

$EmitCsgCmp(S_1, S_2)$ 的任务是连接 $S_1$ 和 $S_2$ 的最优计划，这两个计划必须形成一个 $csg{-}cmp{-}pairs$。为此，我们必须能够计算出正确的连接谓词和结果连接的成本。这就要求将连接谓词、选择性和基数附加到超图上。由于我们在一个抽象函数 $cost$ 中隐藏了成本计算，所以我们只需要显式地组装连接谓词。对于给定的超图 $G = (V, E)$ 和超边 $(u, v) ∈ E$，我们用 $\mathcal{P}(u, v)$ 表示超边 $(u, v)$ 表示的谓词。

EmitCsgCmp的伪代码应该看起来很熟悉：

首先，从动态规划表中恢复 $S_1$ 和 $S_2$ 的最优计划。然后，我们在 $S$ 中记住要构造的计划中存在的关系的总集合。我们查看每一个将 $S_1$ 和 $S_2$ 连接起来的超边，取它们的谓词，然后将这些谓词进行"与"操作，得到的结果就是连接谓词 $p$。然后，构造计划，如果它们比现有的计划更便宜，就存储在 $dpTable$ 中。

计算谓词 $p$ 似乎很昂贵，因为所有的边都必须被测试。然而，我们可以将谓词集合
$$p_S = \{\mathcal{P}(u, v)|(u, v) ∈ E, u ⊆ S\}$$
附加到任何计划类 $S ⊆ V$。如果我们用位向量表示 $p_S$，那么对于一个 $csg{-}cmp{-}pairs$，我们可以很容易地计算 $p_{S_1} ∩ p_{S_3}$ 并只考虑结果。