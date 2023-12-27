- [Table\_ref](#table_ref)
- [缩略版](#缩略版)
- [详细版](#详细版)

# Table_ref
# 缩略版
```cpp
class Table_ref {
  public:
    Table_ref *next_local; // 下一个本地表引用
    Table_ref *next_global; // 下一个全局表引用
    Table_ref **prev_global; // 全局表引用的前一个指针
    const char *db; // 数据库名称
    const char *table_name; // 表名
    const char *alias; // 表的别名
    LEX_CSTRING target_tablespace_name; // 目标表空间名称
    char *option; // 选项
    Opt_hints_table *opt_hints_table; // 表提示
    Opt_hints_qb *opt_hints_qb; // 查询块提示
  private:
    uint m_tableno; // 表编号
    table_map m_map; // 表映射
    Item *m_join_cond; // 连接条件
    bool m_is_sj_or_aj_nest; // 是否为自然连接或联接嵌套
  public:
    table_map sj_inner_tables; // 自然连接内部表
    Table_ref *natural_join; // 自然连接表
    bool is_natural_join; // 是否为自然连接
    List<String> *join_using_fields; // 使用字段的连接列表
    List<Natural_join_column> *join_columns; // 连接列列表
    bool is_join_columns_complete; // 连接列是否完整
    Table_ref *next_name_resolution_table; // 下一个名称解析表
    List<Index_hint> *index_hints; // 索引提示列表
    TABLE *table; // 表
    mysql::binlog::event::Table_id table_id; // 表ID
    Query_result_union *derived_result; // 派生结果
    Table_ref *correspondent_table; // 相应的表
    Table_function *table_function; // 表函数
    AccessPath *access_path_for_derived; // 派生的访问路径
  private:
    Query_expression *derived; // 派生
    Common_table_expr *m_common_table_expr; // 公共表达式
    const Create_col_name_list *m_derived_column_names; // 派生列名列表
  public:
    ST_SCHEMA_TABLE *schema_table; // 模式表
    Query_block *schema_query_block; // 模式查询块
    bool schema_table_reformed; // 模式表是否重组
    Query_block *query_block; // 查询块
  private:
    LEX *view; // 视图
  public:
    Field_translator *field_translation; // 字段翻译器
    Field_translator *field_translation_end; // 字段翻译器结束
    Table_ref *merge_underlying_list; // 合并底层列表
    mem_root_deque<Table_ref*> *view_tables; // 视图表列表
    Table_ref *belong_to_view; // 属于视图
    Table_ref *referencing_view; // 引用的视图
    Table_ref *parent_l; // 父表引用
    Security_context *security_ctx; // 安全上下文
    Security_context *view_sctx; // 视图安全上下文
    Table_ref *next_leaf; // 下一个叶子表引用
    Item *derived_where_cond; // 派生的 WHERE 条件
    Item *check_option; // 检查选项
    Item *replace_filter; // 替换过滤器
    LEX_STRING select_stmt; // SELECT 语句
    LEX_STRING source; // 源
    LEX_STRING timestamp; // 时间戳
    LEX_USER definer; // 定义者
    ulonglong updatable_view; // 可更新的视图
    ulonglong algorithm; // 算法
    ulonglong view_suid; // 视图 SUID
    ulonglong with_check; // WITH CHECK
  private:
    enum_view_algorithm effective_algorithm; // 有效算法
    Lock_descriptor m_lock_descriptor; // 锁描述符
  public:
    GRANT_INFO grant; // 授权信息
    bool outer_join; // 外连接
    bool join_order_swapped; // 连接顺序是否交换
    uint shared; // 共享
    size_t db_length; // 数据库名称长度
    size_t table_name_length; // 表名长度
  private:
    bool m_updatable; // 是否可更新
    bool m_insertable; // 是否可插入
    bool m_updated; // 是否已更新
    bool m_inserted; // 是否已插入
    bool m_deleted; // 是否已删除
    bool m_fulltext_searched; // 是否已进行全文搜索
  public:
    bool straight; // 直连
    bool updating; // 更新中
    bool ignore_leaves; // 忽略叶子节点
    table_map dep_tables; // 依赖表
    table_map join_cond_dep_tables; // 连接条件依赖表
    NESTED_JOIN *nested_join; // 嵌套连接
    Table_ref *embedding; // 嵌套表引用
    mem_root_deque<Table_ref*> *join_list; // 连接列表
    bool cacheable_table; // 可缓存的表
    enum_open_type open_type; // 打开类型
    bool contain_auto_increment; // 是否包含自增列
    bool check_option_processed; // 检查选项是否已处理
    bool replace_filter_processed; // 替换过滤器是否已处理
    dd::enum_table_type required_type; // 必需的表类型
    char timestamp_buffer[20]; // 时间戳缓冲区
    bool prelocking_placeholder; // 预锁定占位符
    enum : unsigned int {Table_ref::OPEN_NORMAL, Table_ref::OPEN_IF_EXISTS, Table_ref::OPEN_FOR_CREATE, Table_ref::OPEN_STUB} open_strategy; // 打开策略
    bool internal_tmp_table; // 内部临时表
    bool is_alias; // 是否为别名
    bool is_fqtn; // 是否为全限定表名
    bool m_was_scalar_subquery; // 是否为标量子查询
    View_creation_ctx *view_creation_ctx; // 视图创建上下文
    LEX_CSTRING view_client_cs_name; // 视图客户端字符集名称
    LEX_CSTRING view_connection_cl_name; // 视图连接字符集名称
    LEX_STRING view_body_utf8; // 视图主体（UTF-8）
    bool is_system_view; // 是否为系统视图
    bool is_dd_ctx_table; // 是否为数据字典上下文表
    List<Derived_key> derived_key_list; // 派生键列表
    uint8 trg_event_map; // 触发器事件映射
    bool schema_table_filled; // 模式表是否已填充
    MDL_request mdl_request; // MDL 请求
    bool view_no_explain; // 视图不解释
    List<String> *partition_names; // 分区名称列表
  private:
    Item *m_join_cond_optim; // 优化后的连接条件
  public:
    COND_EQUAL *cond_equal; // 相等条件
    bool optimized_away; // 是否已优化掉
    bool derived_keys_ready; // 派生键是否准备就绪
  private:
    bool m_is_recursive_reference; // 是否为递归引用
    enum_table_ref_type m_table_ref_type; // 表引用类型
    ulonglong m_table_ref_version; // 表引用版本
    Key_map covering_keys_saved; // 保存的覆盖键
    Key_map merge_keys_saved; // 保存的合并键
    Key_map keys_in_use_for_query_saved; // 保存的用于查询的键
    Key_map keys_in_use_for_group_by_saved; // 保存的用于 GROUP BY 的键
    Key_map keys_in_use_for_order_by_saved; // 保存的用于 ORDER BY 的键
    bool nullable_saved; // 保存的可空性
    bool force_index_saved; // 保存的强制索引
    bool force_index_order_saved; // 保存的强制索引顺序
    bool force_index_group_saved; // 保存的强制索引 GROUP
    MY_BITMAP lock_partitions_saved; // 保存的锁定分区
    MY_BITMAP read_set_saved; // 保存的读集
    MY_BITMAP write_set_saved; // 保存的写集
    MY_BITMAP read_set_internal_saved; // 保存的内部读集
}
```
# 详细版
```cpp
class Table_ref {
  public:
    Table_ref *next_local;
    Table_ref *next_global;
    Table_ref **prev_global;
    const char *db;
    const char *table_name;
    const char *alias;
    LEX_CSTRING target_tablespace_name;
    char *option;
    Opt_hints_table *opt_hints_table;
    Opt_hints_qb *opt_hints_qb;
  private:
    uint m_tableno;
    table_map m_map;
    Item *m_join_cond;
    bool m_is_sj_or_aj_nest;
  public:
    table_map sj_inner_tables;
    Table_ref *natural_join;
    bool is_natural_join;
    List<String> *join_using_fields;
    List<Natural_join_column> *join_columns;
    bool is_join_columns_complete;
    Table_ref *next_name_resolution_table;
    List<Index_hint> *index_hints;
    TABLE *table;
    mysql::binlog::event::Table_id table_id;
    Query_result_union *derived_result;
    Table_ref *correspondent_table;
    Table_function *table_function;
    AccessPath *access_path_for_derived;
  private:
    Query_expression *derived;
    Common_table_expr *m_common_table_expr;
    const Create_col_name_list *m_derived_column_names;
  public:
    ST_SCHEMA_TABLE *schema_table;
    Query_block *schema_query_block;
    bool schema_table_reformed;
    Query_block *query_block;
  private:
    LEX *view;
  public:
    Field_translator *field_translation;
    Field_translator *field_translation_end;
    Table_ref *merge_underlying_list;
    mem_root_deque<Table_ref*> *view_tables;
    Table_ref *belong_to_view;
    Table_ref *referencing_view;
    Table_ref *parent_l;
    Security_context *security_ctx;
    Security_context *view_sctx;
    Table_ref *next_leaf;
    Item *derived_where_cond;
    Item *check_option;
    Item *replace_filter;
    LEX_STRING select_stmt;
    LEX_STRING source;
    LEX_STRING timestamp;
    LEX_USER definer;
    ulonglong updatable_view;
    ulonglong algorithm;
    ulonglong view_suid;
    ulonglong with_check;
  private:
    enum_view_algorithm effective_algorithm;
    Lock_descriptor m_lock_descriptor;
  public:
    GRANT_INFO grant;
    bool outer_join;
    bool join_order_swapped;
    uint shared;
    size_t db_length;
    size_t table_name_length;
  private:
    bool m_updatable;
    bool m_insertable;
    bool m_updated;
    bool m_inserted;
    bool m_deleted;
    bool m_fulltext_searched;
  public:
    bool straight;
    bool updating;
    bool ignore_leaves;
    table_map dep_tables;
    table_map join_cond_dep_tables;
    NESTED_JOIN *nested_join;
    Table_ref *embedding;
    mem_root_deque<Table_ref*> *join_list;
    bool cacheable_table;
    enum_open_type open_type;
    bool contain_auto_increment;
    bool check_option_processed;
    bool replace_filter_processed;
    dd::enum_table_type required_type;
    char timestamp_buffer[20];
    bool prelocking_placeholder;
    enum : unsigned int {Table_ref::OPEN_NORMAL, Table_ref::OPEN_IF_EXISTS, Table_ref::OPEN_FOR_CREATE, Table_ref::OPEN_STUB} open_strategy;
    bool internal_tmp_table;
    bool is_alias;
    bool is_fqtn;
    bool m_was_scalar_subquery;
    View_creation_ctx *view_creation_ctx;
    LEX_CSTRING view_client_cs_name;
    LEX_CSTRING view_connection_cl_name;
    LEX_STRING view_body_utf8;
    bool is_system_view;
    bool is_dd_ctx_table;
    List<Derived_key> derived_key_list;
    uint8 trg_event_map;
    bool schema_table_filled;
    MDL_request mdl_request;
    bool view_no_explain;
    List<String> *partition_names;
  private:
    Item *m_join_cond_optim;
  public:
    COND_EQUAL *cond_equal;
    bool optimized_away;
    bool derived_keys_ready;
  private:
    bool m_is_recursive_reference;
    enum_table_ref_type m_table_ref_type;
    ulonglong m_table_ref_version;
    Key_map covering_keys_saved;
    Key_map merge_keys_saved;
    Key_map keys_in_use_for_query_saved;
    Key_map keys_in_use_for_group_by_saved;
    Key_map keys_in_use_for_order_by_saved;
    bool nullable_saved;
    bool force_index_saved;
    bool force_index_order_saved;
    bool force_index_group_saved;
    MY_BITMAP lock_partitions_saved;
    MY_BITMAP read_set_saved;
    MY_BITMAP write_set_saved;
    MY_BITMAP read_set_internal_saved;

  public:
    Table_ref(void);
    Table_ref(TABLE *);
    Table_ref(const char *, const char *, thr_lock_type);
    Table_ref(TABLE *, const char *, size_t, const char *, size_t, const char *, thr_lock_type);
    Table_ref(const char *, const char *, const char *, thr_lock_type);
    Table_ref(TABLE *, const char *);
    Table_ref(TABLE *, const char *, enum_mdl_type);
    Table_ref(const char *, const char *, thr_lock_type, enum_mdl_type);
    Table_ref(const char *, size_t, const char *, size_t, thr_lock_type, enum_mdl_type);
    Table_ref(const char *, size_t, const char *, size_t, thr_lock_type);
    Table_ref(const char *, size_t, const char *, size_t, const char *, enum_mdl_type);
    Table_ref(const char *, size_t, const char *, size_t, const char *, thr_lock_type, enum_mdl_type);
    Table_ref(const char *, size_t, const char *, size_t, const char *, thr_lock_type);
    static Table_ref * new_nested_join(MEM_ROOT *, const char *, Table_ref *, mem_root_deque<Table_ref*> *, Query_block *);
    Item ** join_cond_ref(void);
    Item * join_cond(void) const;
    void set_join_cond(Item *);
    Item * join_cond_optim(void) const;
    void set_join_cond_optim(Item *);
    Item ** join_cond_optim_ref(void);
    bool is_sj_nest(void) const;
    bool is_aj_nest(void) const;
    bool is_sj_or_aj_nest(void) const;
    void set_sj_or_aj_nest(void);
    bool merge_underlying_tables(Query_block *);
    void reset(void);
    int view_check_option(THD *) const;
    void print(const THD *, String *, enum_query_type) const;
    bool check_single_table(Table_ref **, table_map);
    bool set_insert_values(MEM_ROOT *);
    Table_ref * first_leaf_for_name_resolution(void);
    Table_ref * last_leaf_for_name_resolution(void);
    bool is_leaf_for_name_resolution(void) const;
    const Table_ref * top_table(void) const;
    Table_ref * top_table(void);
    bool prepare_check_option(THD *, bool);
    bool merge_where(THD *);
    bool prepare_replace_filter(THD *);
    bool is_view(void) const;
    bool is_derived(void) const;
    bool is_view_or_derived(void) const;
    bool is_table_function(void) const;
    bool is_recursive_reference(void) const;
    bool is_base_table(void) const;
    bool set_recursive_reference(void);
    bool is_internal(void) const;
    bool is_placeholder(void) const;
    bool is_mergeable(void) const;
    bool materializable_is_const(void) const;
    bool is_merged(void) const;
    void set_merged(void);
    bool uses_materialization(void) const;
    void set_uses_materialization(void);
    bool is_updatable(void) const;
    void set_updatable(void);
    bool is_insertable(void) const;
    void set_insertable(void);
    bool is_updated(void) const;
    void set_updated(void);
    bool is_inserted(void) const;
    void set_inserted(void);
    bool is_deleted(void) const;
    void set_deleted(void);
    void set_fulltext_searched(void);
    bool is_fulltext_searched(void) const;
    bool is_external(void) const;
    void set_readonly(void);
    bool is_multiple_tables(void) const;
    uint leaf_tables_count(void) const;
    Table_ref * first_leaf_table(void);
    Table_ref * any_outer_leaf_table(void);
    void set_view_query(LEX *);
    LEX * view_query(void) const;
    void set_derived_query_expression(Query_expression *);
    Query_expression * derived_query_expression(void) const;
    bool resolve_derived(THD *, bool);
    bool optimize_derived(THD *);
    bool create_materialized_table(THD *);
    bool materialize_derived(THD *);
    bool can_push_condition_to_derived(THD *);
    uint get_hidden_field_count_for_derived(void) const;
    bool prepare_security(THD *);
    Security_context * find_view_security_context(THD *);
    bool prepare_view_security_context(THD *);
    bool process_index_hints(const THD *, TABLE *);
    bool is_table_ref_id_equal(TABLE_SHARE *) const;
    void set_table_ref_id(TABLE_SHARE *);
    void set_table_ref_id(enum_table_ref_type, ulonglong);
    uint query_block_id(void) const;
    uint query_block_id_for_explain(void) const;
    const char * get_db_name(void) const;
    const char * get_table_name(void) const;
    int fetch_number_of_rows(ha_rows);
    bool update_derived_keys(THD *, Field *, Item **, uint, bool *);
    bool generate_keys(void);
    bool setup_materialized_derived(THD *);
    bool setup_materialized_derived_tmp_table(THD *);
    bool setup_table_function(THD *);
    bool create_field_translation(THD *);
    Table_ref * outer_join_nest(void) const;
    bool is_inner_table_of_outer_join(void) const;
    const Table_ref * updatable_base_table(void) const;
    Table_ref * updatable_base_table(void);
    void add_join_natural(Table_ref *);
    void set_privileges(ulong);
    bool save_properties(void);
    void restore_properties(void);
    void set_lock(const Lock_descriptor &);
    const Lock_descriptor & lock_descriptor(void) const;
    bool is_derived_unfinished_materialization(void) const;
    void set_tableno(uint);
    uint tableno(void) const;
    table_map map(void) const;
    Common_table_expr * common_table_expr(void) const;
    void set_common_table_expr(Common_table_expr *);
    const Create_col_name_list * derived_column_names(void) const;
    void set_derived_column_names(const Create_col_name_list *);
}
```

在MySQL源码中，TABLE和Table_ref这两个类都扮演着重要的角色。

TABLE：这个类主要用于表示数据库中的一个表。它包含了表的所有信息，如列的定义、索引的信息等12。在执行查询时，MySQL会为每个需要访问的表创建一个TABLE对象，然后通过这个对象来获取或修改表中的数据12。

Table_ref：这个类主要用于表示查询中的一个表引用3。在MySQL中，一个查询可能会涉及到多个表，这些表之间可能存在各种各样的关系，如连接、子查询等34。Table_ref类就是用来表示这些表引用的，它包含了表的名称、别名、锁类型等信息3。此外，Table_ref还有一些方法，可以用来获取或设置表引用的连接条件、优化后的连接条件等3。