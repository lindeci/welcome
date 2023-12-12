- [缩略版](#缩略版)
- [详细版](#详细版)

# 缩略版
```cpp
LEX : public Query_tables_list {
 public:
   Query_expression *unit;  // 查询树的根节点
   Query_block *query_block;    // 查询块
   Query_block *all_query_blocks_list;  // 所有查询块的列表
 private:
   Query_block *m_current_query_block;  // 当前查询块
 public:
   LEX_STRING name; // LEX_STRING结构体代表一个字符串
   Query_result *result;    // 查询结果
   THD *thd;    // 线程描述
   Table_ref *insert_table; // 插入表
   partition_info *part_info;   // 分区信息
   ulonglong bulk_insert_row_cnt;   // 批量插入行数
   List<set_var_base> var_list; // 变量列表
   List<Item_func_set_user_var> set_var_list;   // 设置变量列表
   List<Item_param> param_list; // 参数列表
 private:
   std::map<Item_field*, Field*, std::less<Item_field*>, std::allocator<std::pair<Item_field* const, Field*> > > *insert_update_values_map; // 插入更新值映射
 public:
   List<Name_resolution_context> context_stack; // 上下文堆栈
   KEY_CREATE_INFO key_create_info; // 键创建信息
   ulong type;// 类型
   Sql_cmd *m_sql_cmd;  // SQL命令
   bool expr_allows_subselect;  // 表达式允许子查询
   uint reparse_common_table_expr_at;   // 重新解析公共表表达式
   enum_duplicates duplicates;  // 重复
   enum_tx_isolation tx_isolation;  // 事务隔离级别
   enum_var_type option_type;   // 选项类型
   uint start_transaction_opt;  // 开始事务选项
   int select_number;   // 选择数量
   uint8 context_analysis_only; // 上下文分析
   bool drop_if_exists; // 存在则删除
   bool autocommit; // 自动提交
   enum_yes_no_unknown tx_chain;    // 事务链
   enum_yes_no_unknown tx_release;  // 事务释放
 public:
   st_parsing_options parsing_options;  // 解析选项
   Alter_info *alter_info;  // 修改信息
 private:
   bool m_broken;   // 损坏
   bool m_exec_started; // 执行开始
   bool m_exec_completed;   // 执行完成
 public:
   Explain_format *explain_format;  // 解释格式
   ulong max_execution_time;     // 最大执行时间
   bool will_contextualize; // 将上下文化
   dd::info_schema::Table_statistics m_IS_table_stats;  // 信息SCHEMA表统计
   dd::info_schema::Tablespace_statistics m_IS_tablespace_stats;    // 信息SCHEMA表空间统计

 public:
   LEX(void);
   Query_block * current_query_block(void) const;   // 构造函数
   void assert_ok_set_current_query_block(void);    // 当前查询块
   void set_current_query_block(Query_block *); // 确认设置当前查询块
   bool locate_var_assignment(const Name_string &); // 定位变量赋值
   void insert_values_map(Item_field *, Field *);   // 插入值映射
   void cleanup(bool);  // 清理
   bool is_exec_started(void) const;    // 执行开始
   void set_exec_started(void); // 设置执行开始
   void reset_exec_started(void);   // 重置执行开始
   bool is_exec_completed(void) const;  // 执行完成
   void set_exec_completed(void);   // 设置执行完成
   bool is_metadata_used(void) const;   // 元数据使用
   ~LEX();  // 析构函数
   void destroy(void);  // 销毁
   void reset(void);    // 重置
   Query_block * new_empty_query_block(void);   // 新建空查询块
   Query_block * new_query(Query_block *);  // 新查询
   Query_block * new_set_operation_query(Query_block *);    // 新建集操作查询
   bool new_top_level_query(void);  // 新建顶级查询
   void new_static_query(Query_expression *, Query_block *);    // 新建静态查询
   Query_expression * create_query_expr_and_block(THD *, Query_block *, Item *, Item *, enum_parsing_context);  // 创建查询表达式和块
   void clear_execution(void);  // 清除执行
   bool push_context(Name_resolution_context *);    // 压入上下文
   void pop_context(void);  // 弹出上下文
   bool is_single_level_stmt(void); // 是单级语句
   bool make_sql_cmd(Parse_tree_root *);    // 使sql命令
}
```
# 详细版
```cpp
LEX : public Query_tables_list {
 public:
   Query_expression *unit;  // 查询树的根节点
   Query_block *query_block;    // 查询块
   Query_block *all_query_blocks_list;  // 所有查询块的列表
 private:
   Query_block *m_current_query_block;  // 当前查询块
 public:
   bool is_explain_analyze; // 是否是EXPLAIN语句
   bool using_hypergraph_optimizer; // 是否使用超图优化器
   LEX_STRING name; // LEX_STRING结构体代表一个字符串
   char *help_arg;  // help_arg参数表示帮助信息
   char *to_log;    // to_log参数表示日志信息
   const char *x509_subject;    // x509_subject参数表示X509证书的主题
   const char *x509_issuer; // x509_issuer参数表示X509证书的颁发者
   const char *ssl_cipher;  // ssl_cipher参数表示SSL加密算法
   String *wild;    // 通配符
   Query_result *result;    // 查询结果
   LEX_STRING binlog_stmt_arg;  // binlog语句参数
   LEX_STRING ident;    // 标识符
   LEX_USER *grant_user;    // 授权用户
   LEX_ALTER alter_password;    // 修改密码
   enum_alter_user_attribute alter_user_attribute;  // 修改用户属性
   LEX_STRING alter_user_comment_text;   // 修改用户注释文本
   LEX_GRANT_AS grant_as;   // 授权为
   THD *thd;    // 线程描述
   Opt_hints_global *opt_hints_global;  // 全局提示
   Plugins_array plugins;   // 插件数组
   Table_ref *insert_table; // 插入表
   Table_ref *insert_table_leaf;    // 插入表叶子
   LEX_STRING create_view_query_block;  // 创建视图查询块
   partition_info *part_info;   // 分区信息
   LEX_USER *definer;   // 定义者
   List<LEX_USER> users_list;   // 用户列表
   List<LEX_COLUMN> columns;    // 列列表
   List<MYSQL_LEX_CSTRING> dynamic_privileges;  // 动态权限
   List<LEX_USER> *default_roles;   // 默认角色
   ulonglong bulk_insert_row_cnt;   // 批量插入行数
   List<Item> purge_value_list; // 清除值列表
   List<Item> kill_value_list;  // 终止值列表
   List<set_var_base> var_list; // 变量列表
   List<Item_func_set_user_var> set_var_list;   // 设置变量列表
   List<Item_param> param_list; // 参数列表
 private:
   std::map<Item_field*, Field*, std::less<Item_field*>, std::allocator<std::pair<Item_field* const, Field*> > > *insert_update_values_map; // 插入更新值映射
 public:
   List<Name_resolution_context> context_stack; // 上下文堆栈
   Item_sum *in_sum_func;   // 在sum函数中
   udf_func udf;    // UDF函数
   HA_CHECK_OPT check_opt;  // 检查选项
   HA_CREATE_INFO *create_info; // 创建信息
   KEY_CREATE_INFO key_create_info; // 键创建信息
   LEX_MASTER_INFO mi;  // 主信息
   LEX_SLAVE_CONNECTION slave_connection;   // 从连接
   Server_options server_options;   // 服务选项
   USER_RESOURCES mqh;  // 用户资源
   LEX_RESET_SLAVE reset_slave_info;    // 重置从信息
   ulong type;// 类型
   nesting_map allow_sum_func;  // 允许sum函数
   nesting_map m_deny_window_func;  // 禁止window函数
   bool m_subquery_to_derived_is_impossible;
   Sql_cmd *m_sql_cmd;  // SQL命令
   bool expr_allows_subselect;  // 表达式允许子查询
   uint reparse_common_table_expr_at;   // 重新解析公共表表达式
   bool reparse_derived_table_condition;
   std::vector<unsigned int, std::allocator<unsigned int> > reparse_derived_table_params_at;
   SSL_type ssl_type;   // SSL类型
   enum_duplicates duplicates;  // 重复
   enum_tx_isolation tx_isolation;  // 事务隔离级别
   enum_var_type option_type;   // 选项类型
   enum_view_create_mode create_view_mode;  // 创建视图模式
   my_thread_id show_profile_query_id;  // 显示简介查询ID
   uint profile_options;    // 简介选项
   uint grant;  // 授权
   uint grant_tot_col;  // 授权总列
   bool grant_privilege;    // 授权权限
   uint slave_thd_opt;  // 从线程选项
   uint start_transaction_opt;  // 开始事务选项
   int select_number;   // 选择数量
   uint8 create_view_algorithm; // 创建视图算法
   uint8 create_view_check; // 创建视图检查
   uint8 context_analysis_only; // 上下文分析
   bool drop_if_exists; // 存在则删除
   bool grant_if_exists;    // 存在则授权
   bool ignore_unknown_user;    // 忽略未知用户
   bool drop_temporary; // 删除临时
   bool autocommit; // 自动提交
   bool verbose;    // 详细
   bool no_write_to_binlog; // 不写入二进制日志
   bool m_extended_show;    // 扩展显示
   enum_yes_no_unknown tx_chain;    // 事务链
   enum_yes_no_unknown tx_release;  // 事务释放
   bool safe_to_cache_query;    // 安全缓存查询
 private:
   bool m_has_udf;  // 有UDF
   bool ignore; // 忽略
 public:
   st_parsing_options parsing_options;  // 解析选项
   Alter_info *alter_info;  // 修改信息
   LEX_CSTRING prepared_stmt_name;  // prepare语句名
   LEX_STRING prepared_stmt_code;   // prepare语句代码
   bool prepared_stmt_code_is_varref;   // prepare语句代码为变量引用
   List<MYSQL_LEX_STRING> prepared_stmt_params; // prepare语句参数
   sp_head *sphead; // 存储过程头
   sp_name *spname; // 存储过程名
   bool sp_lex_in_use;  // SP lex正在使用
   bool all_privileges; // 所有特权
   bool contains_plaintext_password;    // 包含明文密码
   enum_keep_diagnostics keep_diagnostics;  // 保持诊断
   uint32 next_binlog_file_nr;  // 下一个binlog文件号
 private:
   bool m_broken;   // 损坏
   bool m_exec_started; // 执行开始
   bool m_exec_completed;   // 执行完成
   sp_pcontext *sp_current_parsing_ctx; // SP当前解析上下文
   ulonglong m_statement_options;   // 语句选项
 public:
   st_sp_chistics sp_chistics;  // SP特征
   Event_parse_data *event_parse_data;  // 事件解析数据
   bool only_view;  // 仅视图
   uint8 create_view_suid;  // 创建视图suid
   const char *stmt_definition_begin;   // 语句定义开始
   const char *stmt_definition_end; // 语句定义结束
   bool use_only_table_context; // 仅使用表上下文
   bool is_lex_started; // lex开始
   bool in_update_value_clause; // 在更新值子句中
   Explain_format *explain_format;  // 解释格式
   ulong max_execution_time;     // 最大执行时间
   bool binlog_need_explicit_defaults_ts;   // binlog需要显式默认值时间戳
   bool will_contextualize; // 将上下文化
   dd::info_schema::Table_statistics m_IS_table_stats;  // 信息SCHEMA表统计
   dd::info_schema::Tablespace_statistics m_IS_tablespace_stats;    // 信息SCHEMA表空间统计
 private:
   Secondary_engine_execution_context *m_secondary_engine_context;  // 第二引擎执行上下文
   bool m_is_replication_deprecated_syntax_used;    // 使用了废弃的复制语法
   bool m_was_replication_command_executed; // 执行了复制命令
   bool rewrite_required;   // 需要重写

 public:
   LEX(void);
   Query_block * current_query_block(void) const;   // 构造函数
   void assert_ok_set_current_query_block(void);    // 当前查询块
   void set_current_query_block(Query_block *); // 确认设置当前查询块
   bool is_explain(void) const; // 是否为EXPLAIN
   bool locate_var_assignment(const Name_string &); // 定位变量赋值
   void insert_values_map(Item_field *, Field *);   // 插入值映射
   void destroy_values_map(void);   // 销毁值映射
   void clear_values_map(void); // 清空值映射
   bool has_values_map(void) const; // 有值映射
   std::map<Item_field*, Field*, std::less<Item_field*>, std::allocator<std::pair<Item_field* const, Field*> > >::iterator begin_values_map(void);  // 值映射开始
   std::map<Item_field*, Field*, std::less<Item_field*>, std::allocator<std::pair<Item_field* const, Field*> > >::iterator end_values_map(void);    // 值映射结束
   bool is_ignore(void) const;  // 是否忽略
   void set_ignore(bool);   // 设置忽略
   void set_has_udf(void);  // 设置有UDF
   bool has_udf(void) const;    // 有UDF
   ulonglong statement_options(void);   // 语句选项
   void add_statement_options(ulonglong);   // 添加语句选项
   bool is_broken(void) const;  // 是否损坏
   void mark_broken(bool);  // 标记损坏
   bool check_preparation_invalid(THD *);   // 检查准备无效
   void cleanup(bool);  // 清理
   bool is_exec_started(void) const;    // 执行开始
   void set_exec_started(void); // 设置执行开始
   void reset_exec_started(void);   // 重置执行开始
   bool is_exec_completed(void) const;  // 执行完成
   void set_exec_completed(void);   // 设置执行完成
   sp_pcontext * get_sp_current_parsing_ctx(void);  // 获取SP当前解析上下文
   void set_sp_current_parsing_ctx(sp_pcontext *);  // 设置SP当前解析上下文
   bool is_metadata_used(void) const;   // 元数据使用
   ~LEX();  // 析构函数
   void destroy(void);  // 销毁
   void reset(void);    // 重置
   Query_block * new_empty_query_block(void);   // 新建空查询块
   Query_block * new_query(Query_block *);  // 新查询
   Query_block * new_set_operation_query(Query_block *);    // 新建集操作查询
   bool new_top_level_query(void);  // 新建顶级查询
   void new_static_query(Query_expression *, Query_block *);    // 新建静态查询
   Query_expression * create_query_expr_and_block(THD *, Query_block *, Item *, Item *, enum_parsing_context);  // 创建查询表达式和块
   bool is_ps_or_view_context_analysis(void);   // 是PS或视图上下文分析
   bool is_view_context_analysis(void); // 是视图上下文分析
   void clear_execution(void);  // 清除执行
   void set_uncacheable(Query_block *, uint8);  // 设置不可缓存
   void set_trg_event_type_for_tables(void);    // 设置表触发器事件类型
   Table_ref * unlink_first_table(bool *);  // 取消链接第一个表
   void link_first_table_back(Table_ref *, bool);   // 链接回第一个表
   void first_lists_tables_same(void);  // 第一个列表表相同
   void restore_cmd_properties(void);   // 恢复命令属性
   void restore_properties_for_insert(void);    // 恢复插入属性
   bool save_cmd_properties(THD *); // 保存命令属性
   bool can_use_merged(void);   // 可使用合并
   bool can_not_use_merged(void);   // 不可使用合并
   bool need_correct_ident(void);   // 需要正确标识
   bool which_check_option_applicable(void);    // 哪个check选项适用
   void cleanup_after_one_table_open(void); // 一个表打开后清理
   bool push_context(Name_resolution_context *);    // 压入上下文
   void pop_context(void);  // 弹出上下文
   bool copy_db_to(const char **, size_t *) const;  // 复制数据库到
   bool copy_db_to(char **, size_t *) const;    // 复制数据库到
   Name_resolution_context * current_context(void); // 当前上下文
   void reset_n_backup_query_tables_list(Query_tables_list *);  // 重置和备份查询表列表
   void restore_backup_query_tables_list(Query_tables_list *);  // 恢复备份查询表列表
   bool table_or_sp_used(void); // 使用表或存储过程
   bool is_single_level_stmt(void); // 是单级语句
   void release_plugins(void);  // 释放插件
   bool accept(Select_lex_visitor *);   // 接受访问者
   bool set_wild(LEX_STRING);   // 设置通配符
   void clear_privileges(void); // 清除权限
   bool make_sql_cmd(Parse_tree_root *);    // 使sql命令
   Secondary_engine_execution_context * secondary_engine_execution_context(void) const; // 第二引擎执行上下文
   void set_secondary_engine_execution_context(Secondary_engine_execution_context *);   // 设置第二引擎执行上下文
   bool is_replication_deprecated_syntax_used(void);    // 使用了废弃的复制语法
   void set_replication_deprecated_syntax_used(void);   // 设置使用了废弃的复制语法
   bool was_replication_command_executed(void) const;   // 执行了复制命令
   void set_was_replication_command_executed(void); // 设置执行了复制命令
   bool set_channel_name(LEX_CSTRING);  // 设置通道名
   void set_rewrite_required(void); // 设置需要重写
   void reset_rewrite_required(void);   // 重置需要重写
   bool is_rewrite_required(void);  // 需要重写

   typedef Prealloced_array<st_plugin_int**, 16> Plugins_array; // 插件数组类型定义
}
```