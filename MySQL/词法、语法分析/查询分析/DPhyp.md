# EnumerateCsgRec
is responsible for enumerating connected subgraphs.  
It does so by calculating the neighborhood and iterating over each of its subset.   
For each such subset `S1`, it calls `EmitCsg`.

计算邻居，枚举所有的CSG,每个CSG中调用 EmitCsg

# EmitCsg
This member function is responsible for finding suitable complements.   
It does so by calling `EnumerateCmpRec`.

寻找cmp，然后调用 EnumerateCmpRec

# EnumerateCmpRec
recursively enumerates the complements `S2` for the connected subgraph `S1` found before.   
The pair (`S1`, `S2`) is a csg-cmp-pair.   
For every such pair, `EmitCsgCmp` is called.

对于之前找到的 S1 ，递归的枚举它的 cmp 为 S2，直至 S2 跟 S1 连通。 此时 (S1, S2) 是 csg-cmp-pair。   
对于每个 csg-cmp-pair，调用 EmitCsgCmp

# EmitCsgCmp
Its main responsibility is to consider a plan built up from the plans for `S1` and `S2`.

它的职责是计算 S1 和 S2 的执行计划代价 

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
## EnumerateCsgRec(S1, X)
$$
\begin{align*}
&EnumerateCsgRec(S1,X) \\
&\text{for each } N \in \mathbb{N}(S1,X); N \neq \emptyset \\
&\quad \text{if } dpTable[S1 \cup N] \neq \emptyset \\
&\quad \quad EmitCsg(S1 \cup N) \\
&\text{for each } N \in \mathbb{N}(S1,X); N \neq \emptyset \\
&\quad EnumerateCsgRec(S1 \cup N,X \cup \mathbb{N}(S1,X))
\end{align*}
$$
##  EmitCsg
$$
$$