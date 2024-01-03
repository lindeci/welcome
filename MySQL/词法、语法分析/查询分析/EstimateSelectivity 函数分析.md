
```sql


```

```cpp
double EstimateSelectivity(THD *thd, Item *condition,
                           const CompanionSet &companion_set, string *trace) {
  // If the item is a true constant, we can say immediately whether it passes
  // or filters all rows. (Actually, calling get_filtering_effect() below
  // would crash if used_tables() is zero, which it is for const items.)
  if (condition->const_item()) {    //如果条件是常量，为真则返回1，为假则返回0
    return (condition->val_int() != 0) ? 1.0 : 0.0;
  }

  // For field = field (e.g. t1.x = t2.y), we try to use index
  // information or histograms to find a better selectivity estimate.
  // TODO(khatlen): Do the same for field <=> field?
  double selectivity_cap = 1.0;
  if (is_function_of_type(condition, Item_func::EQ_FUNC)) {
    Item_func_eq *eq = down_cast<Item_func_eq *>(condition);
    if (eq->source_multiple_equality != nullptr &&
        eq->source_multiple_equality->const_arg() == nullptr) {
      // To get consistent selectivities, we want all equalities that come from
      // the same multiple equality to use information from all of the tables.
      condition = eq->source_multiple_equality;
    } else {
      Item *left = eq->arguments()[0];
      Item *right = eq->arguments()[1];
      if (left->type() == Item::FIELD_ITEM &&
          right->type() == Item::FIELD_ITEM) {
        const Field *fields[] = {down_cast<Item_field *>(left)->field,
                                 down_cast<Item_field *>(right)->field};

        double selectivity = EstimateEqualPredicateSelectivity(
            EqualFieldArray(fields, array_elements(fields)), companion_set,
            trace);

        if (selectivity >= 0.0) {
          if (trace != nullptr) {
            *trace += StringPrintf(
                " - used an index or a histogram for %s, selectivity = %g\n",
                ItemToString(condition).c_str(), selectivity);
          }
          return selectivity;
        }
      } else if (left->type() == Item::FIELD_ITEM) {
        // field = <anything> (except field = field).
        //
        // See if we can derive an upper limit on selectivity from a unique
        // index on this field.
        selectivity_cap = std::min(
            selectivity_cap,
            FindSelectivityCap(*down_cast<Item_field *>(left)->field, trace));
      } else if (right->type() == Item::FIELD_ITEM) {
        // Same, for <anything> = field.
        selectivity_cap = std::min(
            selectivity_cap,
            FindSelectivityCap(*down_cast<Item_field *>(right)->field, trace));
      }
    }
  }

  // For multi-equalities, we do the same thing. This is maybe surprising;
  // one would think that there are more degrees of freedom with more joins.
  // However, given that we want the cardinality of the join ABC to be the
  // same no matter what the join order is and which predicates we select,
  // we can see that
  //
  //   |ABC| = |A| * |B| * |C| * S_ab * S_ac
  //   |ACB| = |A| * |C| * |B| * S_ac * S_bc
  //
  // (where S_ab means selectivity of joining A with B, etc.)
  // which immediately gives S_ab = S_bc, and similar equations give
  // S_ac = S_bc and so on.
  //
  // So all the selectivities in the multi-equality must be the same!
  // However, if you go to a database with real-world data, you will see that
  // they actually differ, despite the mathematics disagreeing.
  // The mystery, however, is resolved when we realize where we've made a
  // simplification; the _real_ cardinality is given by:
  //
  //   |ABC| = (|A| * |B| * S_ab) * |C| * S_{ab,c}
  //
  // The selectivity of joining AB with C is not the same as the selectivity
  // of joining B with C (since the correlation, which we do not model,
  // differs), but we've approximated the former by the latter. And when we do
  // this approximation, we also collapse all the degrees of freedom, and can
  // have only one selectivity.
  //
  // If we get more sophisticated cardinality estimation, e.g. by histograms
  // or the likes, we need to revisit this assumption, and potentially adjust
  // our model here.
  if (is_function_of_type(condition, Item_func::MULT_EQUAL_FUNC)) {
    Item_equal *equal = down_cast<Item_equal *>(condition);

    // These should have been expanded early, before we get here.
    assert(equal->const_arg() == nullptr);
    Prealloced_array<const Field *, 4> fields{PSI_NOT_INSTRUMENTED};
    for (const Item_field &item : equal->get_fields()) {
      fields.push_back(item.field);
    }

    double selectivity = EstimateEqualPredicateSelectivity(
        EqualFieldArray(&fields[0], fields.size()), companion_set, trace);

    if (selectivity >= 0.0) {
      if (trace != nullptr) {
        *trace += StringPrintf(
            " - used an index or a histogram for %s, selectivity = %g\n",
            ItemToString(condition).c_str(), selectivity);
      }
      return selectivity;
    }
  }

  // Neither index information nor histograms could help us, so use
  // Item::get_filtering_effect().
  //
  // There is a challenge in that the Item::get_filtering_effect() API
  // is intrinsically locked to the old join optimizer's way of thinking,
  // where one made a long chain of (left-deep) nested tables, and selectivity
  // estimation would be run for the entire WHERE condition at all points
  // in that chain. In such a situation, it would be necessary to know which
  // tables were already in the chain and which would not, and multiple
  // equalities would also be resolved through this mechanism. In the hypergraph
  // optimizer, we no longer have a chain, and always estimate selectivity for
  // applicable conditions only; thus, we need to fake that chain for the API.
  table_map used_tables = condition->used_tables() & ~PSEUDO_TABLE_BITS;
  table_map this_table = IsolateLowestBit(used_tables);
  MY_BITMAP empty;
  my_bitmap_map bitbuf[bitmap_buffer_size(MAX_FIELDS) / sizeof(my_bitmap_map)];
  bitmap_init(&empty, bitbuf, MAX_FIELDS);
  double selectivity = condition->get_filtering_effect(
      thd, this_table, used_tables & ~this_table,
      /*fields_to_ignore=*/&empty,
      /*rows_in_table=*/1000.0);

  selectivity = std::min(selectivity, selectivity_cap);
  if (trace != nullptr) {
    *trace += StringPrintf(" - fallback selectivity for %s = %g\n",
                           ItemToString(condition).c_str(), selectivity);
  }
  return selectivity;
}

```