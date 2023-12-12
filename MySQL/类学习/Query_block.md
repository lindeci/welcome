- [缩略版](#缩略版)
- [详细版](#详细版)

# 缩略版
```cpp
class Query_block : public Query_term {  // 查询块类，继承自查询项类
public:
    size_t m_added_non_hidden_fields;  // 添加的非隐藏字段数量
    mem_root_deque<Item*> fields;  // 字段列表
    List<Window> m_windows;  // 窗口函数列表
    List<Item_func_match> *ftfunc_list;  // 全文检索函数列表指针
    List<Item_func_match> ftfunc_list_alloc;  // 分配的全文检索函数列表
    mem_root_deque<mem_root_deque<Item*>*> *row_value_list;  // 行值列表
    mem_root_deque<Table_ref*> sj_nests;  // 半连接嵌套表引用列表
    SQL_I_List<Table_ref> m_table_list;  // 表列表
    SQL_I_List<ORDER> order_list;  // 排序列表
    Group_list_ptrs *order_list_ptrs;  // 排序列表指针
    Opt_hints_qb *opt_hints_qb;  // 优化提示查询块
    char *db;  // 数据库名称
    LEX *parent_lex;  // 父级词法分析器
    table_map select_list_tables;  // 选择列表的表映射
    table_map outer_join;  // 外连接表映射
    Name_resolution_context context;  // 名称解析上下文
    Name_resolution_context *first_context;  // 第一个名称解析上下文
    JOIN *join;  // 连接
    mem_root_deque<Table_ref*> m_table_nest;  // 表嵌套列表
    mem_root_deque<Table_ref*> *m_current_table_nest;  // 当前表嵌套列表
    Table_ref *end_lateral_table;  // 结束的Lateral表
    Item *select_limit;  // 选择限制
    Item *offset_limit;  // 偏移限制
    Item::cond_result cond_value;  // 条件值
    Item::cond_result having_value;  // HAVING条件值
    uint select_n_where_fields;  // WHERE字段数量
    uint select_n_having_items;  // HAVING项数量
    uint saved_cond_count;  // 保存的条件计数
    uint cond_count;  // 条件计数
    uint between_count;  // BETWEEN计数
    enum_condition_context condition_context;  // 条件上下文
    sub_select_type linkage;  // 子查询类型
    bool subquery_in_having;  // HAVING中的子查询
    bool m_use_select_limit;  // 使用SELECT限制
    bool m_internal_limit;  // 内部限制
private:
    Query_block *next;  // 下一个查询块
    Query_expression *master;  // 主查询表达式
    Query_expression *slave;  // 从查询表达式
    Query_block *link_next;  // 下一个连接查询块
    Query_block **link_prev;  // 上一个连接查询块
    Query_result *m_query_result;  // 查询结果
public:
    Table_ref *resolve_nest;  // 解析嵌套
private:
    Item *m_where_cond;  // WHERE条件
    Item *m_having_cond;  // HAVING条件
    int hidden_group_field_count;  // 隐藏的分组字段数量
    bool has_sj_nests;  // 是否有半连接嵌套
    bool has_aj_nests;  // 是否有外连接嵌套
    bool m_right_joins;  // 右连接
    bool allow_merge_derived;  // 允许合并派生
    bool m_agg_func_used;  // 聚合函数已使用
    bool m_json_agg_func_used;  // JSON聚合函数已使用
    bool m_empty_query;  // 空查询
    static const char *type_str[13];  // 类型字符串数组
public:
    // 构造函数
    Query_block(MEM_ROOT *, Item *, Item *);
    ……
```

# 详细版
```cpp
class Query_block : public Query_term {  // 查询块类，继承自查询项类
public:
    size_t m_added_non_hidden_fields;  // 添加的非隐藏字段数量
    mem_root_deque<Item*> fields;  // 字段列表
    List<Window> m_windows;  // 窗口函数列表
    List<Item_func_match> *ftfunc_list;  // 全文检索函数列表指针
    List<Item_func_match> ftfunc_list_alloc;  // 分配的全文检索函数列表
    mem_root_deque<mem_root_deque<Item*>*> *row_value_list;  // 行值列表
    mem_root_deque<Table_ref*> sj_nests;  // 半连接嵌套表引用列表
    SQL_I_List<Table_ref> m_table_list;  // 表列表
    SQL_I_List<ORDER> order_list;  // 排序列表
    Group_list_ptrs *order_list_ptrs;  // 排序列表指针
    SQL_I_List<ORDER> group_list;  // 分组列表
    Group_list_ptrs *group_list_ptrs;  // 分组列表指针
    Prealloced_array<Item_rollup_group_item*, 4> rollup_group_items;  // Rollup分组项数组
    Prealloced_array<Item_rollup_sum_switcher*, 4> rollup_sums;  // Rollup求和开关数组
    Opt_hints_qb *opt_hints_qb;  // 优化提示查询块
    char *db;  // 数据库名称
    Table_ref *recursive_reference;  // 递归引用表
    LEX *parent_lex;  // 父级词法分析器
    table_map select_list_tables;  // 选择列表的表映射
    table_map outer_join;  // 外连接表映射
    Name_resolution_context context;  // 名称解析上下文
    Name_resolution_context *first_context;  // 第一个名称解析上下文
    JOIN *join;  // 连接
    mem_root_deque<Table_ref*> m_table_nest;  // 表嵌套列表
    mem_root_deque<Table_ref*> *m_current_table_nest;  // 当前表嵌套列表
    Table_ref *embedding;  // 嵌套表
    Table_ref *leaf_tables;  // 叶表
    Table_ref *end_lateral_table;  // 结束的Lateral表
    Item *select_limit;  // 选择限制
    Item *offset_limit;  // 偏移限制
    Item_sum *inner_sum_func_list;  // 内部求和函数列表
    Ref_item_array base_ref_items;  // 基础引用项数组
    uint select_number;  // 选择号码
    Item::cond_result cond_value;  // 条件值
    Item::cond_result having_value;  // HAVING条件值
    enum_parsing_context parsing_place;  // 解析位置
    uint in_sum_expr;  // SUM表达式中的IN数量
    Query_block::Resolve_place resolve_place;  // 查询块的解析位置
    uint select_n_where_fields;  // WHERE字段数量
    uint select_n_having_items;  // HAVING项数量
    uint saved_cond_count;  // 保存的条件计数
    uint cond_count;  // 条件计数
    uint between_count;  // BETWEEN计数
    uint max_equal_elems;  // 最大相等元素数量
    uint n_sum_items;  // SUM项数量
    uint n_child_sum_items;  // 子SUM项数量
    uint n_scalar_subqueries;  // 标量子查询数量
    uint materialized_derived_table_count;  // 材料化派生表数量
    uint partitioned_table_count;  // 分区表数量
    uint with_wild;  // 带通配符的数量
    uint leaf_table_count;  // 叶表数量
    uint derived_table_count;  // 派生表数量
    uint table_func_count;  // 表函数数量
    int nest_level;  // 嵌套级别
    olap_type olap;  // OLAP类型
    enum_condition_context condition_context;  // 条件上下文
    bool is_table_value_constructor;  // 是否是表值构造函数
    sub_select_type linkage;  // 子查询类型
    uint8 uncacheable;  // 无法缓存的
    bool first_execution;  // 第一次执行
    bool sj_pullout_done;  // 半连接拉出已完成
    bool m_was_implicitly_grouped;  // 是否是隐式分组
    bool skip_local_transforms;  // 跳过本地转换
    bool is_item_list_lookup;  // 是否是项列表查找
    bool having_fix_field;  // HAVING修复字段
    bool group_fix_field;  // 分组修复字段
    bool with_sum_func;  // 是否有SUM函数
    bool subquery_in_having;  // HAVING中的子查询
    bool m_use_select_limit;  // 使用SELECT限制
    bool m_internal_limit;  // 内部限制
    bool exclude_from_table_unique_test;  // 排除表唯一测试
    bool no_table_names_allowed;  // 不允许表名
    uint hidden_items_from_optimization;  // 优化隐藏项数量
private:
    Mem_root_array<Item_exists_subselect*> *sj_candidates;  // 半连接候选项
    int hidden_order_field_count;  // 隐藏的排序字段数量
    Query_block *next;  // 下一个查询块
    Query_expression *master;  // 主查询表达式
    Query_expression *slave;  // 从查询表达式
    Query_block *link_next;  // 下一个连接查询块
    Query_block **link_prev;  // 上一个连接查询块
    Query_result *m_query_result;  // 查询结果
    ulonglong m_base_options;  // 基础选项
    ulonglong m_active_options;  // 活动选项
public:
    Table_ref *resolve_nest;  // 解析嵌套
private:
    Item *m_where_cond;  // WHERE条件
    Item *m_having_cond;  // HAVING条件
    int hidden_group_field_count;  // 隐藏的分组字段数量
    bool has_sj_nests;  // 是否有半连接嵌套
    bool has_aj_nests;  // 是否有外连接嵌套
    bool m_right_joins;  // 右连接
    bool allow_merge_derived;  // 允许合并派生
    bool m_agg_func_used;  // 聚合函数已使用
    bool m_json_agg_func_used;  // JSON聚合函数已使用
    bool m_empty_query;  // 空查询
    static const char *type_str[13];  // 类型字符串数组
public:
    // 构造函数
    Query_block(MEM_ROOT *, Item *, Item *);
    // 调试打印
    virtual void debugPrint(int, std::ostringstream &) const;
    void qbPrint(int, std::ostringstream &) const;
    virtual Query_term_type term_type(void) const;
    virtual const char * operator_string(void) const;
    virtual Query_block * query_block(void) const;
    virtual void destroy_tree(void);
    virtual bool open_result_tables(THD *, int);
    // 吸收查询块的限制
    bool absorb_limit_of(Query_block *);
    // 获取WHERE条件
    Item * where_cond(void) const;
    Item ** where_cond_ref(void);
    void set_where_cond(Item *);
    // 获取HAVING条件
    Item * having_cond(void) const;
    Item ** having_cond_ref(void);
    void set_having_cond(Item *);
    // 设置查询结果
    void set_query_result(Query_result *);
    Query_result * query_result(void) const;
    // 改变查询结果
    bool change_query_result(THD *, Query_result_interceptor *, Query_result_interceptor *);
    // 设置基础选项
    void set_base_options(ulonglong);
    void add_base_options(ulonglong);
    void remove_base_options(ulonglong);
    void make_active_options(ulonglong, ulonglong);
    void add_active_options(ulonglong);
    ulonglong active_options(void) const;
    // 设置表为只读
    void set_tables_readonly(void);
    table_map all_tables_map(void) const;
    // 移除聚合函数
    bool remove_aggregates(THD *, Query_block *);
    Query_expression * master_query_expression(void) const;
    Query_expression * first_inner_query_expression(void) const;
    Query_block * outer_query_block(void) const;
    Query_block * next_query_block(void) const;
    Table_ref * find_table_by_name(const Table_ident *);
    Query_block * next_select_in_list(void) const;
    // 标记为依赖项
    void mark_as_dependent(Query_block *, bool);
    // 是否有表
    bool has_tables(void) const;
    // 是否是显式分组
    bool is_explicitly_grouped(void) const;
    // 是否是隐式分组
    bool is_implicitly_grouped(void) const;
    // 是否分组
    bool is_grouped(void) const;
    // 是否DISTINCT
    bool is_distinct(void) const;
    // 是否有排序
    bool is_ordered(void) const;
    bool can_skip_distinct(void) const;
    bool has_limit(void) const;
    bool has_ft_funcs(void) const;
    bool is_recursive(void) const;
    ORDER * find_in_group_list(Item *, int *) const;
    int group_list_size(void) const;
    bool has_windows(void) const;
    void invalidate(void);
    uint get_in_sum_expr(void) const;
    bool add_item_to_list(Item *);
    bool add_ftfunc_to_list(Item_func_match *);
    Table_ref * add_table_to_list(THD *, Table_ident *, const char *, ulong, thr_lock_type, enum_mdl_type, List<Index_hint> *, List<String> *, LEX_STRING *, Parse_context *);
    Item ** add_hidden_item(Item *);
    void remove_hidden_items(void);
    Table_ref * get_table_list(void) const;
    bool init_nested_join(THD *);
    Table_ref * end_nested_join(void);
    Table_ref * nest_last_join(THD *, size_t);
    bool add_joined_table(Table_ref *);
    mem_root_deque<Item*> * get_fields_list(void);
    VisibleFieldsContainer<mem_root_deque<Item*>, mem_root_deque<Item*>::Iterator<Item*> > visible_fields(void);
    VisibleFieldsContainer<mem_root_deque<Item*> const, mem_root_deque<Item*>::Iterator<Item* const> > visible_fields(void) const;
    bool check_view_privileges(THD *, ulong, ulong);
    bool check_column_privileges(THD *);
    bool check_privileges_for_subqueries(THD *);
    bool setup_tables(THD *, Table_ref *, bool);
    bool resolve_limits(THD *);
    bool resolve_placeholder_tables(THD *, bool);
    void propagate_unique_test_exclusion(void);
    void merge_contexts(Query_block *);
    bool merge_derived(THD *, Table_ref *);
    bool flatten_subqueries(THD *);
    void update_semijoin_strategies(THD *);
    Subquery_strategy subquery_strategy(const THD *) const;
    bool semijoin_enabled(const THD *) const;
    void set_sj_candidates(Mem_root_array<Item_exists_subselect*> *);
    void add_subquery_transform_candidate(Item_exists_subselect *);
    bool has_sj_candidates(void) const;
    bool has_subquery_transforms(void) const;
    bool add_ftfunc_list(List<Item_func_match> *);
    void set_lock_for_table(const Lock_descriptor &, Table_ref *);
    void set_lock_for_tables(thr_lock_type);
    void init_order(void);
    void cut_subtree(void);
    bool test_limit(void);
    ha_rows get_offset(const THD *) const;
    ha_rows get_limit(const THD *) const;
    bool set_context(Name_resolution_context *);
    bool setup_base_ref_items(THD *);
    void print(const THD *, String *, enum_query_type);
    void print_query_block(const THD *, String *, enum_query_type);
    void print_update(const THD *, String *, enum_query_type);
    void print_delete(const THD *, String *, enum_query_type);
    void print_insert(const THD *, String *, enum_query_type);
    void print_hints(const THD *, String *, enum_query_type);
    bool print_error(const THD *, String *);
    void print_select_options(String *);
    void print_update_options(String *);
    void print_delete_options(String *);
    void print_insert_options(String *);
    void print_table_references(const THD *, String *, Table_ref *, enum_query_type);
    void print_item_list(const THD *, String *, enum_query_type);
    void print_update_list(const THD *, String *, enum_query_type, const mem_root_deque<Item*> &, const mem_root_deque<Item*> &);
    void print_insert_fields(const THD *, String *, enum_query_type);
    void print_values(const THD *, String *, enum_query_type, const mem_root_deque<mem_root_deque<Item*>*> &, const char *);
    void print_from_clause(const THD *, String *, enum_query_type);
    void print_where_cond(const THD *, String *, enum_query_type);
    void print_group_by(const THD *, String *, enum_query_type);
    void print_having(const THD *, String *, enum_query_type);
    void print_windows(const THD *, String *, enum_query_type);
    ……
```