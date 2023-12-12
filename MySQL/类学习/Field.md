- [Field 缩略版](#field-缩略版)
- [Field 完整版](#field-完整版)
- [Field\_varstring](#field_varstring)
- [Field\_longstr](#field_longstr)
- [Field\_str](#field_str)

在MySQL源码中，`Item_field`和`Field`这两个类都是非常重要的，但它们的作用和用途是不同的。

- `Item_field`：这是一个继承自`Item`的类，用于表示SQL查询中的字段。例如，在查询`SELECT column1 FROM table1`中，`column1`就会被表示为一个`Item_field`对象。`Item_field`对象存储了字段的元信息，并且可以用于计算和遍历表达式树。

- `Field`：这个类用于描述表中的列或属性。`Field`是对列数据类型以及属性的定义。`Field`类是一个抽象类，几乎每种类型的列都有相对应的`Field`子类。例如，`Field_tiny`、`Field_short`、`Field_medium`、`Field_long`、`Field_longlong`等都是`Field`的子类，分别对应于不同的整数类型。`Field`类的对象存储了实际的字段值，每次读取记录后会将记录存储到相应的`Field`里以便表达式计算。

总的来说，`Item_field`主要用于在查询解析和优化阶段表示字段，而`Field`则用于在执行阶段处理字段的数据和元数据。


# Field 缩略版
```cpp
class Field {
  protected:
    uchar *ptr; // 指针

  private:
    dd::Column::enum_hidden_type m_hidden; // 隐藏列类型
    uchar *m_null_ptr; // 空指针
    bool m_is_tmp_nullable; // 临时可为空
    bool m_is_tmp_null; // 临时为空
    enum_check_fields m_check_for_truncated_fields_saved; // 截断字段保存的检查

  protected:
    static uchar dummy_null_buffer; // 虚拟空缓冲

  public:
    TABLE *table; // 表
    const char *orig_db_name; // 原始数据库名
    const char *orig_table_name; // 原始表名
    const char **table_name; // 表名
    const char *field_name; // 字段名
    LEX_CSTRING comment; // 注释
    Key_map key_start; // 键开始
    Key_map part_of_key; // 键的一部分
    Key_map part_of_prefixkey; // 前缀键的一部分
    Key_map part_of_sortkey; // 排序键的一部分
    Key_map part_of_key_not_extended; // 未扩展键的一部分

  private:
    static const size_t MAX_VARCHAR_WIDTH; // 最大变长字符宽度
    static const size_t MAX_TINY_BLOB_WIDTH; // 最大 TINY_BLOB 宽度
    static const size_t MAX_SHORT_BLOB_WIDTH; // 最大 SHORT_BLOB 宽度
    static const size_t MAX_MEDIUM_BLOB_WIDTH; // 最大 MEDIUM_BLOB 宽度
    static const size_t MAX_LONG_BLOB_WIDTH; // 最大 LONG_BLOB 宽度

  public:
    uint32 field_length; // 字段长度

  private:
    uint32 flags; // 标志
    uint16 m_field_index; // 字段索引

  public:
    uchar null_bit; // 空位
    uchar auto_flags; // 自动标志
    bool is_created_from_null_item; // 是否从空项目创建
    bool m_indexed; // 是否被索引
    LEX_CSTRING m_engine_attribute; // 引擎属性
    LEX_CSTRING m_secondary_engine_attribute; // 二级引擎属性

  private:
    unsigned int m_warnings_pushed; // 推送的警告

  public:
    Value_generator *gcol_info; // 值生成器信息
    bool stored_in_db; // 是否在数据库中存储
    Value_generator *m_default_val_expr; // 默认值表达式

    Field(const Field &); // 复制构造函数
    Field(uchar *, uint32, uchar *, uchar, uchar, const char *); // 构造函数
    void operator=(Field &); // 赋值运算符重载
    // 更多成员函数...
}

```
# Field 完整版
```cpp
class Field {
  protected:
    uchar *ptr;
  private:
    dd::Column::enum_hidden_type m_hidden;
    uchar *m_null_ptr;
    bool m_is_tmp_nullable;
    bool m_is_tmp_null;
    enum_check_fields m_check_for_truncated_fields_saved;
  protected:
    static uchar dummy_null_buffer;
  public:
    TABLE *table;
    const char *orig_db_name;
    const char *orig_table_name;
    const char **table_name;
    const char *field_name;
    LEX_CSTRING comment;
    Key_map key_start;
    Key_map part_of_key;
    Key_map part_of_prefixkey;
    Key_map part_of_sortkey;
    Key_map part_of_key_not_extended;
  private:
    static const size_t MAX_VARCHAR_WIDTH;
    static const size_t MAX_TINY_BLOB_WIDTH;
    static const size_t MAX_SHORT_BLOB_WIDTH;
    static const size_t MAX_MEDIUM_BLOB_WIDTH;
    static const size_t MAX_LONG_BLOB_WIDTH;
  public:
    uint32 field_length;
  private:
    uint32 flags;
    uint16 m_field_index;
  public:
    uchar null_bit;
    uchar auto_flags;
    bool is_created_from_null_item;
    bool m_indexed;
    LEX_CSTRING m_engine_attribute;
    LEX_CSTRING m_secondary_engine_attribute;
  private:
    unsigned int m_warnings_pushed;
  public:
    Value_generator *gcol_info;
    bool stored_in_db;
    Value_generator *m_default_val_expr;

    Field(const Field &);
    Field(uchar *, uint32, uchar *, uchar, uchar, const char *);
    void operator=(Field &);
    bool has_insert_default_general_value_expression(void) const;
    bool has_insert_default_datetime_value_expression(void) const;
    bool has_update_default_datetime_value_expression(void) const;
    bool has_insert_default_constant_expression(void) const;
    uchar * get_null_ptr(void);
    virtual void set_field_length(uint32);
    bool is_flag_set(unsigned int) const;
    void set_flag(unsigned int);
    void clear_flag(unsigned int);
    uint32 all_flags(void) const;
    virtual bool is_unsigned(void) const;
    bool is_gcol(void) const;
    bool is_virtual_gcol(void) const;
    void set_hidden(dd::Column::enum_hidden_type);
    dd::Column::enum_hidden_type hidden(void) const;
    bool is_hidden(void) const;
    bool is_hidden_by_system(void) const;
    bool is_hidden_by_user(void) const;
    bool is_field_for_functional_index(void) const;
    ~Field();
    void reset_warnings(void);
    void set_tmp_nullable(void);
    void reset_tmp_nullable(void);
    void reset_tmp_null(void);
    void set_tmp_null(void);
    bool is_tmp_nullable(void) const;
    bool is_tmp_null(void) const;
    virtual type_conversion_status store(const char *, size_t, const CHARSET_INFO *);
    virtual type_conversion_status store(double);
    virtual type_conversion_status store(longlong, bool);
    type_conversion_status store(const char *, size_t, const CHARSET_INFO *, enum_check_fields);
    virtual type_conversion_status store_packed(longlong);
    virtual type_conversion_status store_decimal(const my_decimal *);
    virtual type_conversion_status store_time(MYSQL_TIME *, uint8);
    type_conversion_status store_time(MYSQL_TIME *);
    virtual double val_real(void) const;
    virtual longlong val_int(void) const;
    longlong val_int(uchar *);
    virtual longlong val_time_temporal(void) const;
    virtual longlong val_date_temporal(void) const;
    virtual longlong val_time_temporal_at_utc(void) const;
    virtual longlong val_date_temporal_at_utc(void) const;
    longlong val_temporal_by_field_type(void) const;
    virtual my_decimal * val_decimal(my_decimal *) const;
    String * val_str(String *) const;
    virtual String * val_str(String *, String *) const;
    String * val_str(String *, uchar *);
    String * val_int_as_str(String *, bool) const;
    virtual bool str_needs_quotes(void) const;
    virtual Item_result result_type(void) const;
    virtual Item_result numeric_context_result_type(void) const;
    virtual Item_result cmp_type(void) const;
    virtual Item_result cast_to_int_type(void) const;
    static bool type_can_have_key_part(enum_field_types);
    static enum_field_types field_type_merge(enum_field_types, enum_field_types);
    static Item_result result_merge_type(enum_field_types);
    bool gcol_expr_is_equal(const Create_field *) const;
    virtual bool eq(const Field *) const;
    virtual bool eq_def(const Field *) const;
    virtual uint32 pack_length(void) const;
    virtual uint32 pack_length_in_rec(void) const;
    virtual bool compatible_field_size(uint, Relay_log_info *, uint16, int *) const;
    virtual uint pack_length_from_metadata(uint) const;
    virtual uint row_pack_length(void) const;
    int save_field_metadata(uchar *);
    virtual uint32 data_length(ptrdiff_t) const;
    virtual uint32 max_data_length(void) const;
    virtual type_conversion_status reset(void);
    virtual bool get_timestamp(my_timeval *, int *) const;
    virtual void store_timestamp(const my_timeval *);
    virtual void set_default(void);
    void evaluate_insert_default_function(void);
    void evaluate_update_default_function(void);
    virtual bool binary(void) const;
    virtual bool zero_pack(void) const;
    virtual ha_base_keytype key_type(void) const;
    virtual uint32 key_length(void) const;
    virtual enum_field_types type(void) const;
    virtual enum_field_types real_type(void) const;
    virtual enum_field_types binlog_type(void) const;
    int cmp(const uchar *) const;
    virtual int cmp(const uchar *, const uchar *) const;
    virtual int cmp_max(const uchar *, const uchar *, uint) const;
    virtual int cmp_binary(const uchar *, const uchar *, uint32) const;
    virtual int cmp_offset(ptrdiff_t) const;
    virtual int cmp_binary_offset(ptrdiff_t) const;
    virtual int key_cmp(const uchar *, const uchar *) const;
    virtual int key_cmp(const uchar *, uint) const;
    virtual uint decimals(void) const;
    virtual bool is_text_key_type(void) const;
    virtual void sql_type(String &) const;
    bool is_null(ptrdiff_t) const;
    bool is_real_null(ptrdiff_t) const;
    bool is_null_in_record(const uchar *) const;
    void set_null(ptrdiff_t);
    void set_notnull(ptrdiff_t);
    type_conversion_status check_constraints(int);
    void set_check_for_truncated_fields(enum_check_fields);
    bool is_nullable(void) const;
    uint null_offset(const uchar *) const;
    uint null_offset(void) const;
    void set_null_ptr(uchar *, uint);
    virtual void make_send_field(Send_field *) const;
    virtual size_t make_sort_key(uchar *, size_t) const;
    virtual bool optimize_range(uint, uint) const;
    virtual bool can_be_compared_as_longlong(void) const;
    virtual void mem_free(void);
    virtual Field * new_field(MEM_ROOT *, TABLE *) const;
    Field * new_field(MEM_ROOT *, TABLE *, uchar *, uchar *, uint) const;
    virtual Field * new_key_field(MEM_ROOT *, TABLE *, uchar *, uchar *, uint) const;
    Field * new_key_field(MEM_ROOT *, TABLE *, uchar *) const;
    virtual Field * clone(MEM_ROOT *) const;
    void move_field(uchar *, uchar *, uchar);
    virtual void move_field_offset(ptrdiff_t);
    virtual void get_image(uchar *, size_t, const CHARSET_INFO *) const;
    virtual void set_image(const uchar *, size_t, const CHARSET_INFO *);
    virtual size_t get_key_image(uchar *, size_t, Field::imagetype) const;
    virtual void set_key_image(const uchar *, size_t);
    longlong val_int_offset(ptrdiff_t);
    virtual bool send_to_protocol(Protocol *) const;
    virtual uchar * pack(uchar *, const uchar *, size_t) const;
    uchar * pack(uchar *) const;
    virtual const uchar * unpack(uchar *, const uchar *, uint);
    const uchar * unpack(const uchar *);
    virtual uchar * pack_with_metadata_bytes(uchar *, const uchar *, uint) const;
    virtual bool pack_diff(uchar **, ulonglong) const;
    virtual uint max_packed_col_length(void) const;
    uint offset(uchar *) const;
    void copy_data(ptrdiff_t);
    virtual bool get_date(MYSQL_TIME *, my_time_flags_t) const;
    virtual bool get_time(MYSQL_TIME *) const;
    virtual const CHARSET_INFO * charset(void) const;
    const CHARSET_INFO * charset_for_protocol(void) const;
    virtual const CHARSET_INFO * sort_charset(void) const;
    virtual bool has_charset(void) const;
    virtual bool match_collation_to_optimize_range(void) const;
    virtual Derivation derivation(void) const;
    virtual uint repertoire(void) const;
    virtual void set_derivation(Derivation);
    bool set_warning(Sql_condition::enum_severity_level, unsigned int, int);
    bool set_warning(Sql_condition::enum_severity_level, uint, int, const char *, const char *);
    bool warn_if_overflow(int);
    virtual void init(TABLE *);
    virtual uint32 max_display_length(void) const;
    virtual uint is_equal(const Create_field *) const;
    longlong convert_decimal2longlong(const my_decimal *, bool, bool *);
    virtual uint32 char_length(void) const;
    virtual Field::geometry_type get_geometry_type(void) const;
    void dbug_print(void) const;
    ha_storage_media field_storage_type(void) const;
    void set_storage_type(ha_storage_media);
    column_format_type column_format(void) const;
    void set_column_format(column_format_type);
    virtual type_conversion_status validate_stored_val(THD *);
    virtual void hash(ulong *, ulong *) const;
    virtual ulonglong get_max_int_value(void) const;
    virtual const uchar * data_ptr(void) const;
    const uchar * field_ptr(void) const;
    uchar * field_ptr(void);
    void set_field_ptr(uchar *);
    virtual bool is_updatable(void) const;
    bool is_part_of_actual_key(THD *, uint, KEY *) const;
    Key_map get_covering_prefix_keys(void) const;
    virtual bool is_array(void) const;
    virtual uint32 get_length_bytes(void) const;
    bool handle_old_value(void) const;
    virtual void set_field_index(uint16);
    uint16 field_index(void) const;
  private:
    virtual int do_save_field_metadata(uchar *) const;
  protected:
    uchar * pack_int16(uchar *, const uchar *, size_t) const;
    const uchar * unpack_int16(uchar *, const uchar *) const;
    uchar * pack_int24(uchar *, const uchar *, size_t) const;
    const uchar * unpack_int24(uchar *, const uchar *) const;
    uchar * pack_int32(uchar *, const uchar *, size_t) const;
    const uchar * unpack_int32(uchar *, const uchar *) const;
    uchar * pack_int64(uchar *, const uchar *, size_t) const;
    const uchar * unpack_int64(uchar *, const uchar *) const;
}
```

# Field_varstring 
```cpp
class Field_varstring : public Field_longstr {
private:
    uint32 length_bytes;  // 存储字符串长度的字节数

public:
    Field_varstring(uchar *, uint32, uint, uchar *, uchar, uchar, const char *, TABLE_SHARE *, const CHARSET_INFO *);
    // 构造函数，接受多个参数
    Field_varstring(uint32, bool, const char *, TABLE_SHARE *, const CHARSET_INFO *);
    // 构造函数，接受另一组参数
    virtual enum_field_types type(void) const;
    // 返回字段的类型
    virtual bool match_collation_to_optimize_range(void) const;
    // 检查排序规则以优化范围
    virtual ha_base_keytype key_type(void) const;
    // 返回键的类型
    virtual uint row_pack_length(void) const;
    // 返回行的打包长度
    virtual bool zero_pack(void) const;
    // 返回是否零打包
    virtual uint32 pack_length(void) const;
    // 返回打包长度
    virtual uint32 key_length(void) const;
    // 返回键长度
    virtual type_conversion_status store(const char *, size_t, const CHARSET_INFO *);
    // 存储字符串的方法
    virtual type_conversion_status store(longlong, bool);
    // 存储长整型数据的方法
    // ... 其他虚拟函数将执行特定操作 ...
    // ... 比如处理各种数据类型，比较，打包等 ...
  private:
    virtual int do_save_field_metadata(uchar *) const;
    // 保存字段元数据的私有方法
};
```

# Field_longstr
```cpp
class Field_longstr : public Field_str {
  public:
    Field_longstr(uchar *, uint32, uchar *, uchar, uchar, const char *, const CHARSET_INFO *); // 构造函数

  private:
    type_conversion_status report_if_important_data(const char *, const char *, bool); // 如果重要数据，报告转换状态函数

  protected:
    type_conversion_status check_string_copy_error(const char *, const char *, const char *, const char *, bool, const CHARSET_INFO *); // 检查字符串复制错误的转换状态函数

  public:
    virtual type_conversion_status store_decimal(const my_decimal *); // 存储十进制数的转换状态函数
    virtual uint32 max_data_length(void) const; // 获取最大数据长度函数
    virtual bool is_updatable(void) const; // 是否可更新函数
}

```

# Field_str
```cpp
type = class Field_str : public Field {
  protected:
    const CHARSET_INFO *field_charset; // 字段字符集信息
    Derivation field_derivation; // 字段派生信息

  public:
    uint32 char_length_cache; // 字符长度缓存

    Field_str(uchar *, uint32, uchar *, uchar, uchar, const char *, const CHARSET_INFO *); // 构造函数
    virtual Item_result result_type(void) const; // 结果类型函数
    virtual Item_result numeric_context_result_type(void) const; // 数字上下文结果类型函数
    virtual uint decimals(void) const; // 小数点位数函数
    virtual void make_send_field(Send_field *) const; // 创建发送字段函数
    virtual type_conversion_status store(double); // 存储双精度浮点数的转换状态函数
    virtual type_conversion_status store(longlong, bool); // 存储长整型的转换状态函数
    virtual type_conversion_status store(const char *, size_t, const CHARSET_INFO *); // 存储字符的转换状态函数
    virtual type_conversion_status store_decimal(const my_decimal *); // 存储十进制数的转换状态函数
    virtual uint repertoire(void) const; // 字符集函数
    virtual const CHARSET_INFO * charset(void) const; // 获取字符集函数
    void set_charset(const CHARSET_INFO *); // 设置字符集函数
    virtual void set_field_length(uint32); // 设置字段长度函数
    virtual Derivation derivation(void) const; // 获取派生信息函数
    virtual void set_derivation(Derivation); // 设置派生信息函数
    virtual bool binary(void) const; // 是否为二进制数据函数
    virtual uint32 max_display_length(void) const; // 最大显示长度函数
    virtual bool str_needs_quotes(void) const; // 字符是否需要引号函数
    virtual uint is_equal(const Create_field *) const; // 判断是否相等函数
}
```