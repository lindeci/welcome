- [PT\_inline\_index\_definition](#pt_inline_index_definition)
- [PT\_table\_constraint\_def](#pt_table_constraint_def)
- [PT\_table\_element](#pt_table_element)
- [PT\_key\_part\_specification](#pt_key_part_specification)

# PT_inline_index_definition
```cpp
class PT_inline_index_definition : public PT_table_constraint_def {
  private:
    keytype m_keytype;
    const LEX_STRING m_name;
    PT_base_index_option *m_type;
    List<PT_key_part_specification> *m_columns;
    Index_options m_options;

  public:
    PT_inline_index_definition(const POS &, keytype, const LEX_STRING &, PT_base_index_option *, List<PT_key_part_specification> *, Index_options);
    virtual bool do_contextualize(context_t *);
}
```

```
-exec p typeid(*element).name()
$4 = 0x655c040 <typeinfo name for PT_inline_index_definition> "26PT_inline_index_definition"

-exec p *(PT_key_part_specification*)((*(((PT_inline_index_definition*)(element))->m_columns)->first)->next.info)
```

# PT_table_constraint_def
```cpp
class PT_table_constraint_def : public PT_table_element {
  protected:
    PT_table_constraint_def(const POS &);
}
```

# PT_table_element
```cpp
class PT_table_element : public Parse_tree_node_tmpl<Table_ddl_parse_context> {
  protected:
    PT_table_element(const POS &);
}
```


# PT_key_part_specification
```cpp
class PT_key_part_specification : public Parse_tree_node_tmpl<Parse_context> {
  private:
    Item *m_expression;
    enum_order m_order;
    LEX_CSTRING m_column_name;
    int m_prefix_length;

  public:
    PT_key_part_specification(const POS &, Item *, enum_order);
    PT_key_part_specification(const POS &, const LEX_CSTRING &, enum_order, int);
    virtual bool do_contextualize(Parse_context *);
    Item * get_expression(void) const;
    enum_order get_order(void) const;
    bool is_explicit(void) const;
    bool has_expression(void) const;
    LEX_CSTRING get_column_name(void) const;
    int get_prefix_length(void) const;
}
```

