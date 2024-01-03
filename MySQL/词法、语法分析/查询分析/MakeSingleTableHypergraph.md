- [Table\_ref](#table_ref)
- [RelationalExpression](#relationalexpression)
- [CompanionSetCollection](#companionsetcollection)
  - [CompanionSet](#companionset)
    - [CompanionSet::EqualTerm](#companionsetequalterm)
    - [CompanionSet::FieldArray](#companionsetfieldarray)

# Table_ref
```cpp
class Table_ref {
  public:
    Table_ref *next_local;
    Table_ref *next_global;
    Table_ref **prev_global;
    const char *db;
    const char *table_name;
    const char *alias;
    LEX_CSTRING target_tablespace_name;
    char *option;
    Opt_hints_table *opt_hints_table;
    Opt_hints_qb *opt_hints_qb;
  private:
    uint m_tableno;
    table_map m_map;
    Item *m_join_cond;
    bool m_is_sj_or_aj_nest;
  public:
    table_map sj_inner_tables;
    Table_ref *natural_join;
    bool is_natural_join;
    List<String> *join_using_fields;
    List<Natural_join_column> *join_columns;
    bool is_join_columns_complete;
    Table_ref *next_name_resolution_table;
    List<Index_hint> *index_hints;
    TABLE *table;
    mysql::binlog::event::Table_id table_id;
    Query_result_union *derived_result;
    Table_ref *correspondent_table;
    Table_function *table_function;
    AccessPath *access_path_for_derived;
  private:
    Query_expression *derived;
    Common_table_expr *m_common_table_expr;
    const Create_col_name_list *m_derived_column_names;
  public:
    ST_SCHEMA_TABLE *schema_table;
    Query_block *schema_query_block;
    bool schema_table_reformed;
    Query_block *query_block;
  private:
    LEX *view;
  public:
    Field_translator *field_translation;
    Field_translator *field_translation_end;
    Table_ref *merge_underlying_list;
    mem_root_deque<Table_ref*> *view_tables;
    Table_ref *belong_to_view;
    Table_ref *referencing_view;
    Table_ref *parent_l;
    Security_context *security_ctx;
    Security_context *view_sctx;
    Table_ref *next_leaf;
    Item *derived_where_cond;
    Item *check_option;
    Item *replace_filter;
    LEX_STRING select_stmt;
    LEX_STRING source;
    LEX_STRING timestamp;
    LEX_USER definer;
    ulonglong updatable_view;
    ulonglong algorithm;
    ulonglong view_suid;
    ulonglong with_check;
  private:
    enum_view_algorithm effective_algorithm;
    Lock_descriptor m_lock_descriptor;
  public:
    GRANT_INFO grant;
    bool outer_join;
    bool join_order_swapped;
    uint shared;
    size_t db_length;
    size_t table_name_length;
  private:
    bool m_updatable;
    bool m_insertable;
    bool m_updated;
    bool m_inserted;
    bool m_deleted;
    bool m_fulltext_searched;
  public:
    bool straight;
    bool updating;
    bool ignore_leaves;
    table_map dep_tables;
    table_map join_cond_dep_tables;
    NESTED_JOIN *nested_join;
    Table_ref *embedding;
    mem_root_deque<Table_ref*> *join_list;
    bool cacheable_table;
    enum_open_type open_type;
    bool contain_auto_increment;
    bool check_option_processed;
    bool replace_filter_processed;
    dd::enum_table_type required_type;
    char timestamp_buffer[20];
    bool prelocking_placeholder;
    enum : unsigned int {Table_ref::OPEN_NORMAL, Table_ref::OPEN_IF_EXISTS, Table_ref::OPEN_FOR_CREATE, Table_ref::OPEN_STUB} open_strategy;
    bool internal_tmp_table;
    bool is_alias;
    bool is_fqtn;
    bool m_was_scalar_subquery;
    View_creation_ctx *view_creation_ctx;
    LEX_CSTRING view_client_cs_name;
    LEX_CSTRING view_connection_cl_name;
    LEX_STRING view_body_utf8;
    bool is_system_view;
    bool is_dd_ctx_table;
    List<Derived_key> derived_key_list;
    uint8 trg_event_map;
    bool schema_table_filled;
    MDL_request mdl_request;
    bool view_no_explain;
    List<String> *partition_names;
  private:
    Item *m_join_cond_optim;
  public:
    COND_EQUAL *cond_equal;
    bool optimized_away;
    bool derived_keys_ready;
  private:
    bool m_is_recursive_reference;
    enum_table_ref_type m_table_ref_type;
    ulonglong m_table_ref_version;
    Key_map covering_keys_saved;
    Key_map merge_keys_saved;
    Key_map keys_in_use_for_query_saved;
    Key_map keys_in_use_for_group_by_saved;
    Key_map keys_in_use_for_order_by_saved;
    bool nullable_saved;
    bool force_index_saved;
    bool force_index_order_saved;
    bool force_index_group_saved;
    MY_BITMAP lock_partitions_saved;
    MY_BITMAP read_set_saved;
    MY_BITMAP write_set_saved;
    MY_BITMAP read_set_internal_saved;
}
```

# RelationalExpression
```cpp
struct RelationalExpression {
    RelationalExpression::Type type;
    table_map tables_in_subtree;
    hypergraph::NodeMap nodes_in_subtree;
    const Table_ref *table;
    Mem_root_array<Item*> join_conditions_pushable_to_this;
    CompanionSet *companion_set;
    RelationalExpression *left;
    RelationalExpression *right;
    Mem_root_array<RelationalExpression*> multi_children;
    Mem_root_array<Item*> join_conditions;
    Mem_root_array<Item_eq_base*> equijoin_conditions;
    Mem_root_array<CachedPropertiesForPredicate> properties_for_join_conditions;
    Mem_root_array<CachedPropertiesForPredicate> properties_for_equijoin_conditions;
    bool join_conditions_reject_all_rows;
    table_map conditions_used_tables;
    int join_predicate_first;
    int join_predicate_last;
    Mem_root_array<ConflictRule> conflict_rules;
}
```

# CompanionSetCollection
```cpp
class CompanionSetCollection {
  private:
    std::array<CompanionSet*, 61> m_table_num_to_companion_set;
}
```

## CompanionSet
```cpp
class CompanionSet {
  private:
    Mem_root_array<CompanionSet::EqualTerm> m_equal_terms;

    typedef Mem_root_array<Field const*> FieldArray;
}
```

### CompanionSet::EqualTerm
```cpp
struct CompanionSet::EqualTerm {
    CompanionSet::FieldArray *fields;
    table_map tables;
}
```

### CompanionSet::FieldArray
```cpp
class Mem_root_array<Field const*> [with Element_type = const Field *] : public Mem_root_array_YY<Field const*> {

  public:
    typedef Element_type value_type;
    typedef Mem_root_array_YY<Field const*>::const_iterator const_iterator;
}
```