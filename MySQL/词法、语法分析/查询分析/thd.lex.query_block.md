- [分析的 SQL](#分析的-sql)
  - [断点](#断点)
  - [make\_cmd 前](#make_cmd-前)
  - [make\_cmd 后](#make_cmd-后)
  - [查看 thd-\>lex-\>query\_block-\>fields](#查看-thd-lex-query_block-fields)
  - [查看 thd-\>lex-\>query\_block-\>m\_table\_list](#查看-thd-lex-query_block-m_table_list)
  - [查看 thd-\>lex-\>query\_block-\>order\_list](#查看-thd-lex-query_block-order_list)
  - [查看 thd-\>lex-\>query\_block-\>group\_list](#查看-thd-lex-query_block-group_list)
  - [查看 thd-\>lex-\>query\_block-\>select\_limit](#查看-thd-lex-query_block-select_limit)
  - [查看 thd-\>lex-\>query\_block-\>offset\_limit](#查看-thd-lex-query_block-offset_limit)
  - [查看 thd-\>lex-\>query\_block-\>m\_where\_cond](#查看-thd-lex-query_block-m_where_cond)
  - [查看 thd-\>lex-\>query\_block-\>m\_having\_cond](#查看-thd-lex-query_block-m_having_cond)
  - [查看 thd-\>lex-\>unit](#查看-thd-lex-unit)
- [有子查询得 SQL 分析](#有子查询得-sql-分析)
  - [查看 thd-\>lex-\>unit](#查看-thd-lex-unit-1)
  - [查看 thd-\>lex-\>query\_block-\>fields](#查看-thd-lex-query_block-fields-1)
- [where 条件中有子查询](#where-条件中有子查询)
  - [查看 thd-\>lex-\>unit](#查看-thd-lex-unit-2)
  - [查看 thd-\>lex-\>query\_block-\>m\_where\_cond](#查看-thd-lex-query_block-m_where_cond-1)
    - [查看 thd-\>lex-\>query\_block-\>m\_where\_cond](#查看-thd-lex-query_block-m_where_cond-2)

# 分析的 SQL
```sql
select
    t1.id,t1.name,sum(t2.balance) as tot 
from user1 t1,user2  t2 
where 
    t1.id<9 and t1.id=t2.id
group by t1.id,name 
having tot>5 
order by t1.id,t1.name desc 
limit 2,3;
```
## 断点
```cpp
bool LEX::make_sql_cmd(Parse_tree_root *parse_tree) {
  if (!will_contextualize) return false;

  m_sql_cmd = parse_tree->make_cmd(thd);
  if (m_sql_cmd == nullptr) return true;

  assert(m_sql_cmd->sql_command_code() == sql_command);

  return false;
}
```

## make_cmd 前
```json
-exec p *thd->lex->query_block
$41 = {
  <Query_term> = {
    _vptr.Query_term = 0x557880910970 <vtable for Query_block+16>,
    m_parent = 0x0,
    m_setop_query_result = 0x0,
    m_owning_operand = false,
    m_result_table = 0x0,
    m_fields = 0x0,
    m_curr_id = 2408550287
  }, 
  members of Query_block:
  m_added_non_hidden_fields = 0,
  fields = {
    m_blocks = 0x0,
    m_begin_idx = 0,
    m_end_idx = 0,
    m_capacity = 0,
    m_root = 0x7f8aa4003a20,
    m_generation = 0
  },
  m_windows = {
    <base_list> = {
      first = 0x557880d66e30 <end_of_list>,
      last = 0x7f8aa4124968,
      elements = 0
    }, <No data fields>},
  ftfunc_list = 0x7f8aa4124988,
  ftfunc_list_alloc = {
    <base_list> = {
      first = 0x557880d66e30 <end_of_list>,
      last = 0x7f8aa4124988,
      elements = 0
    }, <No data fields>},
  row_value_list = 0x0,
  sj_nests = {
    m_blocks = 0x0,
    m_begin_idx = 0,
    m_end_idx = 0,
    m_capacity = 0,
    m_root = 0x7f8aa4003a20,
    m_generation = 0
  },
  m_table_list = {
    elements = 0,
    first = 0x0,
    next = 0x7f8aa41249e0
  },
  order_list = {
    elements = 0,
    first = 0x0,
    next = 0x7f8aa41249f8
  },
  order_list_ptrs = 0x0,
  group_list = {
    elements = 0,
    first = 0x0,
    next = 0x7f8aa4124a18
  },
  group_list_ptrs = 0x0,
  rollup_group_items = {
    m_psi_key = 0,
    m_inline_size = 0,
    {
      m_ext = {
        m_array_ptr = 0x0,
        m_alloced_size = 0,
        m_alloced_capacity = 0
      },
      m_buff = {0x0, 0x0, 0x0, 0x8f8f8f8f8f8f8f8f}
    }
  },
  rollup_sums = {
    m_psi_key = 0,
    m_inline_size = 0,
    {
      m_ext = {
        m_array_ptr = 0x0,
        m_alloced_size = 0,
        m_alloced_capacity = 0
      },
      m_buff = {0x0, 0x0, 0x0, 0x8f8f8f8f8f8f8f8f}
    }
  },
  opt_hints_qb = 0x0,
  db = 0x0,
  recursive_reference = 0x0,
  parent_lex = 0x7f8aa40046b0,
  select_list_tables = 0,
  outer_join = 0,
  context = {
    outer_context = 0x0,
    next_context = 0x0,
    table_list = 0x0,
    first_name_resolution_table = 0x0,
    last_name_resolution_table = 0x0,
    query_block = 0x7f8aa41248f8,
    view_error_handler = false,
    view_error_handler_arg = 0x0,
    resolve_in_select_list = true,
    security_ctx = 0x0
  },
  first_context = 0x7f8aa4124ab0,
  join = 0x0,
  m_table_nest = {
    m_blocks = 0x0,
    m_begin_idx = 0,
    m_end_idx = 0,
    m_capacity = 0,
    m_root = 0x7f8aa4003a20,
    m_generation = 0
  },
  m_current_table_nest = 0x7f8aa4124b10,
  embedding = 0x0,
  leaf_tables = 0x0,
  end_lateral_table = 0x0,
  select_limit = 0x0,
  offset_limit = 0x0,
  inner_sum_func_list = 0x0,
  base_ref_items = {
    m_array = 0x0,
    m_size = 0
  },
  select_number = 1,
  cond_value = Item::COND_UNDEF,
  having_value = Item::COND_UNDEF,
  parsing_place = CTX_NONE,
  in_sum_expr = 0,
  resolve_place = Query_block::RESOLVE_NONE,
  select_n_where_fields = 0,
  select_n_having_items = 0,
  saved_cond_count = 0,
  cond_count = 0,
  between_count = 0,
  max_equal_elems = 0,
  n_sum_items = 0,
  n_child_sum_items = 0,
  n_scalar_subqueries = 0,
  materialized_derived_table_count = 0,
  partitioned_table_count = 0,
  with_wild = 0,
  leaf_table_count = 0,
  derived_table_count = 0,
  table_func_count = 0,
  nest_level = 0,
  olap = UNSPECIFIED_OLAP_TYPE,
  condition_context = enum_condition_context::ANDS,
  is_table_value_constructor = false,
  linkage = UNSPECIFIED_TYPE,
  uncacheable = 0 '\000',
  first_execution = true,
  sj_pullout_done = false,
  m_was_implicitly_grouped = false,
  skip_local_transforms = false,
  is_item_list_lookup = false,
  having_fix_field = false,
  group_fix_field = false,
  with_sum_func = false,
  subquery_in_having = false,
  m_use_select_limit = false,
  m_internal_limit = false,
  exclude_from_table_unique_test = false,
  no_table_names_allowed = false,
  hidden_items_from_optimization = 0,
  sj_candidates = 0x0,
  hidden_order_field_count = 0,
  next = 0x0,
  master = 0x7f8aa4124810,
  slave = 0x0,
  link_next = 0x0,
  link_prev = 0x7f8aa4004728,
  m_query_result = 0x0,
  m_base_options = 0,
  m_active_options = 0,
  resolve_nest = 0x0,
  m_where_cond = 0x0,
  m_having_cond = 0x0,
  hidden_group_field_count = -1886417009,
  has_sj_nests = false,
  has_aj_nests = false,
  m_right_joins = false,
  allow_merge_derived = true,
  m_agg_func_used = false,
  m_json_agg_func_used = false,
  m_empty_query = false
}
```
## make_cmd 后
```json
-exec p *thd->lex->query_block
$42 = {
  <Query_term> = {
    _vptr.Query_term = 0x557880910970 <vtable for Query_block+16>,
    m_parent = 0x0,
    m_setop_query_result = 0x0,
    m_owning_operand = false,
    m_result_table = 0x0,
    m_fields = 0x0,
    m_curr_id = 2408550287
  }, 
  members of Query_block:
  m_added_non_hidden_fields = 0,
  fields = {
    m_blocks = 0x7f8aa4121be0,
    m_begin_idx = 64,
    m_end_idx = 67,
    m_capacity = 128,
    m_root = 0x7f8aa4003a20,
    m_generation = 4
  },
  m_windows = {
    <base_list> = {
      first = 0x557880d66e30 <end_of_list>,
      last = 0x7f8aa4124968,
      elements = 0
    }, <No data fields>},
  ftfunc_list = 0x7f8aa4124988,
  ftfunc_list_alloc = {
    <base_list> = {
      first = 0x557880d66e30 <end_of_list>,
      last = 0x7f8aa4124988,
      elements = 0
    }, <No data fields>},
  row_value_list = 0x0,
  sj_nests = {
    m_blocks = 0x0,
    m_begin_idx = 0,
    m_end_idx = 0,
    m_capacity = 0,
    m_root = 0x7f8aa4003a20,
    m_generation = 0
  },
  m_table_list = {
    elements = 2,
    first = 0x7f8aa4121fe8,
    next = 0x7f8aa4122a60
  },
  order_list = {
    elements = 2,
    first = 0x7f8aa4120e98,
    next = 0x7f8aa4121060
  },
  order_list_ptrs = 0x0,
  group_list = {
    elements = 2,
    first = 0x7f8aa41263f0,
    next = 0x7f8aa41265a0
  },
  group_list_ptrs = 0x0,
  rollup_group_items = {
    m_psi_key = 0,
    m_inline_size = 0,
    {
      m_ext = {
        m_array_ptr = 0x0,
        m_alloced_size = 0,
        m_alloced_capacity = 0
      },
      m_buff = {0x0, 0x0, 0x0, 0x8f8f8f8f8f8f8f8f}
    }
  },
  rollup_sums = {
    m_psi_key = 0,
    m_inline_size = 0,
    {
      m_ext = {
        m_array_ptr = 0x0,
        m_alloced_size = 0,
        m_alloced_capacity = 0
      },
      m_buff = {0x0, 0x0, 0x0, 0x8f8f8f8f8f8f8f8f}
    }
  },
  opt_hints_qb = 0x0,
  db = 0x0,
  recursive_reference = 0x0,
  parent_lex = 0x7f8aa40046b0,
  select_list_tables = 0,
  outer_join = 0,
  context = {
    outer_context = 0x0,
    next_context = 0x0,
    table_list = 0x7f8aa4121fe8,
    first_name_resolution_table = 0x7f8aa4121fe8,
    last_name_resolution_table = 0x0,
    query_block = 0x7f8aa41248f8,
    view_error_handler = false,
    view_error_handler_arg = 0x0,
    resolve_in_select_list = true,
    security_ctx = 0x0
  },
  first_context = 0x7f8aa4124ab0,
  join = 0x0,
  m_table_nest = {
    m_blocks = 0x7f8aa4122658,
    m_begin_idx = 62,
    m_end_idx = 64,
    m_capacity = 128,
    m_root = 0x7f8aa4003a20,
    m_generation = 2
  },
  m_current_table_nest = 0x7f8aa4124b10,
  embedding = 0x0,
  leaf_tables = 0x0,
  end_lateral_table = 0x0,
  select_limit = 0x7f8aa41211d0,
  offset_limit = 0x7f8aa41210f8,
  inner_sum_func_list = 0x0,
  base_ref_items = {
    m_array = 0x0,
    m_size = 0
  },
  select_number = 1,
  cond_value = Item::COND_UNDEF,
  having_value = Item::COND_UNDEF,
  parsing_place = CTX_NONE,
  in_sum_expr = 0,
  resolve_place = Query_block::RESOLVE_NONE,
  select_n_where_fields = 10,
  select_n_having_items = 15,
  saved_cond_count = 0,
  cond_count = 0,
  between_count = 0,
  max_equal_elems = 0,
  n_sum_items = 1,
  n_child_sum_items = 0,
  n_scalar_subqueries = 0,
  materialized_derived_table_count = 0,
  partitioned_table_count = 0,
  with_wild = 0,
  leaf_table_count = 0,
  derived_table_count = 0,
  table_func_count = 0,
  nest_level = 0,
  olap = UNSPECIFIED_OLAP_TYPE,
  condition_context = enum_condition_context::ANDS,
  is_table_value_constructor = false,
  linkage = UNSPECIFIED_TYPE,
  uncacheable = 0 '\000',
  first_execution = true,
  sj_pullout_done = false,
  m_was_implicitly_grouped = false,
  skip_local_transforms = false,
  is_item_list_lookup = false,
  having_fix_field = false,
  group_fix_field = false,
  with_sum_func = true,
  subquery_in_having = false,
  m_use_select_limit = false,
  m_internal_limit = false,
  exclude_from_table_unique_test = false,
  no_table_names_allowed = false,
  hidden_items_from_optimization = 0,
  sj_candidates = 0x0,
  hidden_order_field_count = 0,
  next = 0x0,
  master = 0x7f8aa4124810,
  slave = 0x0,
  link_next = 0x0,
  link_prev = 0x7f8aa4004728,
  m_query_result = 0x0,
  m_base_options = 0,
  m_active_options = 0,
  resolve_nest = 0x0,
  m_where_cond = 0x7f8aa41260a0,
  m_having_cond = 0x7f8aa416a710,
  hidden_group_field_count = -1886417009,
  has_sj_nests = false,
  has_aj_nests = false,
  m_right_joins = false,
  allow_merge_derived = true,
  m_agg_func_used = false,
  m_json_agg_func_used = false,
  m_empty_query = false
}
```
## 查看 thd->lex->query_block->fields
```
-exec p typeid(*thd->lex->query_block->fields[0]).__name
$53 = 0x55787e76f6e0 <typeinfo name for Item_field> "10Item_field"
-exec p ((Item_field*)(thd->lex->query_block->fields[0]))->item_name->m_str
$58 = 0x7f8aa4124ca8 "id"
```
```
-exec p typeid(*thd->lex->query_block->fields[1]).__name
$54 = 0x55787e76f6e0 <typeinfo name for Item_field> "10Item_field"
-exec p ((Item_field*)(thd->lex->query_block->fields[1]))->item_name->m_str
$59 = 0x7f8aa41252e0 "name"
```
```
-exec p typeid(*thd->lex->query_block->fields[2]).__name
$52 = 0x55787e7a3808 <typeinfo name for Item_sum_sum> "12Item_sum_sum"
-exec p ((Item_sum_sum*)(thd->lex->query_block->fields[2]))->item_name->m_str
$68 = 0x7f8aa4121bd8 "tot"
```
## 查看 thd->lex->query_block->m_table_list
```
-exec p typeid(thd->lex->query_block->m_table_list).__name
could not find typeinfo symbol for 'SQL_I_List<Table_ref>'

-exec p thd->lex->query_block->m_table_list->first->table_name
$74 = 0x7f8aa4125968 "user1"
```
```
-exec p thd->lex->query_block->m_table_list->first->next_name_resolution_table->table_name
$118 = 0x7f8aa4125ab8 "user2"
-exec p thd->lex->query_block->m_table_list->first->next_local->table_name
$119 = 0x7f8aa4125ab8 "user2"
-exec p thd->lex->query_block->m_table_list->first->next_global->table_name
$120 = 0x7f8aa4125ab8 "user2"
```

## 查看 thd->lex->query_block->order_list
```
-exec p typeid(thd->lex->query_block->order_list).__name
could not find typeinfo symbol for 'SQL_I_List<ORDER>'

-exec p thd->lex->query_block->order_list->first->item->item_name->m_str
$87 = 0x7f8aa4120d90 "id"
```
```
-exec p (*(ORDER*)((SQL_I_List<ORDER>)(thd->lex->query_block->order_list).first)).next->item->item_name->m_str
$102 = 0x7f8aa4120f50 "name"

-exec p thd->lex->query_block->order_list->first->next->item->item_name->m_str
$109 = 0x7f8aa4120f50 "name
```

## 查看 thd->lex->query_block->group_list
```
-exec p typeid(thd->lex->query_block->group_list).__name
could not find typeinfo symbol for 'SQL_I_List<ORDER>'
```
```
-exec p thd->lex->query_block->group_list->first->item->item_name->m_str
$124 = 0x7f8aa41262e8 "id"
```
```
-exec p thd->lex->query_block->group_list->first->next->item->item_name->m_str
$125 = 0x7f8aa4126490 "name"
```
## 查看 thd->lex->query_block->select_limit
```
-exec p *thd->lex->query_block->select_limit->item_name->m_str
$128 = 51 '3'
```

## 查看 thd->lex->query_block->offset_limit
```
-exec p *thd->lex->query_block->offset_limit->item_name->m_str
$129 = 50 '2'
```

## 查看 thd->lex->query_block->m_where_cond
```
-exec p typeid(*((List<Item>)(((Item_cond_and*)thd->lex->query_block->m_where_cond)->list))[0]).__name
$144 = 0x55787e775db8 <typeinfo name for Item_func_lt> "12Item_func_lt"
```
```
-exec p typeid(*((List<Item>)(((Item_cond_and*)thd->lex->query_block->m_where_cond)->list))[1]).__name
$145 = 0x55787e775e58 <typeinfo name for Item_func_eq> "12Item_func_eq"
```

## 查看 thd->lex->query_block->m_having_cond
```
-exec p typeid(*thd->lex->query_block->m_having_cond).__name
$152 = 0x55787e775df8 <typeinfo name for Item_func_gt> "12Item_func_gt"
```

## 查看 thd->lex->unit
```json
-exec p thd->lex->unit
$153 = (Query_expression *) 0x7f8aa4124810
-exec p *thd->lex->unit
$154 = {
  next = 0x0,
  prev = 0x0,
  master = 0x0,
  slave = 0x7f8aa41248f8,
  m_query_term = 0x7f8aa41248f8,
  explain_marker = CTX_NONE,
  prepared = false,
  optimized = false,
  executed = false,
  m_query_result = 0x0,
  m_root_iterator = std::unique_ptr<RowIterator> = {
    get() = 0x0
  },
  m_root_access_path = 0x0,
  m_operands = {
    <Mem_root_array_YY<MaterializePathParameters::Operand>> = {
      m_root = 0x0,
      m_array = 0x0,
      m_size = 0,
      m_capacity = 0
    }, <No data fields>},
  uncacheable = 0 '\000',
  cleaned = Query_expression::UC_DIRTY,
  types = {
    m_blocks = 0x0,
    m_begin_idx = 0,
    m_end_idx = 0,
    m_capacity = 0,
    m_root = 0x7f8aa4003a20,
    m_generation = 0
  },
  select_limit_cnt = 18446744073709551615,
  offset_limit_cnt = 0,
  item = 0x0,
  m_with_clause = 0x0,
  derived_table = 0x0,
  first_recursive = 0x0,
  m_lateral_deps = 0,
  m_reject_multiple_rows = false,
  send_records = 10344644715844964239
}
```
```
-exec p thd->lex->query_block
$155 = (Query_block *) 0x7f8aa41248f8
```
```
-exec p *thd->lex->unit->m_query_term
$156 = {
  _vptr.Query_term = 0x557880910970 <vtable for Query_block+16>,
  m_parent = 0x0,
  m_setop_query_result = 0x0,
  m_owning_operand = false,
  m_result_table = 0x0,
  m_fields = 0x0,
  m_curr_id = 2408550287
}
-exec p thd->lex->unit->m_query_term
$157 = (Query_term *) 0x7f8aa41248f8
```

# 有子查询得 SQL 分析
```sql
select (select now()) as begin from t;
```
## 查看 thd->lex->unit
```
-exec p thd->lex->unit
$159 = (Query_expression *) 0x7f8aa416a360
-exec p *thd->lex->unit
$160 = {
  next = 0x0,
  prev = 0x0,
  master = 0x0,
  slave = 0x7f8aa416a448,
  m_query_term = 0x7f8aa416a448,
  explain_marker = CTX_NONE,
  prepared = false,
  optimized = false,
  executed = false,
  m_query_result = 0x0,
  m_root_iterator = std::unique_ptr<RowIterator> = {
    get() = 0x0
  },
  m_root_access_path = 0x0,
  m_operands = {
    <Mem_root_array_YY<MaterializePathParameters::Operand>> = {
      m_root = 0x0,
      m_array = 0x0,
      m_size = 0,
      m_capacity = 0
    }, <No data fields>},
  uncacheable = 0 '\000',
  cleaned = Query_expression::UC_DIRTY,
  types = {
    m_blocks = 0x0,
    m_begin_idx = 0,
    m_end_idx = 0,
    m_capacity = 0,
    m_root = 0x7f8aa4003a20,
    m_generation = 0
  },
  select_limit_cnt = 18446744073709551615,
  offset_limit_cnt = 0,
  item = 0x0,
  m_with_clause = 0x0,
  derived_table = 0x0,
  first_recursive = 0x0,
  m_lateral_deps = 0,
  m_reject_multiple_rows = false,
  send_records = 10344644715844964239
}
```
## 查看 thd->lex->query_block->fields
```
-exec p typeid(*thd->lex->query_block->fields[0]).__name
$161 = 0x55787e79df50 <typeinfo name for Item_singlerow_subselect> "24Item_singlerow_subselect"
```
```
-exec p ((Item_field*)(thd->lex->query_block->fields[0]))->item_name->m_str
$162 = 0x7f8aa416d9a8 "begin"
```

# where 条件中有子查询
```sql
  select *
  from table1
     where table1.field IN (select * from table1_1_1 union
                            select * from table1_1_2);
```
## 查看 thd->lex->unit
```
-exec p thd->lex->unit
$166 = (Query_expression *) 0x7f8aa41247c0
```
```
-exec p *thd->lex->unit
$165 = {
  next = 0x0,
  prev = 0x0,
  master = 0x0,
  slave = 0x7f8aa41248a8,
  m_query_term = 0x7f8aa41248a8,
  explain_marker = CTX_NONE,
  prepared = false,
  optimized = false,
  executed = false,
  m_query_result = 0x0,
  m_root_iterator = std::unique_ptr<RowIterator> = {
    get() = 0x0
  },
  m_root_access_path = 0x0,
  m_operands = {
    <Mem_root_array_YY<MaterializePathParameters::Operand>> = {
      m_root = 0x0,
      m_array = 0x0,
      m_size = 0,
      m_capacity = 0
    }, <No data fields>},
  uncacheable = 0 '\000',
  cleaned = Query_expression::UC_DIRTY,
  types = {
    m_blocks = 0x0,
    m_begin_idx = 0,
    m_end_idx = 0,
    m_capacity = 0,
    m_root = 0x7f8aa4003a20,
    m_generation = 0
  },
  select_limit_cnt = 18446744073709551615,
  offset_limit_cnt = 0,
  item = 0x0,
  m_with_clause = 0x0,
  derived_table = 0x0,
  first_recursive = 0x0,
  m_lateral_deps = 0,
  m_reject_multiple_rows = false,
  send_records = 10344644715844964239
}
```

## 查看 thd->lex->query_block->m_where_cond
```json
-exec p ((Item_in_subselect*)thd->lex->query_block->m_where_cond)->m_query_expr
$172 = (Query_expression *) 0x7f8aa4121f98
```
```json
-exec p *((Item_in_subselect*)thd->lex->query_block->m_where_cond)->m_query_expr
$173 = {
  next = 0x0,
  prev = 0x7f8aa4124bd8,
  master = 0x7f8aa41248a8,
  slave = 0x7f8aa4122080,
  m_query_term = 0x7f8aa416bd40,
  explain_marker = CTX_WHERE,
  prepared = false,
  optimized = false,
  executed = false,
  m_query_result = 0x0,
  m_root_iterator = std::unique_ptr<RowIterator> = {
    get() = 0x0
  },
  m_root_access_path = 0x0,
  m_operands = {
    <Mem_root_array_YY<MaterializePathParameters::Operand>> = {
      m_root = 0x0,
      m_array = 0x0,
      m_size = 0,
      m_capacity = 0
    }, <No data fields>},
  uncacheable = 0 '\000',
  cleaned = Query_expression::UC_DIRTY,
  types = {
    m_blocks = 0x0,
    m_begin_idx = 0,
    m_end_idx = 0,
    m_capacity = 0,
    m_root = 0x7f8aa4003a20,
    m_generation = 0
  },
  select_limit_cnt = 18446744073709551615,
  offset_limit_cnt = 0,
  item = 0x7f8aa41264e8,
  m_with_clause = 0x0,
  derived_table = 0x0,
  first_recursive = 0x0,
  m_lateral_deps = 0,
  m_reject_multiple_rows = false,
  send_records = 10344644715844964239
}
```
### 查看 thd->lex->query_block->m_where_cond
```json
-exec p *((Item_in_subselect*)thd->lex->query_block->m_where_cond)->m_query_expr->prev
$178 = (Query_expression *) 0x7f8aa4121f98
-exec p ((Item_in_subselect*)thd->lex->query_block->m_where_cond)->m_query_expr->prev
$179 = (Query_expression **) 0x7f8aa4124bd8
```

```json
-exec p **((Item_in_subselect*)thd->lex->query_block->m_where_cond)->m_query_expr->prev
$177 = {
  next = 0x0,
  prev = 0x7f8aa4124bd8,
  master = 0x7f8aa41248a8,
  slave = 0x7f8aa4122080,
  m_query_term = 0x7f8aa416bd40,
  explain_marker = CTX_WHERE,
  prepared = false,
  optimized = false,
  executed = false,
  m_query_result = 0x0,
  m_root_iterator = std::unique_ptr<RowIterator> = {
    get() = 0x0
  },
  m_root_access_path = 0x0,
  m_operands = {
    <Mem_root_array_YY<MaterializePathParameters::Operand>> = {
      m_root = 0x0,
      m_array = 0x0,
      m_size = 0,
      m_capacity = 0
    }, <No data fields>},
  uncacheable = 0 '\000',
  cleaned = Query_expression::UC_DIRTY,
  types = {
    m_blocks = 0x0,
    m_begin_idx = 0,
    m_end_idx = 0,
    m_capacity = 0,
    m_root = 0x7f8aa4003a20,
    m_generation = 0
  },
  select_limit_cnt = 18446744073709551615,
  offset_limit_cnt = 0,
  item = 0x7f8aa41264e8,
  m_with_clause = 0x0,
  derived_table = 0x0,
  first_recursive = 0x0,
  m_lateral_deps = 0,
  m_reject_multiple_rows = false,
  send_records = 10344644715844964239
}
```

### 查看 thd->lex->query_block
  ……
  next = 0x0,
  master = 0x7f8aa41247c0,
  slave = 0x7f8aa4121f98,
  link_next = 0x0,
  link_prev = 0x7f8aa41223b8,
  ……