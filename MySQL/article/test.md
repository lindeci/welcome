@startuml
Class Parse_tree_node_tmpl
Class Item{
    + Item *next_free
    # String str_value
    + DTCollation collation
    + Item_name_string item_name
    + Item_name_string orig_name
    + uint32 max_length
    + Item::item_marker marker
    + Item_result cmp_context
    + uint m_ref_count
    + bool m_abandoned
    + const bool is_parser_item
    + uint8 m_data_type
    + CostOfItem m_cost
    + bool fixed
    + uint8 decimals
    - bool m_nullable
    + bool null_value
    + bool unsigned_flag
    + bool m_is_window_function
    + bool hidden
    + bool m_in_check_constraint_exec_ctx
    - static const uint8 PROP_SUBQUERY;
    - static const uint8 PROP_STORED_PROGRAM;
    - static const uint8 PROP_AGGREGATION;
    - static const uint8 PROP_WINDOW_FUNCTION;
    - static const uint8 PROP_ROLLUP_EXPR;
    - static const uint8 PROP_GROUPING_FUNC;
  # uint8 m_accum_properties;
}
note right: Item 类中定义了enum Type、enum cond_result、enum traverse_order

Class Item_result_field{
  # Field *result_field
}

Class Item_func{
 # Item **args
 - Item *m_embedded_arguments[2]
 + uint arg_count
 # bool null_on_null
 # uint allowed_arg_cols
 # table_map used_tables_cache
 # table_map not_null_tables_cache
 + enum Type type() const override { return FUNC_ITEM; }
 + virtual enum Functype functype() const { return UNKNOWN_FUNC; }
 + virtual Item *get_arg(uint i) { return args[i]; }
 + virtual const Item *get_arg(uint i) const { return args[i]; }
 + void print(const THD *thd, String *str, enum_query_type query_type) const override
 + void print_op(const THD *thd, String *str, enum_query_type query_type) const
 +  void print_args(const THD *thd, String *str, uint from, enum_query_type query_type) const
}

Class Item_int_func {}
Class Item_bool_func{
  - bool m_created_by_in2exists
}

Class Item_cond{
  # List<Item> list
  # bool abort_on_null
  + Type type() const override { return COND_ITEM; }
  + void print(const THD *thd, String *str, enum_query_type query_type) const override;
}

Class Item_cond_and{
  + COND_EQUAL cond_equal
  + enum Functype functype() const override { return COND_AND_FUNC; }
  + const char *func_name() const override { return "and"; }
}

Class Item_cond_or {
  + enum Functype functype() const override { return COND_OR_FUNC; }
  + const char *func_name() const override { return "or"; }
}

Class Item_equal{
    - List<Item_field> fields
    - Item *m_const_arg
    - cmp_item *eval_item
    - Arg_comparator cmp
    - bool cond_false
    - bool compare_as_dates
    + Item *m_const_folding[2]
    + enum Functype functype() const override { return MULT_EQUAL_FUNC; }
    + const char *func_name() const override { return "multiple equal"; }
    + optimize_type select_optimize(const THD *) override { return OPTIMIZE_EQUAL; }
    + void print(const THD *thd, String *str, enum_query_type query_type) const override;
}

Class Item_bool_func2{
  # Arg_comparator cmp
  # bool abort_on_null
  + Item_result compare_type() const { return cmp.get_compare_type(); }
  + void print(const THD *thd, String *str,enum_query_type query_type) const override { Item_func::print_op(thd, str, query_type); }
}

Class Item_func_comparison {}
Class Item_eq_base{
  + Item_equal *source_multiple_equality
}

Class Item_func_equal {
  + enum Functype functype() const override { return EQUAL_FUNC; }
}

Class Item_func_eq {
  + enum Functype functype() const override { return EQ_FUNC; }
}

Parse_tree_node_tmpl <|-- Item
Item <|-- Item_result_field
Item_result_field <|-- Item_func
Item_func <|-- Item_int_func
Item_int_func <|-- Item_bool_func
Item_bool_func <|-- Item_cond
Item_cond <|-- Item_cond_and
Item_cond <|-- Item_cond_or
Item_bool_func <|-- Item_equal
Item_bool_func <|-- Item_bool_func2
Item_bool_func2 <|-- Item_func_comparison
Item_func_comparison <|-- Item_eq_base
Item_eq_base <|-- Item_func_eq
Item_eq_base <|-- Item_func_equal


class Item_field{
  + Table_ref *table_ref;
  + Field *field;

  - Field *result_field;
  - Field *last_org_destination_field;
  - Field *last_destination_field;
  - uint32_t last_org_destination_field_memcpyable;
  - uint32_t last_destination_field_memcpyable;
  - const Item_field *m_base_item_field;
  - bool m_protected_by_any_value;

  + Item_equal *item_equal;
  + uint16 field_index;
  + Item_equal *item_equal_all_join_nests;
  + bool no_constant_propagation;
  + uint have_privileges;
  + bool any_privileges;
  + bool can_use_prefix_key;
  + enum Type type() const override { return FIELD_ITEM; }
}
@enduml
