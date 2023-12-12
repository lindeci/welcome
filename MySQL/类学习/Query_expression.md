- [缩略版](#缩略版)
- [图解](#图解)
- [详细版](#详细版)

在MySQL中，一个`Query_expression`对象通常对应一个子查询。如果一个查询有多个子查询，那么会有多个`Query_expression`对象，每个对象对应一个子查询。每个`Query_expression`对象都有一个`Item_subselect *item`成员，这个成员是一个指向`Item_subselect`对象的指针，`Item_subselect`对象代表一个子查询。

所以，即使一个查询有多个子查询，每个`Query_expression`对象也只需要一个`Item_subselect *item`成员，因为每个`Query_expression`对象只处理一个子查询。

换句话说，`Query_expression`类的设计是为了处理单个子查询的情况。如果一个查询有多个子查询，那么会创建多个`Query_expression`对象，每个对象处理一个子查询。这样，每个`Query_expression`对象都可以通过它的`Item_subselect *item`成员来访问和操作它所关联的子查询。

# 缩略版
```cpp
class Query_expression {
  private:
    Query_expression *next;  // 下一个查询表达式
    Query_expression **prev;  // 前一个查询表达式的指针
    Query_block *master;  // 主查询块
    Query_block *slave;  // 从查询块
    Query_term *m_query_term;  // 查询项
    enum_parsing_context explain_marker;  // 解释标记
    bool prepared;  // 是否已准备好
    bool optimized;  // 是否已优化
    bool executed;  // 是否已执行
    Query_result *m_query_result;  // 查询结果
    unique_ptr_destroy_only m_root_iterator;  // 唯一的根迭代器
    AccessPath *m_root_access_path;  // 根访问路径
    Mem_root_array<MaterializePathParameters::QueryBlock> m_query_blocks_to_materialize;  // 需要实体化的查询块数组
  public:
    uint8 uncacheable;  // 不可缓存的标志
    Query_expression::enum_clean_state cleaned;  // 清理状态
  private:
    mem_root_deque<Item*> types;  // 类型队列
  public:
    ha_rows select_limit_cnt;  // 选择限制行数
    ha_rows offset_limit_cnt;  // 偏移限制行数
    Item_subselect *item;  // 子查询项
    ha_rows send_records;  // 发送记录数
}
```
# 图解
```sql
  select *
  from table1
     where table1.field IN (select * from table1_1_1 union
                            select * from table1_1_2)
     union
   select *
     from table2
     where table2.field=(select (select f1 from table2_1_1_1_1
                                   where table2_1_1_1_1.f2=table2_1_1.f3)
                           from table2_1_1
                           where table2_1_1.f1=table2.f2)
     union
   select * from table3;
 
   we will have following structure:
 
   select1: (select * from table1 ...)
   select2: (select * from table2 ...)
   select3: (select * from table3)
   select1.1.1: (select * from table1_1_1)
   ...
 
     main unit
     select1 select2 select3
     |^^     |^
    s|||     ||master
    l|||     |+---------------------------------+
    a|||     +---------------------------------+|
    v|||master                         slave   ||
    e||+-------------------------+             ||
     V|            neighbor      |             V|
     unit1.1<+==================>unit1.2       unit2.1
     select1.1.1 select 1.1.2    select1.2.1   select2.1.1
                                               |^
                                               ||
                                               V|
                                               unit2.1.1.1
                                               select2.1.1.1.1
 
 
   relation in main unit will be following:
   (bigger picture for:
      main unit
      select1 select2 select3
   in the above picture)
 
         main unit
         |^^^
         ||||
         ||||
         |||+------------------------------+
         ||+--------------+                |
    slave||master         |                |
         V|      neighbor |       neighbor |
         select1<========>select2<========>select3
 
    list of all query_block will be following (as it will be constructed by
    parser):
 
    select1->select2->select3->select2.1.1->select 2.1.2->select2.1.1.1.1-+
                                                                          |
    +---------------------------------------------------------------------+
    |
    +->select1.1.1->select1.1.2
```

# 详细版
```cpp
class Query_expression {
  private:
    Query_expression *next;  // 下一个查询表达式
    Query_expression **prev;  // 前一个查询表达式的指针
    Query_block *master;  // 主查询块
    Query_block *slave;  // 从查询块
    Query_term *m_query_term;  // 查询项
    enum_parsing_context explain_marker;  // 解释标记
    bool prepared;  // 是否已准备好
    bool optimized;  // 是否已优化
    bool executed;  // 是否已执行
    Query_result *m_query_result;  // 查询结果
    unique_ptr_destroy_only m_root_iterator;  // 唯一的根迭代器
    AccessPath *m_root_access_path;  // 根访问路径
    Mem_root_array<MaterializePathParameters::QueryBlock> m_query_blocks_to_materialize;  // 需要实体化的查询块数组
  public:
    uint8 uncacheable;  // 不可缓存的标志
    Query_expression::enum_clean_state cleaned;  // 清理状态
  private:
    mem_root_deque<Item*> types;  // 类型队列
  public:
    ha_rows select_limit_cnt;  // 选择限制行数
    ha_rows offset_limit_cnt;  // 偏移限制行数
    Item_subselect *item;  // 子查询项
    PT_with_clause *m_with_clause;  // WITH子句
    Table_ref *derived_table;  // 派生表
    Query_block *first_recursive;  // 第一个递归查询块
    table_map m_lateral_deps;  // 横向依赖表
    bool m_reject_multiple_rows;  // 拒绝多行
    ha_rows send_records;  // 发送记录数

    // 下面是成员函数，你可以继续添加注释
    // 获取查询项
    Query_term * query_term(void) const;
    // 设置查询项
    void set_query_term(Query_term *);
    // 获取集合操作
    Query_term_set_op * set_operation(void) const;
    // 返回非简单结果的查询块
    Query_block * non_simple_result_query_block(void) const;
    // 检查是否为叶子查询块
    bool is_leaf_block(Query_block *);
    // 查找与给定查询块相关联的查询项
    Query_term * find_blocks_query_term(const Query_block *) const;
    // 返回最后一个不同的查询块
    Query_block * last_distinct(void) const;
    // 检查是否具有顶层的不同项
    bool has_top_level_distinct(void) const;
    // 创建访问路径
    void create_access_paths(THD *);
    // 构造函数
    Query_expression(enum_parsing_context);
    // 检查是否为简单查询
    bool is_simple(void) const;
    // 获取全局参数
    Query_block * global_parameters(void) const;
    // 检查是否可合并
    bool is_mergeable(void) const;
    // 合并启发式
    bool merge_heuristic(const LEX *) const;
    // 获取外部查询块
    Query_block * outer_query_block(void) const;
    // 获取第一个查询块
    Query_block * first_query_block(void) const;
    // 获取下一个查询表达式
    Query_expression * next_query_expression(void) const;
    // 获取查询结果
    Query_result * query_result(void) const;
    // 获取根迭代器
    RowIterator * root_iterator(void) const;
    // 释放根迭代器
    unique_ptr_destroy_only release_root_iterator(void);
    // 获取根访问路径
    AccessPath * root_access_path(void) const;
    // 将访问路径更改为不使用IN子查询的方式
    void change_to_access_path_without_in2exists(THD *);
    // 清除根访问路径
    void clear_root_access_path();
    // 强制创建迭代器
    bool force_create_iterators(THD *);
    // 检查未完成的材料化
    bool unfinished_materialization(void) const;
    // 释放需要材料化的查询块数组
    Mem_root_array<MaterializePathParameters::QueryBlock> release_query_blocks_to_materialize(void);
    // 设置查询结果
    void set_query_result(Query_result *);
    // 检查是否可以直接材料化到结果
    bool can_materialize_directly_into_result(void) const;
    // 准备查询
    bool prepare(THD *, Query_result *, mem_root_deque<Item*> *, ulonglong, ulonglong);
    // 优化查询
    bool optimize(THD *, TABLE *, bool, bool);
    // 最终处理查询
    bool finalize(THD *);
    // 清除以便执行
    bool ClearForExecution(void);
    // 执行迭代器查询
    bool ExecuteIteratorQuery(THD *);
    // 执行查询
    bool execute(THD *);
    // 解释查询
    bool explain(THD *, const THD *);
    // 解释查询项
    bool explain_query_term(THD *, const THD *, Query_term *);
    // 清理
    void cleanup(bool);
    // 销毁
    void destroy(void);
    // 打印
    void print(const THD *, String *, enum_query_type);
    // 接受访问者
    bool accept(Select_lex_visitor *);
    // 创建后处理块
    Query_block * create_post_processing_block(Query_term_set_op *);
    // 准备查询项
    bool prepare_query_term(THD *, Query_term *, Query_result *, ulonglong, ulonglong, int, Mem_root_array<bool> &);
    // 设置为已准备
    void set_prepared(void);
    // 设置为已优化
    void set_optimized(void);
    // 设置为已执行
    void set_executed(void);
    // 重置为未执行
    void reset_executed(void);
    // 清除执行
    void clear_execution();
    // 检查是否已准备
    bool is_prepared(void) const;
    // 检查是否已优化
    bool is_optimized(void) const;
    // 检查是否已执行
    bool is_executed(void) const;
    // 更改查询结果
    bool change_query_result(THD *, Query_result_interceptor *, Query_result_interceptor *);
    // 设置限制
    bool set_limit(THD *, Query_block *);
    // 检查是否有任何限制
    bool has_any_limit(void) const;
    // 检查是否为联合查询
    bool is_union(void) const;
    // 检查是否为集合操作
    bool is_set_operation(void) const;
    // 包含下级
    void include_down(LEX *, Query_block *);
    // 排除级别
    void exclude_level(void);
    // 排除整个树
    void exclude_tree(void);
    // 重新编号选择
    void renumber_selects(LEX *);
    // 恢复命令属性
    void restore_cmd_properties(void);
    // 保存命令属性
    bool save_cmd_properties(THD *);
    // 获取单元列类型队列
    mem_root_deque<Item*> * get_unit_column_types(void);
    // 获取字段列表
    mem_root_deque<Item*> * get_field_list(void);
    // 可见字段数量
    size_t num_visible_fields(void) const;
    // 获取解释标记
    enum_parsing_context get_explain_marker(const THD *) const;
    // 设置解释标记
    void set_explain_marker(THD *, enum_parsing_context);
    // 从另一个查询表达式获取解释标记
    void set_explain_marker_from(THD *, const Query_expression *);
    // 断言未完全清理
    void assert_not_fully_clean(void);
    // 使无效
    void invalidate(void);
    // 检查是否为递归查询
    bool is_recursive(void) const;
    // 检查材料化的派生查询块
    bool check_materialized_derived_query_blocks(THD *);
    // 清除相关联的查询块
    bool clear_correlated_query_blocks(void);
    // 拉出后修复
    void fix_after_pullout(Query_block *, Query_block *);
    // 累积使用的表
    void accumulate_used_tables(table_map);
    // 查询位置
    enum_parsing_context place(void) const;
    // 遍历项目
    bool walk(Item_processor, enum_walk, uchar *);
    // 替换项目
    bool replace_items(Item_transformer, uchar *);
}
```