```plantuml
entity hypergraph::NodeMap {
+    type = unsigned long
}

struct hypergraph::Hyperedge {
+    hypergraph::NodeMap left;
+    hypergraph::NodeMap right;
}

struct hypergraph::Node {
+    std::vector<unsigned int> complex_edges;
+    std::vector<unsigned int> simple_edges;
+    hypergraph::NodeMap simple_neighborhood;
+    static const int Size;
-    char padding[8];
}

hypergraph::NodeMap *-- hypergraph::Hyperedge::left
hypergraph::NodeMap *-- hypergraph::Hyperedge::right
hypergraph::NodeMap *-- hypergraph::Node::simple_neighborhood

struct hypergraph::Hypergraph {
+    Mem_root_array<hypergraph::Node> nodes;
+    Mem_root_array<hypergraph::Hyperedge> edges;

+    Hypergraph(MEM_ROOT *);
+    void AddNode(void);
+    void AddEdge(hypergraph::NodeMap, hypergraph::NodeMap);
+    void ModifyEdge(unsigned int, hypergraph::NodeMap, hypergraph::NodeMap);
-    void AttachEdgeToNodes(size_t, size_t, hypergraph::NodeMap, hypergraph::NodeMap);
}

hypergraph::Hypergraph::nodes --* hypergraph::Node
hypergraph::Hypergraph::edges --* hypergraph::Hyperedge

struct JoinHypergraph {
+    hypergraph::Hypergraph graph;
+    SecondaryEngineCostingFlags secondary_engine_costing_flags;
+    std::array<int, 61> table_num_to_node_num;
+    Mem_root_array<JoinHypergraph::Node> nodes;
+    Mem_root_array<JoinPredicate> edges;
+    Mem_root_array<Predicate> predicates;
+    unsigned int num_where_predicates;
+    OverflowBitset materializable_predicates;
+    mem_root_unordered_map<Item*, int, std::hash<Item*>, std::equal_to<Item*>> sargable_join_predicates;
+    bool has_reordered_left_joins;
+    table_map tables_inner_to_outer_or_anti;

-    const Query_block *m_query_block;

+    JoinHypergraph(MEM_ROOT *, const Query_block *);
+    const Query_block * query_block(void) const;
+    const JOIN * join(void) const;
}

JoinHypergraph::graph --* hypergraph::Hypergraph
```