```cpp
bool Query_block::prepare(THD *thd, mem_root_deque<Item *> *insert_field_list) {
  ……
  if (is_table_value_constructor) return prepare_values(thd);
  Query_expression *const unit = master_query_expression();
  if (!m_table_nest.empty()) propagate_nullability(&m_table_nest, false);
  allow_merge_derived = outer_query_block() == nullptr ||
                        master_query_expression()->item == nullptr ||
                        (outer_query_block()->outer_query_block() == nullptr
                             ? parent_lex->sql_command == SQLCOM_SELECT ||
                                   parent_lex->sql_command == SQLCOM_SET_OPTION
                             : outer_query_block()->allow_merge_derived);  
  const bool check_privs = !thd->derived_tables_processing ||
                           master_query_expression()->item != nullptr;
  ……
  is_item_list_lookup = false;
  if (setup_tables(thd, get_table_list(), false)) return true;
  ……
  is_item_list_lookup = true;
  ……
  if (leaf_table_count >= 2 &&
      setup_natural_join_row_types(thd, m_current_table_nest, &context))
    return true;

  Mem_root_array<Item_exists_subselect *> sj_candidates_local(thd->mem_root);
  set_sj_candidates(&sj_candidates_local);
  ……
  if (with_wild && setup_wild(thd)) return true;
  if (setup_base_ref_items(thd)) return true; /* purecov: inspected */

  if (setup_fields(thd, thd->want_privilege, /*allow_sum_func=*/true,
                   /*split_sum_funcs=*/true, /*column_update=*/false,
                   insert_field_list, &fields, base_ref_items))
    return true;
  ……
  if (setup_conds(thd)) return true;
  ……
  if (group_list.elements && setup_group(thd)) return true;
  ……
  // Setup the HAVING clause
  ……
  if (order_list.elements) {
    if (setup_order(thd, base_ref_items, get_table_list(), &fields,
                    order_list.first))
      return true;
  }
  ……
    if (remove_redundant_subquery_clauses(thd, hidden_group_field_count))
      return true;
  ……
  if (m_windows.elements != 0 &&
      Window::setup_windows1(thd, this, base_ref_items, get_table_list(),
                             &fields, &m_windows))
    return true;
  ……
  if (order_list.elements) {
    if (setup_order_final(thd)) return true; /* purecov: inspected */
    added_new_sum_funcs = true;
  }
  ……
  // Remove SELECT_DISTINCT options from a query block if can skip distinct.
  if (is_distinct() && can_skip_distinct())
    remove_base_options(SELECT_DISTINCT);
  ……
  if (!(thd->lex->context_analysis_only & CONTEXT_ANALYSIS_ONLY_VIEW) &&
      (thd->optimizer_switch_flag(OPTIMIZER_SWITCH_SUBQUERY_TO_DERIVED) ||
       (parent_lex->m_sql_cmd != nullptr &&
        thd->secondary_engine_optimization() ==
            Secondary_engine_optimization::SECONDARY)) &&
      transform_scalar_subqueries_to_join_with_derived(thd))
    return true; /* purecov: inspected */
  
  // Setup full-text functions after resolving HAVING
  if (has_ft_funcs()) {
   ……
    if (setup_ftfuncs(thd, this)) return true;
  }
  ……
  if (has_sj_candidates() && flatten_subqueries(thd)) return true;
  ……
    if (apply_local_transforms(thd, true)) return true;  // 这里包含  push_conditions_to_derived_tables
  ……
}
```