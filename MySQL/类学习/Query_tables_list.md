- [Query\_tables\_list](#query_tables_list)

# Query_tables_list
```cpp
class Query_tables_list {
public:
    enum_sql_command sql_command; // SQL 命令类型。
    Table_ref *query_tables; // 查询表列表。
    Table_ref **query_tables_last; // 查询表列表的最后一个元素。
    Table_ref **query_tables_own_last; // 查询表列表中属于自己的最后一个元素。
    std::unique_ptr<malloc_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, Sroutine_hash_entry*, std::hash<std::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::equal_to<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > > > sroutines; // 存储过程列表。
    SQL_I_List<Sroutine_hash_entry> sroutines_list; // 存储过程列表。
    Sroutine_hash_entry **sroutines_list_own_last; // 存储过程列表中属于自己的最后一个元素。
    uint sroutines_list_own_elements; // 存储过程列表中属于自己的元素个数。
    Query_tables_list::enum_lock_tables_state lock_tables_state; // 锁表状态。
    uint table_count; // 查询表个数。
    static const int BINLOG_STMT_UNSAFE_ALL_FLAGS; // 二进制日志语句不安全的所有标志位。
    static const int binlog_stmt_unsafe_errcode[26]; // 二进制日志语句不安全的错误代码列表。
private:
    uint32 binlog_stmt_flags; // 二进制日志语句标志位。
    uint32 stmt_accessed_table_flag; // 语句访问的表标志位。
    bool using_match; // 是否使用 MATCH 语句。
    bool stmt_unsafe_with_mixed_mode; // 在混合模式下语句是否不安全。

public:
    Query_tables_list & operator=(Query_tables_list &&); // 移动赋值运算符。
    bool is_query_tables_locked(void) const; // 判断查询表是否被锁定。
    Query_tables_list(void); // 构造函数。
    ~Query_tables_list(); // 析构函数。
    void reset_query_tables_list(bool); // 重置查询表列表。
    void destroy_query_tables_list(void); // 销毁查询表列表。
    void set_query_tables_list(Query_tables_list *); // 设置查询表列表。
    void add_to_query_tables(Table_ref *); // 添加到查询表列表。
    bool requires_prelocking(void); // 判断是否需要预锁定。
    void mark_as_requiring_prelocking(Table_ref **); // 标记为需要预锁定。
    Table_ref * first_not_own_table(void); // 获取第一个不属于自己的查询表。
    void chop_off_not_own_tables(void); // 移除不属于自己的查询表。
    bool is_stmt_unsafe(void) const; // 判断语句是否不安全。
    bool is_stmt_unsafe(Query_tables_list::enum_binlog_stmt_unsafe); // 判断语句是否不安全。
    void set_stmt_unsafe(Query_tables_list::enum_binlog_stmt_unsafe); // 设置语句为不安全。
    void set_stmt_unsafe_flags(uint32); // 设置二进制日志语句标志位。
    uint32 get_stmt_unsafe_flags(void) const; // 获取二进制日志语句标志位。
    bool is_stmt_row_injection(void) const; // 判断语句是否包含行注入。
    void set_stmt_row_injection(void); // 设置语句包含行注入。
    static const char * stmt_accessed_table_string(Query_tables_list::enum_stmt_accessed_table); // 获取语句访问的表字符串。
    void set_stmt_accessed_table(Query_tables_list::enum_stmt_accessed_table); // 设置语句访问的表。
    ……
}
```