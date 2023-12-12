
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
# 断点
```cpp
bool LEX::make_sql_cmd(Parse_tree_root *parse_tree) {
  if (!will_contextualize) return false;

  m_sql_cmd = parse_tree->make_cmd(thd);
  if (m_sql_cmd == nullptr) return true;

  assert(m_sql_cmd->sql_command_code() == sql_command);

  return false;
}
```

# make_cmd 前
```json
-exec p *thd->lex->unit
$38 = {
  next = 0x0,
  prev = 0x0,
  master = 0x0,
  slave = 0x7f8aa416a558,
  m_query_term = 0x7f8aa416a558,
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
# make_cmd 后
```json
-exec p *thd->lex->unit
$39 = {
  next = 0x0,
  prev = 0x0,
  master = 0x0,
  slave = 0x7f8aa416a558,
  m_query_term = 0x7f8aa416a558,
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
前后没变化