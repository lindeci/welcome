- [Item\_field](#item_field)
- [Item\_ident](#item_ident)
- [Item](#item)

# Item_field
```cpp
class Item_field : public Item_ident {
  public:
    Table_ref *table_ref; /**< 表引用 */
    Field *field; /**< 字段 */

  private:
    Field *result_field; /**< 结果字段 */
    Field *last_org_destination_field; /**< 最后的原始目标字段 */
    Field *last_destination_field; /**< 最后的目标字段 */
    uint32_t last_org_destination_field_memcpyable; /**< 最后的原始目标字段是否可复制 */
    uint32_t last_destination_field_memcpyable; /**< 最后的目标字段是否可复制 */
    const Item_field *m_base_item_field; /**< 基本 Item_field */
    bool m_protected_by_any_value; /**< 受到任何值保护的标志 */

  public:
    Item_equal *item_equal; /**< 相等项 */
    uint16 field_index; /**< 字段索引 */
    Item_equal *item_equal_all_join_nests; /**< 所有连接嵌套的相等项 */
    bool no_constant_propagation; /**< 不进行常量传播的标志 */
    uint have_privileges; /**< 拥有特权的标志 */
    bool any_privileges; /**< 有特权的标志 */
    bool can_use_prefix_key; /**< 是否可以使用前缀键 */

    Item_field(Name_resolution_context *, const char *, const char *, const char *); /**< 构造函数 */
    Item_field(const POS &, const char *, const char *, const char *); /**< 带位置参数的构造函数 */
    Item_field(THD *, Item_field *); /**< 带 THD 和 Item_field 参数的构造函数 */
    Item_field(THD *, Name_resolution_context *, Table_ref *, Field *); /**< 带 THD、Name_resolution_context、Table_ref 和 Field 参数的构造函数 */
    Item_field(Field *); /**< 带 Field 参数的构造函数 */

  protected:
    void set_field(Field *); /**< 设置字段 */
    virtual void fix_after_pullout(Query_block *, Query_block *); /**< 提取后修复 */
    virtual type_conversion_status save_in_field_inner(Field *, bool); /**< 保存到字段内部 */

  public:
    void set_item_equal(Item_equal *); /**< 设置相等项 */
    void set_item_equal_all_join_nests(Item_equal *); /**< 设置所有连接嵌套的相等项 */
    virtual bool do_itemize(Parse_context *, Item **); /**< 进行项目化处理 */
    virtual Item::Type type(void) const; /**< 获取类型 */
    virtual bool eq(const Item *, bool) const; /**< 判断是否相等 */
    virtual double val_real(void); /**< 获取实数值 */
    virtual longlong val_int(void); /**< 获取整数值 */
    virtual longlong val_time_temporal(void); /**< 获取时间时态值 */
    virtual longlong val_date_temporal(void); /**< 获取日期时态值 */
    virtual longlong val_time_temporal_at_utc(void); /**< 获取带有时区的时间时态值 */
    virtual longlong val_date_temporal_at_utc(void); /**< 获取带有时区的日期时态值 */
    virtual my_decimal *val_decimal(my_decimal *); /**< 获取十进制数 */
    virtual String *val_str(String *); /**< 获取字符串值 */
    virtual bool val_json(Json_wrapper *); /**< 获取 JSON 值 */
    virtual bool send(Protocol *, String *); /**< 发送数据 */
    void reset_field(Field *); /**< 重置字段 */
    void reset_field(void); /**< 重置字段 */
    virtual bool fix_fields(THD *, Item **); /**< 修复字段 */
    virtual void make_field(Send_field *); /**< 构建 Send_field */
    virtual void save_org_in_field(Field *); /**< 保存原始值到字段 */
    virtual table_map used_tables(void) const; /**< 获取使用的表集合 */
    virtual Item_result result_type(void) const; /**< 获取结果类型 */
    virtual Item_result numeric_context_result_type(void) const; /**< 获取数字上下文结果类型 */
    virtual TYPELIB *get_typelib(void) const; /**< 获取类型库 */
    virtual Item_result cast_to_int_type(void) const; /**< 转换为整数类型 */
    virtual enum_monotonicity_info get_monotonicity_info(void) const; /**< 获取单调性信息 */
    virtual longlong val_int_endpoint(bool, bool *); /**< 获取整数端点值 */
    virtual void set_result_field(Field *); /**< 设置结果字段 */
    virtual Field *get_tmp_table_field(void); /**< 获取临时表字段 */
    virtual Field *tmp_table_field(TABLE *); /**< 获取临时表字段 */
    void set_base_item_field(const Item_field *); /**< 设置基本 Item_field */
    const Item_field *base_item_field(void) const; /**< 获取基本 Item_field */
    virtual bool get_date(MYSQL_TIME *, my_time_flags_t); /**< 获取日期值 */
    virtual bool get_time(MYSQL_TIME *); /**< 获取时间值 */
    virtual bool get_timeval(my_timeval *, int *); /**< 获取时间戳 */
    virtual bool is_null(void); /**< 判断是否为空 */
    virtual Item *get_tmp_table_item(THD *); /**< 获取临时表项目 */
    virtual bool collect_item_field_processor(uchar *); /**< 收集项目字段处理器 */
    virtual bool collect_item_field_or_ref_processor(uchar *); /**< 收集项目字段或引用处理器 */
    virtual bool collect_item_field_or_view_ref_processor(uchar *); /**< 收集项目字段或视图引用处理器 */
    virtual bool add_field_to_set_processor(uchar *); /**< 添加字段到集合处理器 */
    virtual bool add_field_to_cond_set_processor(uchar *); /**< 添加字段到条件集合处理器 */
    virtual bool remove_column_from_bitmap(uchar *); /**< 从位图中移除列 */
    virtual bool find_item_in_field_list_processor(uchar *); /**< 在字段列表中查找项目处理器 */
    virtual bool find_field_processor(uchar *); /**< 查找字段处理器 */
    virtual bool check_function_as_value_generator(uchar *); /**< 检查函数作为值生成器 */
    virtual bool mark_field_in_map(uchar *); /**< 在映射中标记字段 */
    virtual bool used_tables_for_level(uchar *); /**< 用于级别的使用表 */
    virtual bool check_column_privileges(uchar *); /**< 检查列权限 */
    virtual bool check_partition_func_processor(uchar *); /**< 检查分区函数处理器 */
    virtual void bind_fields(void); /**< 绑定字段 */
    virtual bool is_valid_for_pushdown(uchar *); /**< 是否有效用于下推 */
    virtual bool check_column_in_window_functions(uchar *); /**< 检查窗口函数中的列 */
    virtual bool check_column_in_group_by(uchar *); /**< 检查 GROUP BY 中的列 */
    virtual Item *replace_with_derived_expr(uchar *); /**< 用派生表达式替换 */
    virtual Item *replace_with_derived_expr_ref(uchar *); /**< 用派生表达式引用替换 */
    virtual void cleanup(void); /**< 清理 */
    Item_equal *find_item_equal(COND_EQUAL *) const; /**< 查找相等项 */
    virtual bool subst_argument_checker(uchar **); /**< 替代参数检查器 */
    virtual Item *equal_fields_propagator(uchar *); /**< 相等字段传播器 */
    virtual Item *replace_item_field(uchar *); /**< 替换项目字段 */
    virtual bool disable_constant_propagation(uchar *); /**< 禁用常量传播 */
    virtual Item *replace_equal_field(uchar *); /**< 替换相等字段 */
    uint32 max_disp_length(void); /**< 获取最大显示长度 */
    virtual Item_field *field_for_view_update(void); /**< 视图更新的字段 */
    virtual Item *safe_charset_converter(THD *, const CHARSET_INFO *); /**< 安全字符集转换器 */
    int fix_outer_field(THD *, Field **, Item **); /**< 修复外部字段 */
    virtual Item *update_value_transformer(uchar *); /**< 更新值转换器 */
    virtual void print(const THD *, String *, enum_query_type) const; /**< 打印 */
    virtual bool is_outer_field(void) const; /**< 是否是外部字段 */
    virtual Field::geometry_type get_geometry_type(void) const; /**< 获取几何类型 */
    virtual const CHARSET_INFO *charset_for_protocol(void); /**< 协议的字符集 */
    void dbug_print(void) const; /**< 调试打印 */
    virtual float get_filtering_effect(THD *, table_map, table_map, const MY_BITMAP *, double); /**< 获取过滤效果 */
    float get_cond_filter_default_probability(double, float) const; /**< 获取条件过滤默认概率 */
    virtual bool alias_name_used(void) const; /**< 是否使用别名 */
    virtual bool repoint_const_outer_ref(uchar *); /**< 重定向常量外部引用 */
    virtual bool returns_array(void) const; /**< 是否返回数组 */
    virtual void set_can_use_prefix_key(void); /**< 设置可以使用前缀键 */
    virtual bool replace_field_processor(uchar *); /**< 替换字段处理器 */
    virtual bool strip_db_table_name_processor(uchar *); /**< 去除数据库表名称处理器 */
    virtual bool is_asterisk(void) const; /**< 是否是星号 */
    bool protected_by_any_value(void) const; /**< 是否受到任何值保护 */
}
```

# Item_ident
```cpp
class Item_ident : public Item {
  protected:
    const char *m_orig_db_name; /**< 原始数据库名 */
    const char *m_orig_table_name; /**< 原始表名 */
    const char *m_orig_field_name; /**< 原始字段名 */
    bool m_alias_of_expr; /**< 表达式的别名 */

  public:
    Name_resolution_context *context; /**< 名称解析上下文 */
    const char *db_name; /**< 数据库名 */
    const char *table_name; /**< 表名 */
    const char *field_name; /**< 字段名 */
    Table_ref *cached_table; /**< 缓存的表 */
    Query_block *depended_from; /**< 依赖于的查询块 */

    Item_ident(Name_resolution_context *, const char *, const char *, const char *); /**< 构造函数 */
    Item_ident(const POS &, const char *, const char *, const char *); /**< 带位置参数的构造函数 */
    Item_ident(THD *, Item_ident *); /**< 带 THD 和 Item_ident 参数的构造函数 */
    virtual bool do_itemize(Parse_context *, Item **); /**< 进行项目化处理 */
    virtual const char *full_name(void) const; /**< 获取完整名称 */
    void set_orignal_db_name(const char *); /**< 设置原始数据库名 */
    void set_original_table_name(const char *); /**< 设置原始表名 */
    void set_original_field_name(const char *); /**< 设置原始字段名 */
    const char *original_db_name(void) const; /**< 获取原始数据库名 */
    const char *original_table_name(void) const; /**< 获取原始表名 */
    const char *original_field_name(void) const; /**< 获取原始字段名 */
    virtual void fix_after_pullout(Query_block *, Query_block *); /**< 提取后修复 */
    virtual bool aggregate_check_distinct(uchar *); /**< 聚合函数检查去重 */
    virtual bool aggregate_check_group(uchar *); /**< 聚合函数检查分组 */
    virtual Bool3 local_column(const Query_block *) const; /**< 本地列 */
    virtual void print(const THD *, String *, enum_query_type) const; /**< 打印 */

  protected:
    void print(const THD *, String *, enum_query_type, const char *, const char *) const; /**< 带额外参数的打印函数 */

  public:
    virtual bool change_context_processor(uchar *); /**< 更改上下文处理器 */
    bool is_alias_of_expr(void) const; /**< 是否是表达式的别名 */
    void set_alias_of_expr(void); /**< 设置表达式的别名 */
    virtual bool walk(Item_processor, enum_walk, uchar *); /**< 遍历 */
    virtual bool update_depended_from(uchar *); /**< 更新依赖关系 */
    virtual bool alias_name_used(void) const; /**< 是否使用别名 */
    virtual bool is_strong_side_column_not_in_fd(uchar *); /**< 是否强侧列不在函数依赖集中 */
    virtual bool is_column_not_in_fd(uchar *); /**< 是否列不在函数依赖集中 */
}
```

# Item
```cpp
class Item : public Parse_tree_node_tmpl<Parse_context> {
public:
    Item *next_free; /**< 下一个空闲项 */

protected:
    String str_value; /**< 字符串值 */

public:
    DTCollation collation; /**< 数据库排序规则 */
    Item_name_string item_name; /**< 项名称字符串 */
    Item_name_string orig_name; /**< 原始名称 */
    uint32 max_length; /**< 最大长度 */
    Item::item_marker marker; /**< 项标记 */
    Item_result cmp_context; /**< 比较上下文 */

private:
    uint m_ref_count; /**< 引用计数 */
    bool m_abandoned; /**< 是否被放弃 */
    const bool is_parser_item; /**< 是否为解析项 */
    int8 is_expensive_cache; /**< 是否为昂贵的缓存 */
    uint8 m_data_type; /**< 数据类型 */

public:
    bool fixed; /**< 是否固定 */
    uint8 decimals; /**< 小数位数 */

private:
    bool m_nullable; /**< 是否可为空 */

public:
    bool null_value; /**< 空值 */
    bool unsigned_flag; /**< 无符号标志 */
    bool m_is_window_function; /**< 是否为窗口函数 */
    bool hidden; /**< 是否隐藏 */
    bool m_in_check_constraint_exec_ctx; /**< 是否在检查约束执行上下文中 */

private:
    static const uint8 PROP_SUBQUERY; /**< 子查询属性 */
    static const uint8 PROP_STORED_PROGRAM; /**< 存储的程序属性 */
    static const uint8 PROP_AGGREGATION; /**< 聚合属性 */
    static const uint8 PROP_WINDOW_FUNCTION; /**< 窗口函数属性 */
    static const uint8 PROP_ROLLUP_EXPR; /**< ROLLUP 表达式属性 */
    static const uint8 PROP_GROUPING_FUNC; /**< 分组函数属性 */

protected:
    uint8 m_accum_properties; /**< 累积属性 */

private:
    virtual bool is_expensive_processor(uchar *); /**< 是否为昂贵的处理器 */

protected:
    String * make_empty_result(void); /**< 创建空结果 */

public:
    Item(const Item &); /**< 复制构造函数 */
    Item(void); /**< 构造函数 */
    Item(THD *, const Item *); /**< 带 THD 和 Item 参数的构造函数 */
    Item(const POS &); /**< 带位置参数的构造函数 */
    void operator=(Item &); /**< 赋值运算符 */
    static void * operator new(size_t); /**< new 运算符 */
    static void * operator new(size_t, MEM_ROOT *, const std::nothrow_t &); /**< 带内存根和异常处理的 new 运算符 */
    static void operator delete(void *, size_t); /**< delete 运算符 */
    static void operator delete(void *, MEM_ROOT *, const std::nothrow_t &); /**< 带内存根和异常处理的 delete 运算符 */
    static enum_field_types result_to_type(Item_result); /**< 结果转换为类型 */
    static Item_result type_to_result(enum_field_types); /**< 类型转换为结果 */
    static enum_field_types type_for_variable(enum_field_types); /**< 变量的类型 */
    ~Item(); /**< 析构函数 */

private:
    virtual bool do_contextualize(Parse_context *); /**< 上下文化处理 */

protected:
    bool skip_itemize(Item **); /**< 跳过项目化处理 */
    static bool bit_func_returns_binary(const Item *, const Item *); /**< 位函数是否返回二进制 */
    virtual bool do_itemize(Parse_context *, Item **); /**< 进行项目化处理 */

public:
    virtual bool itemize(Parse_context *, Item **); /**< 项目化处理 */
    void rename(char *); /**< 重命名 */
    void init_make_field(Send_field *, enum_field_types); /**< 初始化字段生成 */
    virtual void cleanup(void); /**< 清理 */
    virtual void notify_removal(void); /**< 通知移除 */
    virtual void make_field(Send_field *); /**< 生成字段 */
    virtual Field * make_string_field(TABLE *) const; /**< 生成字符串字段 */
    virtual bool fix_fields(THD *, Item **); /**< 修复字段 */
    virtual void fix_after_pullout(Query_block *, Query_block *); /**< 提取后修复 */
    void quick_fix_field(void); /**< 快速修复字段 */
    virtual void set_can_use_prefix_key(void); /**< 设置可使用前缀键 */
    virtual bool propagate_type(THD *, const Type_properties &); /**< 传播类型 */
    bool propagate_type(THD *, enum_field_types, bool, bool); /**< 传播类型 */
    virtual void mark_json_as_scalar(void); /**< 将 JSON 标记为标量 */
    virtual std::optional<ContainedSubquery> get_contained_subquery(const Query_block *); /**< 获取包含的子查询 */

protected:
    virtual type_conversion_status save_in_field_inner(Field *, bool); /**< 保存至字段内部 */

public:
    type_conversion_status save_in_field_no_warnings(Field *, bool); /**< 保存至字段（无警告） */
    type_conversion_status save_in_field(Field *, bool); /**< 保存至字段 */
    void save_in_field_no_error_check(Field *, bool); /**< 保存至字段（无错误检查） */
    virtual void save_org_in_field(Field *); /**< 保存原始至字段 */
    virtual bool send(Protocol *, String *); /**< 发送 */
    bool evaluate(THD *, String *); /**< 评估 */
    virtual bool eq(const Item *, bool) const; /**< 相等比较 */
    virtual Item_result result_type(void) const; /**< 结果类型 */
    virtual Item_result numeric_context_result_type(void) const; /**< 数字上下文结果类型 */
    Item_result temporal_with_date_as_number_result_type(void) const; /**< 具有日期作为数字的时间结果类型 */
    virtual void set_data_type_inherited(void); /**< 设置继承的数据类型 */
    virtual void pin_data_type(void); /**< 固定数据类型 */
    enum_field_types data_type(void) const; /**< 数据类型 */
    virtual enum_field_types actual_data_type(void) const; /**< 实际数据类型 */
    virtual enum_field_types default_data_type(void) const; /**< 默认数据类型 */
    void set_data_type(enum_field_types); /**< 设置数据类型 */
    void set_data_type_null(void); /**< 设置数据类型为 null */
    void set_data_type_bool(void); /**< 设置数据类型为 bool */
    void set_data_type_int(enum_field_types, bool, uint32); /**< 设置数据类型为整型 */
    void set_data_type_longlong(void); /**< 设置数据类型为长整型 */
    void set_data_type_decimal(uint8, uint8); /**< 设置数据类型为小数 */
    void set_data_type_double(void); /**< 设置数据类型为双精度浮点数 */
    void set_data_type_float(void); /**< 设置数据类型为单精度浮点数 */
    void set_data_type_string(uint32); /**< 设置数据类型为字符串 */
    void set_data_type_string(ulonglong); /**< 设置数据类型为字符串 */
    void set_data_type_string(uint32, const CHARSET_INFO *); /**< 设置数据类型为字符串 */
    void set_data_type_string(uint32, const DTCollation &); /**< 设置数据类型为字符串 */
    void set_data_type_char(uint32); /**< 设置数据类型为字符 */
    void set_data_type_char(uint32, const CHARSET_INFO *); /**< 设置数据类型为字符 */
    void set_data_type_blob(enum_field_types, uint32); /**< 设置数据类型为 BLOB */
    void set_data_type_date(void); /**< 设置数据类型为日期 */
    void set_data_type_time(uint8); /**< 设置数据类型为时间 */
    void set_data_type_datetime(uint8); /**< 设置数据类型为日期时间 */
    void set_data_type_timestamp(uint8); /**< 设置数据类型为时间戳 */
    void set_data_type_geometry(void); /**< 设置数据类型为几何类型 */
    void set_data_type_json(void); /**< 设置数据类型为 JSON */
    void set_data_type_year(void); /**< 设置数据类型为年 */
    void set_data_type_bit(uint32); /**< 设置数据类型为位 */
    void set_data_type_from_item(const Item *); /**< 从项设置数据类型 */
    static enum_field_types string_field_type(uint32); /**< 字符串字段类型 */
    virtual TYPELIB * get_typelib(void) const; /**< 获取类型库 */
    virtual Item_result cast_to_int_type(void) const; /**< 转换为整数类型 */
    virtual Item::Type type(void) const; /**< 项类型 */
    bool aggregate_type(const char *, Item **, uint); /**< 聚合类型 */
    virtual enum_monotonicity_info get_monotonicity_info(void) const; /**< 获取单调性信息 */
    virtual longlong val_int_endpoint(bool, bool *); /**< 整数端点值 */
    virtual double val_real(void); /**< 实数值 */
    virtual longlong val_int(void); /**< 整数值 */
    virtual longlong val_date_temporal(void); /**< 日期时间值 */
    virtual longlong val_time_temporal(void); /**< 时间值 */
    longlong val_temporal_by_field_type(void); /**< 通过字段类型的时间值 */
    longlong int_sort_key(void); /**< 整数排序键 */
    longlong val_temporal_with_round(enum_field_types, uint8); /**< 具有四舍五入的时间值 */
    ulonglong val_uint(void); /**< 无符号整数值 */
    virtual String * val_str(String *); /**< 字符串值 */
    virtual String * val_str_ascii(String *); /**< ASCII 字符串值 */
    virtual my_decimal * val_decimal(my_decimal *); /**< 小数值 */
    virtual bool val_bool(void); /**< 布尔值 */
    virtual bool val_json(Json_wrapper *); /**< JSON 值 */
    virtual float get_filtering_effect(THD *, table_map, table_map, const MY_BITMAP *, double); /**< 获取过滤效果 */
    bool error_json(void); /**< JSON 错误 */
    bool get_date_from_non_temporal(MYSQL_TIME *, my_time_flags_t); /**< 从非时间获取日期 */
    bool get_time_from_non_temporal(MYSQL_TIME *); /**< 从非时间获取时间 */

protected:
    String * val_string_from_real(String *); /**< 从实数获取字符串 */
    String * val_string_from_int(String *); /**< 从整数获取字符串 */
    String * val_string_from_decimal(String *); /**< 从小数获取字符串 */
    String * val_string_from_date(String *); /**< 从日期获取字符串 */
    String * val_string_from_datetime(String *); /**< 从日期时间获取字符串 */
    String * val_string_from_time(String *); /**< 从时间获取字符串 */
    my_decimal * val_decimal_from_real(my_decimal *); /**< 从实数获取小数 */
    my_decimal * val_decimal_from_int(my_decimal *); /**< 从整数获取小数 */
    my_decimal * val_decimal_from_string(my_decimal *); /**< 从字符串获取小数 */
    my_decimal * val_decimal_from_date(my_decimal *); /**< 从日期获取小数 */
    my_decimal * val_decimal_from_time(my_decimal *); /**< 从时间获取小数 */
    longlong val_int_from_decimal(void); /**< 从小数获取整数 */
    longlong val_int_from_date(void); /**< 从日期获取整数 */
    longlong val_int_from_time(void); /**< 从时间获取整数 */
    longlong val_int_from_datetime(void); /**< 从日期时间获取整数 */
    longlong val_int_from_string(void); /**< 从字符串获取整数 */
    double val_real_from_decimal(void); /**< 从小数获取实数 */
    double val_real_from_string(void); /**< 从字符串获取实数 */
    bool error_bool(void); /**< 布尔错误 */
    int error_int(void); /**< 整数错误 */
    double error_real(void); /**< 实数错误 */
    bool error_date(void); /**< 日期错误 */
    bool error_time(void); /**< 时间错误 */

public:
    my_decimal * error_decimal(my_decimal *); /**< 小数错误 */
    String * error_str(void); /**< 字符串错误 */

protected:
    String * null_return_str(void); /**< 空值返回字符串 */
    bool get_date_from_string(MYSQL_TIME *, my_time_flags_t); /**< 从字符串获取日期 */
        bool get_date_from_real(MYSQL_TIME *, my_time_flags_t);  // 从实数获取日期
    bool get_date_from_decimal(MYSQL_TIME *, my_time_flags_t);  // 从十进制数获取日期
    bool get_date_from_int(MYSQL_TIME *, my_time_flags_t);  // 从整数获取日期
    bool get_date_from_time(MYSQL_TIME *);  // 从时间获取日期
    bool get_date_from_numeric(MYSQL_TIME *, my_time_flags_t);  // 从数字获取日期
    bool get_time_from_string(MYSQL_TIME *);  // 从字符串获取时间
    bool get_time_from_real(MYSQL_TIME *);  // 从实数获取时间
    bool get_time_from_decimal(MYSQL_TIME *);  // 从十进制数获取时间
    bool get_time_from_int(MYSQL_TIME *);  // 从整数获取时间
    bool get_time_from_date(MYSQL_TIME *);  // 从日期获取时间
    bool get_time_from_datetime(MYSQL_TIME *);  // 从日期时间获取时间
    bool get_time_from_numeric(MYSQL_TIME *);  // 从数字获取时间
    virtual longlong val_date_temporal_at_utc(void);  // 获取日期时区在UTC的值
    virtual longlong val_time_temporal_at_utc(void);  // 获取时间时区在UTC的值

  public:
    type_conversion_status save_time_in_field(Field *);  // 保存时间到字段
    type_conversion_status save_date_in_field(Field *);  // 保存日期到字段
    type_conversion_status save_str_value_in_field(Field *, String *);  // 保存字符串值到字段
    virtual Field * get_tmp_table_field(void);  // 获取临时表字段
    virtual Field * tmp_table_field(TABLE *);  // 临时表字段
    virtual const char * full_name(void) const;  // 获取完整名称
    virtual table_map used_tables(void) const;  // 使用的表
    virtual table_map not_null_tables(void) const;  // 非空表
    virtual bool basic_const_item(void) const;  // 是否为基本常量项
    bool may_eval_const_item(const THD *) const;  // 是否可以评估为常量项
    virtual Item * clone_item(void) const;  // 克隆项
    virtual Item::cond_result eq_cmp_result(void) const;  // 相等比较结果
    uint float_length(uint) const;  // 浮点数长度
    virtual uint decimal_precision(void) const;  // 十进制精度
    int decimal_int_part(void) const;  // 十进制整数部分
    virtual uint time_precision(void);  // 时间精度
    virtual uint datetime_precision(void);  // 日期时间精度
    bool const_item(void) const;  // 常量项
    bool const_for_execution(void) const;  // 是否为执行时常量
    bool may_evaluate_const(const THD *) const;  // 是否可以评估为常量
    bool is_non_deterministic(void) const;  // 是否为非确定性项
    bool is_outer_reference(void) const;  // 是否为外部引用
    virtual void print(const THD *, String *, enum_query_type) const;  // 打印项
    void print_item_w_name(const THD *, String *, enum_query_type) const;  // 打印项带名称
    void print_for_order(const THD *, String *, enum_query_type, const char *) const;  // 为排序打印项
    virtual void update_used_tables(void);  // 更新使用的表
    virtual void split_sum_func(THD *, Ref_item_array, mem_root_deque<Item*> *);  // 分离汇总函数
    void split_sum_func2(THD *, Ref_item_array, mem_root_deque<Item*> *, Item **, bool);  // 分离汇总函数2
    virtual bool get_date(MYSQL_TIME *, my_time_flags_t);  // 获取日期
    virtual bool get_time(MYSQL_TIME *);  // 获取时间
    virtual bool get_timeval(my_timeval *, int *);  // 获取时间值
    virtual bool is_null(void);  // 是否为空
    bool update_null_value(void);  // 更新空值
    virtual void apply_is_true(void);  // 应用为真
    virtual void set_result_field(Field *);  // 设置结果字段
    virtual bool is_result_field(void) const;  // 是否为结果字段
    virtual Field * get_result_field(void) const;  // 获取结果字段
    virtual bool is_bool_func(void) const;  // 是否为布尔函数
    virtual void no_rows_in_result(void);  // 结果中没有行
    virtual Item * copy_or_same(THD *);  // 复制或相同
    virtual Item * copy_andor_structure(THD *);  // 复制AND/OR结构
    virtual Item * real_item(void);  // 真实项
    virtual const Item * real_item(void) const;  // 真实项（常量版本）
    virtual Item * get_tmp_table_item(THD *);  // 获取临时表项
    static const CHARSET_INFO * default_charset(void);  // 默认字符集
    virtual const CHARSET_INFO * compare_collation(void) const;  // 比较排序规则
    virtual const CHARSET_INFO * charset_for_protocol(void);  // 协议字符集
    virtual bool walk(Item_processor, enum_walk, uchar *);  // 遍历
    virtual Item * transform(Item_transformer, uchar *);  // 转换
    virtual Item * compile(Item_analyzer, uchar **, Item_transformer, uchar *);  // 编译
    virtual void traverse_cond(Cond_traverser, void *, Item::traverse_order);  // 遍历条件
    virtual bool intro_version(uchar *);  // 介绍版本
    bool cleanup_processor(uchar *);  // 清理处理器
    virtual bool collect_item_field_processor(uchar *);  // 收集项字段处理器
    virtual bool collect_item_field_or_ref_processor(uchar *);  // 收集项字段或引用处理器
    virtual bool collect_item_field_or_view_ref_processor(uchar *);  // 收集项字段或视图引用处理器
    virtual bool add_field_to_set_processor(uchar *);  // 添加字段到集合处理器
    virtual bool visitor_processor(uchar *);  // 访问者处理器
    virtual bool add_field_to_cond_set_processor(uchar *);  // 添加字段到条件集合处理器
    virtual bool remove_column_from_bitmap(uchar *);  // 从位图中移除列处理器
    virtual bool find_item_in_field_list_processor(uchar *);  // 在字段列表中查找项处理器
    virtual bool change_context_processor(uchar *);  // 更改上下文处理器
    virtual bool find_item_processor(uchar *);  // 查找项处理器
    virtual bool is_non_const_over_literals(uchar *);  // 是否为字面量上的非常量处理器
    virtual bool find_field_processor(uchar *);  // 查找字段处理器
    virtual bool cast_incompatible_args(uchar *);  // 转换不兼容参数处理器
    virtual bool mark_field_in_map(uchar *);  // 在映射中标记字段处理器
  protected:
    static bool mark_field_in_map(Mark_field *, Field *);  // 在映射中标记字段处理器
  public:
    virtual bool reset_wf_state(uchar *);  // 重置wf状态处理器
    virtual bool used_tables_for_level(uchar *);  // 使用表的级别处理器
    virtual bool check_column_privileges(uchar *);  // 检查列权限处理器
    virtual bool inform_item_in_cond_of_tab(uchar *);  // 通知条件中的表处理器
    virtual void bind_fields(void);  // 绑定字段
    virtual bool clean_up_after_removal(uchar *);  // 移除后清理处理器
    virtual bool aggregate_check_distinct(uchar *);  // 聚合检查不同处理器
    virtual bool aggregate_check_group(uchar *);  // 聚合检查组处理器
    virtual bool is_strong_side_column_not_in_fd(uchar *);  // 强侧列不在fd中处理器
    virtual bool is_column_not_in_fd(uchar *);  // 列不在fd中处理器
    virtual Bool3 local_column(const Query_block *) const;  // 本地列处理器
    virtual bool collect_scalar_subqueries(uchar *);  // 收集标量子查询处理器
    virtual bool collect_grouped_aggregates(uchar *);  // 收集分组聚合处理器
    virtual bool collect_subqueries(uchar *);  // 收集子查询处理器
    virtual bool update_depended_from(uchar *);  // 更新依赖处理器
    virtual bool has_aggregate_ref_in_group_by(uchar *);  // 在GROUP BY中具有聚合引用处理器
    bool visit_all_analyzer(uchar **);  // 访问所有分析器
    virtual bool cache_const_expr_analyzer(uchar **);  // 缓存常量表达式分析器
    Item * cache_const_expr_transformer(uchar *);  // 缓存常量表达式转换器
    virtual bool equality_substitution_analyzer(uchar **);  // 相等替换分析器
    virtual Item * equality_substitution_transformer(uchar *);  // 相等替换转换器
    virtual bool check_partition_func_processor(uchar *);  // 检查分区函数处理器
    virtual bool subst_argument_checker(uchar **);  // 替换参数检查器
    virtual bool explain_subquery_checker(uchar **);  // 解释子查询检查器
    virtual Item * explain_subquery_propagator(uchar *);  // 解释子查询传播器
    virtual Item * equal_fields_propagator(uchar *);  // 相等字段传播器
    virtual bool disable_constant_propagation(uchar *);  // 禁用常量传播处理器
    virtual Item * replace_equal_field(uchar *);  // 替换相等字段处理器
    virtual bool check_valid_arguments_processor(uchar *);  // 检查有效参数处理器
    virtual bool check_function_as_value_generator(uchar *);  // 检查函数作为值生成器处理器
    virtual bool check_gcol_depend_default_processor(uchar *);  // 检查gcol依赖默认处理器
    virtual bool is_valid_for_pushdown(uchar *);  // 是否可用于下推优化
    virtual bool check_column_in_window_functions(uchar *);  // 检查列是否在窗口函数中
    virtual bool check_column_in_group_by(uchar *);  // 检查列是否在GROUP BY子句中
    virtual Item * replace_with_derived_expr(uchar *);  // 替换为派生表达式
    virtual Item * replace_with_derived_expr_ref(uchar *);  // 替换为派生表达式引用
    virtual Item * replace_view_refs_with_clone(uchar *);  // 用克隆替换视图引用
    virtual Item * this_item(void);  // 获取当前项
    virtual const Item * this_item(void) const;  // 获取当前项（常量版本）
    virtual Item ** this_item_addr(THD *, Item **);  // 获取当前项的地址
    virtual uint cols(void) const;  // 列数
    virtual Item * element_index(uint);  // 获取指定元素索引
    virtual Item ** addr(uint);  // 获取地址
    virtual bool check_cols(uint);  // 检查列数
    virtual bool null_inside(void);  // 是否含有NULL
    virtual void bring_value(void);  // 获取值
    Field * tmp_table_field_from_field_type(TABLE *, bool) const;  // 从字段类型创建临时表字段
    virtual Item_field * field_for_view_update(void);  // 获取用于视图更新的字段
    virtual Item * truth_transformer(THD *, Item::Bool_test);  // 真值转换器
    virtual Item * update_value_transformer(uchar *);  // 更新值转换器
    virtual Item * replace_scalar_subquery(uchar *);  // 替换标量子查询
    virtual Item * replace_item_field(uchar *);  // 替换字段项
    virtual Item * replace_item_view_ref(uchar *);  // 替换视图引用项
    virtual Item * replace_aggregate(uchar *);  // 替换聚合项
    virtual Item * replace_outer_ref(uchar *);  // 替换外部引用项
    virtual bool update_aggr_refs(uchar *);  // 更新聚合引用
    virtual Item * safe_charset_converter(THD *, const CHARSET_INFO *);  // 安全字符集转换器
    void delete_self(void);  // 删除自身
    virtual bool is_splocal(void) const;  // 是否为存储过程本地变量
    virtual Settable_routine_parameter * get_settable_routine_parameter(void);  // 获取可设置的例程参数
    bool is_temporal_with_date(void) const;  // 是否包含日期时间信息
    bool is_temporal_with_date_and_time(void) const;  // 是否包含日期和时间信息
    bool is_temporal_with_time(void) const;  // 是否包含时间信息
    bool is_temporal(void) const;  // 是否包含时间属性
    bool has_compatible_context(Item *) const;  // 是否有兼容的上下文
    virtual Field::geometry_type get_geometry_type(void) const;  // 获取几何类型
    String * check_well_formed_result(String *, bool, bool);  // 检查结果是否格式良好
    bool eq_by_collation(Item *, bool, const CHARSET_INFO *);  // 是否通过排序规则相等
    virtual bool is_expensive(void);  // 是否昂贵
    uint32 max_char_length(void) const;  // 最大字符长度
    uint32 max_char_length(const CHARSET_INFO *) const;  // 按字符集的最大字符长度
    void fix_char_length(uint32);  // 修复字符长度
    virtual bool is_outer_field(void) const;  // 是否为外部字段
    bool is_blob_field(void) const;  // 是否为BLOB字段
    void increment_ref_count(void);  // 增加引用计数
    uint decrement_ref_count(void);  // 减少引用计数
    protected:
    void set_accum_properties(const Item *);  // 设置累加属性
    void add_accum_properties(const Item *);  // 添加累加属性
    void set_subquery(void);  // 设置子查询
    void set_stored_program(void);  // 设置存储过程
    public:
    bool has_subquery(void) const;  // 是否包含子查询
    bool has_stored_program(void) const;  // 是否包含存储过程
    bool has_aggregation(void) const;  // 是否包含聚合
    void set_aggregation(void);  // 设置聚合
    void reset_aggregation(void);  // 重置聚合
    bool has_wf(void) const;  // 是否包含工作流
    void set_wf(void);  // 设置工作流
    bool has_rollup_expr(void) const;  // 是否包含ROLLUP表达式
    void set_rollup_expr(void);  // 设置ROLLUP表达式
    bool has_grouping_func(void) const;  // 是否包含GROUPING函数
    void set_grouping_func(void);  // 设置GROUPING函数
    virtual bool created_by_in2exists(void) const;  // 是否由IN子查询创建
    void mark_subqueries_optimized_away(void);  // 标记已优化的子查询
    virtual bool gc_subst_analyzer(uchar **);  // 垃圾收集替换分析器
    virtual Item * gc_subst_transformer(uchar *);  // 垃圾收集替换转换器
    virtual bool replace_field_processor(uchar *);  // 替换字段处理器
    bool can_be_substituted_for_gc(bool) const;  // 是否可以被垃圾收集替代
    void aggregate_float_properties(enum_field_types, Item **, uint);  // 聚合浮点属性
    void aggregate_decimal_properties(Item **, uint);  // 聚合十进制属性
    uint32 aggregate_char_width(Item **, uint);  // 聚合字符宽度
    void aggregate_temporal_properties(enum_field_types, Item **, uint);  // 聚合时间属性
    bool aggregate_string_properties(enum_field_types, const char *, Item **, uint);  // 聚合字符串属性
    void aggregate_bit_properties(Item **, uint);  // 聚合位属性
    virtual bool repoint_const_outer_ref(uchar *);  // 重定向常量外部引用
    virtual bool strip_db_table_name_processor(uchar *);  // 剥离数据库表名处理器
    private:
    virtual bool subq_opt_away_processor(uchar *);  // 子查询优化处理器
    public:
    bool is_nullable(void) const;  // 是否可为空
    void set_nullable(bool);  // 设置可为空
    virtual bool supports_partial_update(const Field_json *) const;  // 是否支持部分更新
    virtual bool returns_array(void) const;  // 是否返回数组
    virtual void allow_array_cast(void);  // 允许数组转换
    bool walk_helper_thunk<Item_field::is_valid_for_pushdown(uchar*)::<lambda(Item*)> >(uchar *);  // 遍历辅助函数
}
```