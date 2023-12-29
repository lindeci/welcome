- [AccessPath](#accesspath)
- [AccessPath::Type](#accesspathtype)
- [AccessPath::Safety](#accesspathsafety)
- [RowIterator](#rowiterator)
- [OverflowBitset](#overflowbitset)
- [OverflowBitset::Ext](#overflowbitsetext)
- [AccessPath::u 的 hash\_join](#accesspathu-的-hash_join)
  - [JoinPredicate](#joinpredicate)

# AccessPath
```cpp
struct AccessPath {
  public:
    AccessPath::Type type;
    AccessPath::Safety safe_for_rowid;
    bool count_examined_rows : 1;
    bool forced_by_dbug : 1;
    int8_t immediate_update_delete_table;
    int ordering_state;
    RowIterator *iterator;
    double cost;
    double init_cost;
    double init_once_cost;
    double num_output_rows_before_filter;
    double cost_before_filter;
    OverflowBitset filter_predicates;
    OverflowBitset delayed_predicates;
    hypergraph::NodeMap parameter_tables;
    void *secondary_engine_data;
  private:
    double m_num_output_rows;
    union {
        struct {...} table_scan;
        struct {...} index_scan;
        struct {...} ref;
        struct {...} ref_or_null;
        struct {...} eq_ref;
        struct {...} pushed_join_ref;
        struct {...} full_text_search;
        struct {...} const_table;
        struct {...} mrr;
        struct {...} follow_tail;
        struct {...} index_range_scan;
        struct {...} index_merge;
        struct {...} rowid_intersection;
        struct {...} rowid_union;
        struct {...} index_skip_scan;
        struct {...} group_index_skip_scan;
        struct {...} dynamic_index_range_scan;
        struct {...} materialized_table_function;
        struct {...} unqualified_count;
        struct {...} table_value_constructor;
        struct {...} fake_single_row;
        struct {...} zero_rows;
        struct {...} zero_rows_aggregated;
        struct {...} hash_join;
        struct {...} bka_join;
        struct {...} nested_loop_join;
        struct {...} nested_loop_semijoin_with_duplicate_removal;
        struct {...} filter;
        struct {...} sort;
        struct {...} aggregate;
        struct {...} temptable_aggregate;
        struct {...} limit_offset;
        struct {...} stream;
        struct {...} materialize;
        struct {...} materialize_information_schema_table;
        struct {...} append;
        struct {...} window;
        struct {...} weedout;
        struct {...} remove_duplicates;
        struct {...} remove_duplicates_on_index;
        struct {...} alternative;
        struct {...} cache_invalidator;
        struct {...} delete_rows;
        struct {...} update_rows;
    } u;

  public:
    AccessPath(void);
    double rescan_cost(void) const;
    OverflowBitset & applied_sargable_join_predicates(void);
    const OverflowBitset & applied_sargable_join_predicates(void) const;
    OverflowBitset & subsumed_sargable_join_predicates(void);
    const OverflowBitset & subsumed_sargable_join_predicates(void) const;
    auto & table_scan(void);
    const auto & table_scan(void) const;
    auto & index_scan(void);
    const auto & index_scan(void) const;
    auto & ref(void);
    const auto & ref(void) const;
    auto & ref_or_null(void);
    const auto & ref_or_null(void) const;
    auto & eq_ref(void);
    const auto & eq_ref(void) const;
    auto & pushed_join_ref(void);
    const auto & pushed_join_ref(void) const;
    auto & full_text_search(void);
    const auto & full_text_search(void) const;
    auto & const_table(void);
    const auto & const_table(void) const;
    auto & mrr(void);
    const auto & mrr(void) const;
    auto & follow_tail(void);
    const auto & follow_tail(void) const;
    auto & index_range_scan(void);
    const auto & index_range_scan(void) const;
    auto & index_merge(void);
    const auto & index_merge(void) const;
    auto & rowid_intersection(void);
    const auto & rowid_intersection(void) const;
    auto & rowid_union(void);
    const auto & rowid_union(void) const;
    auto & index_skip_scan(void);
    const auto & index_skip_scan(void) const;
    auto & group_index_skip_scan(void);
    const auto & group_index_skip_scan(void) const;
    auto & dynamic_index_range_scan(void);
    const auto & dynamic_index_range_scan(void) const;
    auto & materialized_table_function(void);
    const auto & materialized_table_function(void) const;
    auto & unqualified_count(void);
    const auto & unqualified_count(void) const;
    auto & table_value_constructor(void);
    const auto & table_value_constructor(void) const;
    auto & fake_single_row(void);
    const auto & fake_single_row(void) const;
    auto & zero_rows(void);
    const auto & zero_rows(void) const;
    auto & zero_rows_aggregated(void);
    const auto & zero_rows_aggregated(void) const;
    auto & hash_join(void);
    const auto & hash_join(void) const;
    auto & bka_join(void);
    const auto & bka_join(void) const;
    auto & nested_loop_join(void);
    const auto & nested_loop_join(void) const;
    auto & nested_loop_semijoin_with_duplicate_removal(void);
    const auto & nested_loop_semijoin_with_duplicate_removal(void) const;
    auto & filter(void);
    const auto & filter(void) const;
    auto & sort(void);
    const auto & sort(void) const;
    auto & aggregate(void);
    const auto & aggregate(void) const;
    auto & temptable_aggregate(void);
    const auto & temptable_aggregate(void) const;
    auto & limit_offset(void);
    const auto & limit_offset(void) const;
    auto & stream(void);
    const auto & stream(void) const;
    auto & materialize(void);
    const auto & materialize(void) const;
    auto & materialize_information_schema_table(void);
    const auto & materialize_information_schema_table(void) const;
    auto & append(void);
    const auto & append(void) const;
    auto & window(void);
    const auto & window(void) const;
    auto & weedout(void);
    const auto & weedout(void) const;
    auto & remove_duplicates(void);
    const auto & remove_duplicates(void) const;
    auto & remove_duplicates_on_index(void);
    const auto & remove_duplicates_on_index(void) const;
    auto & alternative(void);
    const auto & alternative(void) const;
    auto & cache_invalidator(void);
    const auto & cache_invalidator(void) const;
    auto & delete_rows(void);
    const auto & delete_rows(void) const;
    auto & update_rows(void);
    const auto & update_rows(void) const;
    double num_output_rows(void) const;
    void set_num_output_rows(double);
}
```

# AccessPath::Type
```cpp
AccessPath::Type : unsigned char {
    AccessPath::TABLE_SCAN, 
    AccessPath::INDEX_SCAN, 
    AccessPath::REF, 
    AccessPath::REF_OR_NULL, 
    AccessPath::EQ_REF, 
    AccessPath::PUSHED_JOIN_REF, 
    AccessPath::FULL_TEXT_SEARCH, 
    AccessPath::CONST_TABLE, 
    AccessPath::MRR, 
    AccessPath::FOLLOW_TAIL, 
    AccessPath::INDEX_RANGE_SCAN, 
    AccessPath::INDEX_MERGE, 
    AccessPath::ROWID_INTERSECTION, 
    AccessPath::ROWID_UNION, 
    AccessPath::INDEX_SKIP_SCAN, 
    AccessPath::GROUP_INDEX_SKIP_SCAN, 
    AccessPath::DYNAMIC_INDEX_RANGE_SCAN, 
    AccessPath::TABLE_VALUE_CONSTRUCTOR, 
    AccessPath::FAKE_SINGLE_ROW, 
    AccessPath::ZERO_ROWS, 
    AccessPath::ZERO_ROWS_AGGREGATED, 
    AccessPath::MATERIALIZED_TABLE_FUNCTION, 
    AccessPath::UNQUALIFIED_COUNT, 
    AccessPath::NESTED_LOOP_JOIN, 
    AccessPath::NESTED_LOOP_SEMIJOIN_WITH_DUPLICATE_REMOVAL, 
    AccessPath::BKA_JOIN, 
    AccessPath::HASH_JOIN, 
    AccessPath::FILTER, 
    AccessPath::SORT, 
    AccessPath::AGGREGATE, 
    AccessPath::TEMPTABLE_AGGREGATE, 
    AccessPath::LIMIT_OFFSET, 
    AccessPath::STREAM, 
    AccessPath::MATERIALIZE, 
    AccessPath::MATERIALIZE_INFORMATION_SCHEMA_TABLE, 
    AccessPath::APPEND, 
    AccessPath::WINDOW, 
    AccessPath::WEEDOUT, 
    AccessPath::REMOVE_DUPLICATES, 
    AccessPath::REMOVE_DUPLICATES_ON_INDEX, 
    AccessPath::ALTERNATIVE, 
    AccessPath::CACHE_INVALIDATOR, 
    AccessPath::DELETE_ROWS, 
    AccessPath::UPDATE_ROWS
};
```

# AccessPath::Safety
```cpp
enum AccessPath::Safety : unsigned char {
    AccessPath::SAFE, 
    AccessPath::SAFE_IF_SCANNED_ONCE, 
    AccessPath::UNSAFE
}
```

# RowIterator
```cpp
class RowIterator {
  private:
    THD * const m_thd;

  public:
    RowIterator(THD *);
    RowIterator(const RowIterator &);
    RowIterator(RowIterator &&);
    ~RowIterator();
    virtual bool Init(void);
    virtual int Read(void);
    virtual void SetNullRowFlag(bool);
    virtual void UnlockRow(void);
    virtual const IteratorProfiler * GetProfiler(void) const;
    virtual void SetOverrideProfiler(const IteratorProfiler *);
    virtual void StartPSIBatchMode(void);
    virtual void EndPSIBatchModeIfStarted(void);
    virtual RowIterator * real_iterator(void);
    virtual const RowIterator * real_iterator(void) const;
  protected:
    THD * thd(void) const;
}
```

# OverflowBitset
```cpp
class OverflowBitset {
  protected:
    union {
        uint64_t m_bits;
        OverflowBitset::Ext *m_ext;
    };
  private:
    static const int kInlineBits;

  public:
    OverflowBitset(void);
    OverflowBitset(uint32_t);
    OverflowBitset(const OverflowBitset &);
    OverflowBitset(OverflowBitset &&);
    OverflowBitset(MutableOverflowBitset &&);
    void Clear(void);
    OverflowBitset & operator=(const OverflowBitset &);
    OverflowBitset & operator=(OverflowBitset &&);
    OverflowBitset & operator=(MutableOverflowBitset &&);
    bool is_inline(void) const;
    bool empty(void);
    size_t capacity(void) const;
    MutableOverflowBitset Clone(MEM_ROOT *) const;
    bool IsContainedIn(const MEM_ROOT *) const;
    static MutableOverflowBitset Or(MEM_ROOT *, OverflowBitset, OverflowBitset);
    static MutableOverflowBitset And(MEM_ROOT *, OverflowBitset, OverflowBitset);
    static MutableOverflowBitset Xor(MEM_ROOT *, OverflowBitset, OverflowBitset);
  protected:
    void InitOverflow(MEM_ROOT *, size_t);
    static MutableOverflowBitset OrOverflow(MEM_ROOT *, OverflowBitset, OverflowBitset);
    static MutableOverflowBitset AndOverflow(MEM_ROOT *, OverflowBitset, OverflowBitset);
    static MutableOverflowBitset XorOverflow(MEM_ROOT *, OverflowBitset, OverflowBitset);
}
```
这个没有名字的`union`在C++中被称为**匿名联合**。它的主要优点是可以直接访问其成员，而无需通过联合名称。在这个`OverflowBitset`类中，匿名联合包含了`m_bits`和`m_ext`两个成员，这意味着我们可以直接通过`m_bits`或`m_ext`来访问它们。

这个设计的主要目的是为了节省空间。`m_bits`和`m_ext`永远不会同时使用，所以没有必要为它们都分配内存。通过使用匿名联合，我们可以确保无论是使用`m_bits`还是`m_ext`，都只会占用`union`的空间。

在这个类中，`m_bits`用于存储小的（“内联”）位集，而`m_ext`则用于存储大的（“非内联”）位集。这样，我们就可以根据位集的大小来选择使用哪个成员，从而实现了存储的优化。

```cpp
class OverflowBitset {
 protected:
  struct Ext {
    size_t m_num_blocks;
    uint64_t m_bits[1];
  };
  union {
    uint64_t m_bits;  // Lowest bit must be 1.
    Ext *m_ext;
  };
  static constexpr int kInlineBits = sizeof(m_bits) * CHAR_BIT - 1;
}; 
```

# OverflowBitset::Ext
```cpp
struct OverflowBitset::Ext {
    size_t m_num_blocks;
    uint64_t m_bits[1];
}
```

# AccessPath::u 的 hash_join
```cpp
struct {
      AccessPath *outer, *inner;
      const JoinPredicate *join_predicate;
      bool allow_spill_to_disk;
      bool store_rowids;  // Whether we are below a weedout or not.
      bool rewrite_semi_to_inner;
      table_map tables_to_get_rowid_for;
    } hash_join;
```
## JoinPredicate
```cpp
struct JoinPredicate {
    RelationalExpression *expr;
    double selectivity;
    size_t estimated_bytes_per_row;
    FunctionalDependencySet functional_dependencies;
    Mem_root_array<int> functional_dependencies_idx;
    int ordering_idx_needed_for_semijoin_rewrite;
    Item **semijoin_group;
    int semijoin_group_size;
}
```