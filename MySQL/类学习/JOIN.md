- [explain](#explain)
- [JOIN](#join)
- [缩略版](#缩略版)
- [详细版](#详细版)
- [QEP\_shared](#qep_shared)
- [QEP\_shared\_owner](#qep_shared_owner)
- [JOIN\_TAB](#join_tab)
- [QEP\_TAB](#qep_tab)
- [join\_type](#join_type)


在MySQL源码中，`QEP_TAB`，`JOIN_TAB`和`QEP_shared`这三个类都是与查询执行计划（Query Execution Plan）相关的重要组成部分。

- `QEP_TAB`：全称是Query Execution Plan Table。这个“Table“可以是物理表、内存表、常量表、子查询的结果表等等。它是查询执行计划的一个节点，指定了对该节点指定的表的表访问操作，以及该节点与前一组计划节点结果的连接。

- `JOIN_TAB`：在MySQL的查询优化器中，`JOIN_TAB`数组是按照SQL中表的顺序初始化的，优化后的查询计划也保存在这个数组中。因此，我们只需要维护这个数组，就是维护查询计划树；求出多表连接的连接顺序就是求解执行计划树的具体形状。

- `QEP_shared`：`QEP_shared`是`JOIN_TAB`和`QEP_TAB`的父类，它持有`QEP_shared`的所有者。它包含了`JOIN_TAB`和`QEP_TAB`共享的成员。
# explain
1. **id**：查询的唯一标识。如果`EXPLAIN`的结果包括多个`id`值，则数字越大越先执行；而对于相同`id`的行，则表示从上往下依次执行。

2. **select_type**：查询类型，有如下几种取值：
    - `SIMPLE`：简单查询，不包含子查询或`UNION`。
    - `PRIMARY`：包含复杂的子查询，最外层查询标记为该值。
    - `SUBQUERY`：在`SELECT`或`WHERE`包含子查询，被标记为该值。
    - `DERIVED`：在`FROM`列表中包含的子查询被标记为该值，MySQL会递归执行这些子查询，把结果放在临时表。

4. **type**：连接类型，表示MySQL如何访问表中的数据。有如下几种取值：
    - `system`：该表只有一行（相当于系统表），`system`是`const`类型的特例。
    - `const`：针对主键或唯一索引的等值查询扫描, 最多只返回一行数据. `const`查询速度非常快, 因为它仅仅读取一次即可。
    - `eq_ref`：当使用了索引的全部组成部分，并且索引是`PRIMARY KEY`或`UNIQUE NOT NULL`才会使用该类型，性能仅次于`system`及`const`。
    - `ref`：当满足索引的最左前缀规则，或者索引不是主键也不是唯一索引时才会发生。如果使用的索引只会匹配到少量的行，性能也是不错的。
    - `fulltext`：全文索引。
    - `ref_or_null`：该类型类似于`ref`，但是MySQL会额外搜索哪些行包含了`NULL`。
    - `index_merge`：此类型表示使用了索引合并优化，表示一个查询里面用到了多个索引。
    - `unique_subquery`：该类型和`eq_ref`类似，但是使用了`IN`查询，且子查询是主键或者唯一索引。
    - `index_subquery`：和`unique_subquery`类似，只是子查询使用的是非唯一索引。
    - `range`：范围扫描，表示检索了指定范围的行，主要用于有限制的索引扫描。

# JOIN
# 缩略版
```cpp
class JOIN {
public:
    Query_block * const query_block;  // 查询块指针
    THD * const thd;  // THD对象指针
    JOIN_TAB *join_tab;  // JOIN_TAB指针
    QEP_TAB *qep_tab;  // QEP_TAB指针
    JOIN_TAB **best_ref;  // 最佳引用指针
    JOIN_TAB **map2table;  // 映射到表指针
    TABLE *sort_by_table;  // 按表排序
    Prealloced_array<JOIN::TemporaryTableToCleanup, 1> temp_tables;  // 临时表数组
    Prealloced_array<Filesort*, 1> filesorts_to_cleanup;  // 待清理的文件排序数组
    uint tables;  // 表数量
    uint primary_tables;  // 主要表数量
    uint const_tables;  // 常量表数量
    uint tmp_tables;  // 临时表数量
    uint send_group_parts;  // 发送组件部分
    bool streaming_aggregation;  // 流式聚合
    bool grouped;  // 已分组
    bool do_send_rows;  // 是否发送行
    table_map all_table_map;  // 所有表映射
    table_map const_table_map;  // 常量表映射
    table_map found_const_table_map;  // 已找到的常量表映射
    table_map deps_of_remaining_lateral_derived_tables;  // 剩余横向派生表的依赖
    ha_rows send_records;  // 发送记录数
    ha_rows found_records;  // 已找到的记录数
    ha_rows examined_rows;  // 检查的记录数
    ha_rows row_limit;  // 行限制
    ha_rows m_select_limit;  // SELECT限制
    ha_rows fetch_limit;  // 获取限制
    POSITION *best_positions;  // 最佳位置
    POSITION *positions;  // 位置
    Override_executor_func override_executor_func;  // 重写执行器函数
    double best_read;  // 最佳读取
    ha_rows best_rowcount;  // 最佳行数
    double sort_cost;  // 排序成本
    double windowing_cost;  // 窗口成本
    mem_root_deque<Item*> *fields;  // 字段数组指针
    List<Cached_item> group_fields;  // 分组字段列表
    List<Cached_item> group_fields_cache;  // 分组字段缓存列表
    List<Cached_item> semijoin_deduplication_fields;  // 半连接去重字段列表
    Item_sum **sum_funcs;  // 汇总函数数组
    Temp_table_param tmp_table_param;  // 临时表参数
    MYSQL_LOCK *lock;  // MySQL锁指针
    JOIN::RollupState rollup_state;  // 滚动状态
    bool implicit_grouping;  // 隐式分组
    bool select_distinct;  // 选择不同
    bool group_optimized_away;  // 分组优化消除
    bool simple_order;  // 简单排序
    bool simple_group;  // 简单分组
    enum : unsigned int {JOIN::ORDERED_INDEX_VOID, JOIN::ORDERED_INDEX_GROUP_BY, JOIN::ORDERED_INDEX_ORDER_BY} m_ordered_index_usage;  // 有序索引用途
    bool skip_sort_order;  // 跳过排序顺序
    bool need_tmp_before_win;  // 窗口前需要临时表
    bool has_lateral;  // 是否具有横向
    Key_use_array keyuse_array;  // 键使用数组
    mem_root_deque<Item*> *tmp_fields;  // 临时字段数组指针
    int error;  // 错误
    uint64_t hash_table_generation;  // 哈希表生成
    ORDER_with_src order;  // 排序
    ORDER_with_src group_list;  // 分组列表
    Prealloced_array<Item_rollup_group_item*, 4> rollup_group_items;  // 滚动分组项数组
    Prealloced_array<Item_rollup_sum_switcher*, 4> rollup_sums;  // 滚动汇总数组
    List<Window> m_windows;  // 窗口列表
    bool m_windows_sort;  // 窗口排序
    bool m_windowing_steps;  // 窗口步骤
    Explain_format_flags explain_flags;  // 解释格式标志
    Item *where_cond;  // WHERE条件
    Item *having_cond;  // HAVING条件
    Item *having_for_explain;  // 用于解释的HAVING条件
    Table_ref *tables_list;  // 表列表
    COND_EQUAL *cond_equal;  // 条件相等
    plan_idx return_tab;  // 返回表
    Ref_item_array *ref_items;  // 引用项数组
    uint current_ref_item_slice;  // 当前引用项切片
    uint recursive_iteration_count;  // 递归迭代计数
    const char *zero_result_cause;  // 零结果原因
    bool child_subquery_can_materialize;  // 子查询是否可物化
    bool allow_outer_refs;  // 允许外部引用
    List<TABLE> sj_tmp_tables;  // 半连接临时表列表
    List<Semijoin_mat_exec> sjm_exec_list;  // 半连接材料化执行列表
    bool group_sent;  // 分组已发送
    bool calc_found_rows;  // 计算已找到的行
    bool with_json_agg;  // 带有JSON_AGG
    bool needs_finalize;  // 需要最终处理

private:
    bool optimized;  // 已优化
    bool executed;  // 已执行
    JOIN::enum_plan_state plan_state;  // 计划状态

public:
    bool select_count;  // 选择计数

private:
    AccessPath *m_root_access_path;  // 根访问路径
    AccessPath *m_root_access_path_no_in2exists;  // 不包含IN子查询的根访问路径
}
```
# 详细版
```cpp
class JOIN {
public:
    Query_block * const query_block;  // 查询块指针
    THD * const thd;  // THD对象指针
    JOIN_TAB *join_tab;  // JOIN_TAB指针
    QEP_TAB *qep_tab;  // QEP_TAB指针
    JOIN_TAB **best_ref;  // 最佳引用指针
    JOIN_TAB **map2table;  // 映射到表指针
    TABLE *sort_by_table;  // 按表排序
    Prealloced_array<JOIN::TemporaryTableToCleanup, 1> temp_tables;  // 临时表数组
    Prealloced_array<Filesort*, 1> filesorts_to_cleanup;  // 待清理的文件排序数组
    uint tables;  // 表数量
    uint primary_tables;  // 主要表数量
    uint const_tables;  // 常量表数量
    uint tmp_tables;  // 临时表数量
    uint send_group_parts;  // 发送组件部分
    bool streaming_aggregation;  // 流式聚合
    bool grouped;  // 已分组
    bool do_send_rows;  // 是否发送行
    table_map all_table_map;  // 所有表映射
    table_map const_table_map;  // 常量表映射
    table_map found_const_table_map;  // 已找到的常量表映射
    table_map deps_of_remaining_lateral_derived_tables;  // 剩余横向派生表的依赖
    ha_rows send_records;  // 发送记录数
    ha_rows found_records;  // 已找到的记录数
    ha_rows examined_rows;  // 检查的记录数
    ha_rows row_limit;  // 行限制
    ha_rows m_select_limit;  // SELECT限制
    ha_rows fetch_limit;  // 获取限制
    POSITION *best_positions;  // 最佳位置
    POSITION *positions;  // 位置
    Override_executor_func override_executor_func;  // 重写执行器函数
    double best_read;  // 最佳读取
    ha_rows best_rowcount;  // 最佳行数
    double sort_cost;  // 排序成本
    double windowing_cost;  // 窗口成本
    mem_root_deque<Item*> *fields;  // 字段数组指针
    List<Cached_item> group_fields;  // 分组字段列表
    List<Cached_item> group_fields_cache;  // 分组字段缓存列表
    List<Cached_item> semijoin_deduplication_fields;  // 半连接去重字段列表
    Item_sum **sum_funcs;  // 汇总函数数组
    Temp_table_param tmp_table_param;  // 临时表参数
    MYSQL_LOCK *lock;  // MySQL锁指针
    JOIN::RollupState rollup_state;  // 滚动状态
    bool implicit_grouping;  // 隐式分组
    bool select_distinct;  // 选择不同
    bool group_optimized_away;  // 分组优化消除
    bool simple_order;  // 简单排序
    bool simple_group;  // 简单分组
    enum : unsigned int {JOIN::ORDERED_INDEX_VOID, JOIN::ORDERED_INDEX_GROUP_BY, JOIN::ORDERED_INDEX_ORDER_BY} m_ordered_index_usage;  // 有序索引用途
    bool skip_sort_order;  // 跳过排序顺序
    bool need_tmp_before_win;  // 窗口前需要临时表
    bool has_lateral;  // 是否具有横向
    Key_use_array keyuse_array;  // 键使用数组
    mem_root_deque<Item*> *tmp_fields;  // 临时字段数组指针
    int error;  // 错误
    uint64_t hash_table_generation;  // 哈希表生成
    ORDER_with_src order;  // 排序
    ORDER_with_src group_list;  // 分组列表
    Prealloced_array<Item_rollup_group_item*, 4> rollup_group_items;  // 滚动分组项数组
    Prealloced_array<Item_rollup_sum_switcher*, 4> rollup_sums;  // 滚动汇总数组
    List<Window> m_windows;  // 窗口列表
    bool m_windows_sort;  // 窗口排序
    bool m_windowing_steps;  // 窗口步骤
    Explain_format_flags explain_flags;  // 解释格式标志
    Item *where_cond;  // WHERE条件
    Item *having_cond;  // HAVING条件
    Item *having_for_explain;  // 用于解释的HAVING条件
    Table_ref *tables_list;  // 表列表
    COND_EQUAL *cond_equal;  // 条件相等
    plan_idx return_tab;  // 返回表
    Ref_item_array *ref_items;  // 引用项数组
    uint current_ref_item_slice;  // 当前引用项切片
    uint recursive_iteration_count;  // 递归迭代计数
    const char *zero_result_cause;  // 零结果原因
    bool child_subquery_can_materialize;  // 子查询是否可物化
    bool allow_outer_refs;  // 允许外部引用
    List<TABLE> sj_tmp_tables;  // 半连接临时表列表
    List<Semijoin_mat_exec> sjm_exec_list;  // 半连接材料化执行列表
    bool group_sent;  // 分组已发送
    bool calc_found_rows;  // 计算已找到的行
    bool with_json_agg;  // 带有JSON_AGG
    bool needs_finalize;  // 需要最终处理

private:
    bool optimized;  // 已优化
    bool executed;  // 已执行
    JOIN::enum_plan_state plan_state;  // 计划状态

public:
    bool select_count;  // 选择计数

private:
    AccessPath *m_root_access_path;  // 根访问路径
    AccessPath *m_root_access_path_no_in2exists;  // 不包含IN子查询的根访问路径

public:
    JOIN(THD *, Query_block *);  // 构造函数声明
    JOIN(const JOIN &);  // 拷贝构造函数声明
    JOIN & operator=(const JOIN &);  // 赋值运算符声明
    Query_expression * query_expression(void) const;  // 获取查询表达式指针
    bool plan_is_const(void) const;  // 计划是否为常量
    bool plan_is_single_table(void);  // 计划是否为单表
    bool contains_non_aggregated_fts(void) const;  // 是否包含未汇总的全文搜索
    bool optimize(bool);  // 优化函数
    void reset(void);  // 重置函数
    bool prepare_result(void);  // 准备结果函数
    void destroy(void);  // 销毁函数
    bool alloc_func_list(void);  // 分配函数列表
    bool make_sum_func_list(const mem_root_deque<Item*> &, bool, bool);  // 构造汇总函数列表
    void copy_ref_item_slice(uint, uint);  // 复制引用项切片
    void copy_ref_item_slice(Ref_item_array, Ref_item_array);  // 复制引用项切片
    bool alloc_ref_item_slice(THD *, int);  // 分配引用项切片
    void set_ref_item_slice(uint);  // 设置引用项切片
    uint get_ref_item_slice(void) const;  // 获取引用项切片
    mem_root_deque<Item*> * get_current_fields(void);  // 获取当前字段数组指针
    bool optimize_rollup(void);  // 优化滚动
    bool finalize_table_conditions(THD *);  // 最终化表条件
    void join_free(void);  // 加入释放函数
    void cleanup(void);  // 清理函数
    bool clear_fields(table_map *);  // 清除字段函数
    void restore_fields(table_map);  // 恢复字段函数

private:
    bool send_row_on_empty_set(void) const;  // 空集合发送行

public:
    bool generate_derived_keys(void);  // 生成派生键函数
    void finalize_derived_keys(void);  // 最终化派生键函数
    bool get_best_combination(void);  // 获取最佳组合函数
    bool attach_join_conditions(plan_idx);  // 附加连接条件

private:
    bool attach_join_condition_to_nest(plan_idx, plan_idx, Item *, bool);  // 附加连接条件至嵌套函数

public:
    bool update_equalities_for_sjm(void);  // 更新半连接等式函数
    bool add_sorting_to_table(uint, ORDER_with_src *, bool);  // 为表添加排序
    bool decide_subquery_strategy(void);  // 决定子查询策略函数
    void refine_best_rowcount(void);  // 优化最佳行数函数
    table_map calculate_deps_of_remaining_lateral_derived_tables(table_map, uint) const;  // 计算剩余横向派生表的依赖函数
    bool clear_sj_tmp_tables(void);  // 清除半连接临时表函数
    bool clear_corr_derived_tmp_tables(void);  // 清除相关派生临时表函数
    void clear_hash_tables(void);  // 清除哈希表函数
    void mark_const_table(JOIN_TAB *, Key_use *);  // 标记常量表函数
    JOIN::enum_plan_state get_plan_state(void) const;  // 获取计划状态函数
    bool is_optimized(void) const;  // 是否已优化函数
    void set_optimized(void);  // 设置已优化函数
    bool is_executed(void) const;  // 是否已执行函数
    void set_executed(void);  // 设置已执行函数
    const Cost_model_server * cost_model(void) const;  // 成本模型函数
    bool fts_index_access(JOIN_TAB *);  // 全文搜索索引访问函数
    QEP_TAB::enum_op_type get_end_select_func(void);  // 获取结束选择函数
    bool propagate_dependencies(void);  // 传播依赖函数
    bool push_to_engines(void);  // 推送至引擎函数
    AccessPath * root_access_path(void) const;  // 根访问路径函数
    void set_root_access_path(AccessPath *);  // 设置根访问路径函数
    void change_to_access_path_without_in2exists(void);  // 转换至不包含IN子查询的访问路径函数
    void refresh_base_slice(void);  // 刷新基本切片函数

private:
    bool create_intermediate_table(QEP_TAB *, const mem_root_deque<Item*> &, ORDER_with_src &, bool);  // 创建中间表函数
    void optimize_distinct(void);  // 优化去重函数
    bool optimize_fts_query(void);  // 优化全文搜索查询函数
    bool check_access_path_with_fts(void) const;  // 检查具有全文搜索的访问路径函数
    bool prune_table_partitions(void);  // 剪枝表分区函数
    void init_key_dependencies(void);  // 初始化键依赖函数
    void set_prefix_tables(void);  // 设置前缀表函数
    void cleanup_item_list(const mem_root_deque<Item*> &) const;  // 清理项目列表函数
    void set_semijoin_embedding(void);  // 设置半连接嵌入函数
    bool make_join_plan(void);
    bool init_planner_arrays(void);
    bool extract_const_tables(void);
    bool extract_func_dependent_tables(void);
    void update_sargable_from_const(SARGABLE_PARAM *);
    bool estimate_rowcount(void);
    void optimize_keyuse(void);
    void set_semijoin_info(void);
    void adjust_access_methods(void);
    void update_depend_map(void);
    void update_depend_map(ORDER *);
    void make_outerjoin_info(void);
    bool init_ref_access(void);
    bool alloc_qep(uint);
    void unplug_join_tabs(void);
    bool setup_semijoin_materialized_table(JOIN_TAB *, uint, POSITION *, POSITION *);
    bool add_having_as_tmp_table_cond(uint);
    bool make_tmp_tables_info(void);
    void set_plan_state(JOIN::enum_plan_state);
    bool compare_costs_of_subquery_strategies(Subquery_strategy *);
    ORDER * remove_const(ORDER *, Item *, bool, bool *, bool);
    int replace_index_subquery(void);
    bool optimize_distinct_group_order(void);
    void test_skip_sort(void);
    bool alloc_indirection_slices(void);
    void create_access_paths(void);
  public:
    AccessPath * create_access_paths_for_zero_rows(void) const;
  private:
    void create_access_paths_for_index_subquery(void);
    AccessPath * create_root_access_path_for_join(void);
    AccessPath * attach_access_paths_for_having_and_limit(AccessPath *) const;
    AccessPath * attach_access_path_for_update_or_delete(AccessPath *) const;

  public:
    typedef bool (*Override_executor_func)(JOIN *, Query_result *);
}
```
# QEP_shared
```cpp
class QEP_shared {
  private:
    JOIN *m_join;
    plan_idx m_idx;
    TABLE *m_table;
    POSITION *m_position;
    Semijoin_mat_exec *m_sj_mat_exec;
    plan_idx m_first_sj_inner;
    plan_idx m_last_sj_inner;
    plan_idx m_first_inner;
    plan_idx m_last_inner;
    plan_idx m_first_upper;
    Index_lookup m_ref;
    uint m_index;
    join_type m_type;
    Item *m_condition;
    bool m_condition_is_pushed_to_sort;
    Key_map m_keys;
    ha_rows m_records;
    AccessPath *m_range_scan;
    table_map prefix_tables_map;
    table_map added_tables_map;
    Item_func_match *m_ft_func;
    bool m_skip_records_in_range;
}
```
# QEP_shared_owner
```cpp
class QEP_shared_owner {
  protected:
    QEP_shared *m_qs;
}
```
# JOIN_TAB
```cpp
class JOIN_TAB : public QEP_shared_owner {
  public:
    Table_ref *table_ref;
  private:
    Key_use *m_keyuse;
    Item **m_join_cond_ref;
  public:
    COND_EQUAL *cond_equal;
    double worst_seeks;
    Key_map const_keys;
    Key_map checked_keys;
    Key_map skip_scan_keys;
    Key_map needed_reg;
    Key_map quick_order_tested;
    ha_rows found_records;
    double read_time;
    table_map dependent;
    table_map key_dependent;
    uint used_fieldlength;
    quick_type use_quick;
    uint m_use_join_cache;
    Table_ref *emb_sj_nest;
    nested_join_map embedding_map;
    uint join_cache_flags;
    bool reversed_access;
}
```
# QEP_TAB
```cpp
class QEP_TAB : public QEP_shared_owner {
  public:
    Table_ref *table_ref;
    SJ_TMP_TABLE *flush_weedout_table;
    SJ_TMP_TABLE *check_weed_out_table;
    plan_idx firstmatch_return;
    uint loosescan_key_len;
    plan_idx match_tab;
    bool rematerialize;
    QEP_TAB::Setup_func materialize_table;
    bool using_dynamic_range;
    bool needs_duplicate_removal;
    bool not_used_in_distinct;
    Item *having;
    QEP_TAB::enum_op_type op_type;
    Temp_table_param *tmp_table_param;
    Filesort *filesort;
    ORDER *filesort_pushed_order;
    uint ref_item_slice;
    Item *m_condition_optim;
    bool m_keyread_optim;
    bool m_reversed_access;
    qep_tab_map lateral_derived_tables_depend_on_me;
    Mem_root_array<AccessPath const*> *invalidators;
}
```

# join_type
```cpp
enum join_type : unsigned int 
{
    JT_UNKNOWN, 
    JT_SYSTEM, 
    JT_CONST, 
    JT_EQ_REF, 
    JT_REF, 
    JT_ALL, 
    JT_RANGE, 
    JT_INDEX_SCAN, 
    JT_FT, 
    JT_REF_OR_NULL, 
    JT_INDEX_MERGE
}
```