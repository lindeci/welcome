# ABSTRACT

Two highly efficient algorithms are known for optimally ordering joins while avoiding cross products: DPccp, which is
based on dynamic programming, and Top-Down Partition
Search, based on memoization. Both have two severe limitations: They handle only (1) simple (binary) join predicates
and (2) inner joins. However, real queries may contain complex join predicates, involving more than two relations, and
outer joins as well as other non-inner joins.
Taking the most efficient known join-ordering algorithm,
DPccp, as a starting point, we first develop a new algorithm,
DPhyp, which is capable to handle complex join predicates
efficiently. We do so by modeling the query graph as a (variant of a) hypergraph and then reason about its connected
subgraphs. Then, we present a technique to exploit this capability to efficiently handle the widest class of non-inner
joins dealt with so far. Our experimental results show that
this reformulation of non-inner joins as complex predicates
can improve optimization time by orders of magnitude, compared to known algorithms dealing with complex join predicates and non-inner joins. Once again, this gives dynamic
programming a distinct advantage over current memoization
techniques
