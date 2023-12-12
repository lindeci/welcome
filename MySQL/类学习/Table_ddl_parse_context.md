
- [Table\_ddl\_parse\_context](#table_ddl_parse_context)
- [Parse\_context](#parse_context)
- [Parse\_context\_base](#parse_context_base)

# Table_ddl_parse_context
```cpp
struct Table_ddl_parse_context : public Parse_context {
    HA_CREATE_INFO * const create_info;
    Alter_info * const alter_info;
    KEY_CREATE_INFO * const key_create_info;
  public:
    Table_ddl_parse_context(THD *, Query_block *, Alter_info *);
}
```

# Parse_context
```cpp
struct Parse_context : public Parse_context_base {
    THD * const thd;
    MEM_ROOT *mem_root;
    Query_block *select;
    mem_root_deque<QueryLevel> m_stack;
  public:
    bool finalize_query_expression(void);
    Parse_context(THD *, Query_block *, bool, Show_parse_tree *);
    Parse_context(THD *, Query_block *, bool);
    Parse_context(THD *, Query_block *, Show_parse_tree *);
    bool is_top_level_union_all(Surrounding_context);
}
```

# Parse_context_base
```cpp
struct Parse_context_base {
    std::unique_ptr<Show_parse_tree, std::default_delete<Show_parse_tree> > m_show_parse_tree;
  public:
    Parse_context_base(bool, Show_parse_tree *);
}
```