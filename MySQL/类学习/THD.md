```cpp
class THD : public MDL_context_owner, public Query_arena, public Open_tables_state {
  public:
    Thd_mem_cnt m_mem_cnt;  // THD内存统计
    MDL_context mdl_context;  // MDL上下文
    enum_mark_columns mark_used_columns;  // 用于标记已使用的列
    ulong want_privilege;  // 期望的特权
  private:
    std::unique_ptr<LEX, std::default_delete<LEX> > main_lex;  // 主要的LEX对象
  public:
    LEX *lex;  // LEX对象
  private:
    std::unique_ptr<dd::cache::Dictionary_client, std::default_delete<dd::cache::Dictionary_client> > m_dd_client;  // 字典客户端
    LEX_CSTRING m_query_string;  // 查询字符串
    String m_normalized_query;  // 标准化的查询字符串
    std::atomic<bool> m_safe_to_display;  // 安全显示标志
    LEX_CSTRING m_catalog;  // 目录
    LEX_CSTRING m_db;  // 数据库
    resourcegroups::Resource_group_ctx m_resource_group_ctx;  // 资源组上下文
    String m_rewritten_query;  // 重写后的查询字符串
  public:
    Relay_log_info *rli_fake;  // 虚拟的中继日志信息
    Relay_log_info *rli_slave;  // 从属中继日志信息
    bool tx_commit_pending;  // 事务提交挂起标志
    static const char * const DEFAULT_WHERE;  // 默认的WHERE子句
    NET_SERVER m_net_server_extension;  // 网络服务器扩展
    collation_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::unique_ptr<user_var_entry, void (*)(user_var_entry*)> > user_vars;  // 用户变量映射
    rand_struct rand;  // 随机数生成结构
    System_variables variables;  // 系统变量
    System_status_var status_var;  // 系统状态变量
    System_status_var *copy_status_var_ptr;  // 复制状态变量指针
    System_status_var *initial_status_var;  // 初始状态变量
    bool status_var_aggregated;  // 状态变量是否已汇总
    std::vector<char, std::allocator<char> > m_connection_attributes;  // 连接属性
    double m_current_query_cost;  // 当前查询成本
    ulonglong m_current_query_partial_plans;  // 当前查询的部分计划数
    THR_LOCK_INFO lock_info;  // 线程锁信息
    mysql_mutex_t LOCK_thd_data;  // THD数据锁
    mysql_mutex_t LOCK_thd_query;  // THD查询锁
    mysql_mutex_t LOCK_thd_sysvar;  // THD系统变量锁
    bool for_debug_only_is_set_persist_options;  // 仅用于调试的持久选项设置标志
    mysql_mutex_t LOCK_thd_protocol;  // THD协议锁
    mysql_mutex_t LOCK_thd_security_ctx;  // THD安全上下文锁
  private:
    mysql_mutex_t LOCK_query_plan;  // 查询计划锁
  public:
    Prepared_statement_map stmt_map;  // 准备语句映射
    const char *thread_stack;  // 线程堆栈
    Security_context m_main_security_ctx;  // 主要安全上下文
    Security_context *m_security_ctx;  // 安全上下文
    List<Security_context> m_view_ctx_list;  // 视图上下文列表
    bool m_disable_password_validation;  // 禁用密码验证标志
    std::unique_ptr<Protocol_text, std::default_delete<Protocol_text> > protocol_text;  // 文本协议
    std::unique_ptr<Protocol_binary, std::default_delete<Protocol_binary> > protocol_binary;  // 二进制协议
  private:
    Protocol *m_protocol;  // 协议
    SSL *m_SSL;  // SSL对象
  public:
    THD::Query_plan query_plan;  // 查询计划
  private:
    PSI_stage_key m_current_stage_key;  // 当前阶段键
    const char *m_proc_info;  // 过程信息
  public:
    const char *where;  // WHERE子句
    ulong max_client_packet_length;  // 最大客户端数据包长度
    collation_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::unique_ptr<Table_ref, My_free_deleter> > handler_tables_hash;  // 处理表哈希映射
    malloc_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, User_level_lock*, std::hash<std::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::equal_to<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > > ull_hash;  // 无锁哈希映射
    uint dbug_sentry;  // 调试哨兵
    bool is_killable;  // 是否可杀死
    mysql_mutex_t LOCK_current_cond;  // 当前条件锁
    std::atomic<mysql_mutex_t*> current_mutex;  // 当前互斥量
    std.atomic<mysql_cond_t*> current_cond;  // 当前条件变量
    mysql_cond_t COND_thr_lock;  // 线程锁条件变量
  private:
    bool m_is_low_level_commit_ordering_enabled;  // 低级别提交顺序是否启用
    enum_server_command m_command;  // 服务器命令
    bool m_is_admin_conn;  // 是否是管理员连接
  public:
    uint32 unmasked_server_id;  // 未屏蔽的服务器ID
    uint32 server_id;  // 服务器ID
    uint32 file_id;  // 文件ID
    uint16 peer_port;  // 对等端口
    timeval start_time;  // 启动时间
    timeval user_time;  // 用户时间
    ulonglong start_utime;  // 启动用户时间
  private:
    ulonglong m_lock_usec;  // 锁微秒
  public:
    thr_lock_type update_lock_default;  // 更新锁默认类型
    thr_lock_type insert_lock_default;  // 插入锁默认类型
    uint in_sub_stmt;  // 在子语句中
    uint fill_status_recursion_level;  // 填充状态递归级别
    uint fill_variables_recursion_level;  // 填充变量递归级别
  private:
    Prealloced_array<Ha_data, 15> ha_data;  // 预分配的Ha_data数组
  public:
    rpl_event_coordinates binlog_next_event_pos;  // 二进制日志下一个事件位置
    uchar *binlog_row_event_extra_data;  // 二进制日志行事件额外数据
    THD_timer_info *timer;  // THD计时器信息
    THD_timer_info *timer_cache;  // THD计时器缓存
  private:
    bool skip_readonly_check;  // 跳过只读检查
    bool skip_transaction_read_only_check;  // 跳过事务只读检查
    THD::binlog_filter_state m_binlog_filter_state;  // 二进制日志过滤器状态
    enum_binlog_format current_stmt_binlog_format;  // 当前语句的二进制日志格式
    uint32 binlog_unsafe_warning_flags;  // 二进制日志不安全警告标志
    uint binlog_table_maps;  // 二进制日志表映射
    List<char> *binlog_accessed_db_names;  // 访问的二进制日志数据库名列表
    const char *m_trans_log_file;  // 事务日志文件
    char *m_trans_fixed_log_file;  // 固定的事务日志文件
    my_off_t m_trans_end_pos;  // 事务结束位置
    NET net;  // 网络
    String packet;  // 数据包
    std::unique_ptr<Transaction_ctx, std::default_delete<Transaction_ctx> > m_transaction;  // 事务上下文
    THD::Attachable_trx *m_attachable_trx;  // 可附加的事务
  public:
    Global_read_lock global_read_lock;  // 全局读锁
    Vio *active_vio;  // 活动的VIO
    Vio *clone_vio;  // 克隆的VIO
    Item_change_list change_list;  // 项变更列表
    Query_arena *stmt_arena;  // 查询区域
    table_map table_map_for_update;  // 更新用的表映射
    bool arg_of_last_insert_id_function;  // 最后插入ID函数的参数
    ulonglong first_successful_insert_id_in_prev_stmt;  // 上一个语句中第一个成功的插入ID
    ulonglong first_successful_insert_id_in_prev_stmt_for_binlog;  // 用于二进制日志的上一个语句中第一个成功的插入ID
    ulonglong first_successful_insert_id_in_cur_stmt;  // 当前语句中第一个成功的插入ID
    bool stmt_depends_on_first_successful_insert_id_in_prev_stmt;  // 语句依赖于上一个语句中第一个成功的插入ID
    Discrete_intervals_list auto_inc_intervals_in_cur_stmt_for_binlog;  // 用于二进制日志的当前语句中的自增间隔列表
    Discrete_intervals_list auto_inc_intervals_forced;  // 强制的自增间隔列表
    ulonglong previous_found_rows;  // 前一次的找到行数
    ulonglong current_found_rows;  // 当前的找到行数
    bool is_operating_gtid_table_implicitly;  // 隐式操作GTID表
    bool is_operating_substatement_implicitly;  // 隐式操作子语句
  private:
    longlong m_row_count_func;  // 行数函数
  public:
    ha_rows num_truncated_fields;  // 截断字段数
  private:
    ha_rows m_sent_row_count;  // 发送的行数
    ha_rows m_examined_row_count;  // 检查的行数
    USER_CONN *m_user_connect;  // 用户连接
  public:
    const CHARSET_INFO *db_charset;  // 数据库字符集信息
    std::unique_ptr<PROFILING, std::default_delete<PROFILING> > profiling;  // 性能分析
    PSI_stage_progress *m_stage_progress_psi;  // 阶段进度PSI
    sql_digest_state *m_digest;  // SQL摘要状态
    unsigned char *m_token_array;  // 令牌数组
    sql_digest_state m_digest_state;  // SQL摘要状态
    PSI_statement_locker *m_statement_psi;  // 语句PSI锁
    PSI_statement_locker_state m_statement_state;  // 语句PSI锁状态
    PSI_transaction_locker *m_transaction_psi;  // 事务PSI锁
    PSI_transaction_locker_state m_transaction_state;  // 事务PSI锁状态
    PSI_idle_locker *m_idle_psi;  // 空闲PSI锁
    PSI_idle_locker_state m_idle_state;  // 空闲PSI锁状态
    bool m_server_idle;  // 服务器空闲
    query_id_t query_id;  // 查询ID
    ulong statement_id_counter;  // 语句ID计数器
    ulong rand_saved_seed1;  // 保存的随机数种子1
    ulong rand_saved_seed2;  // 保存的随机数种子2
    my_thread_t real_id;  // 真实ID
  private:
    my_thread_id m_thread_id;  // 线程ID
  public:
    uint tmp_table;  // 临时表
    uint server_status;  // 服务器状态
    uint open_options;  // 打开选项
    enum_thread_type system_thread;  // 系统线程类型
    enum_tx_isolation tx_isolation;  // 事务隔离级别
    bool tx_read_only;  // 事务只读标志
    int tx_priority;  // 事务优先级
    int thd_tx_priority;  // THD事务优先级
    enum_check_fields check_for_truncated_fields;  // 检查截断字段
    Prealloced_array<Binlog_user_var_event


```

# 完整版
```cpp

```