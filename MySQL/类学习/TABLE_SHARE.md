```cpp
struct TABLE_SHARE {
  public:
    // 表的直方图数据集合
    Table_histograms_collection *m_histograms;
    // 表分类
    TABLE_CATEGORY table_category;
    // 内存根节点
    MEM_ROOT mem_root;
    // 为临时文件处理器分配的内存根节点
    MEM_ROOT *alloc_for_tmp_file_handler;
    // 键名类型库
    TYPELIB keynames;
    // 区间类型库
    TYPELIB *intervals;
    // ha_data的互斥锁
    mysql_mutex_t LOCK_ha_data;
    // 下一个表共享对象
    TABLE_SHARE *next;
    // 前一个表共享对象
    TABLE_SHARE **prev;
    // 表缓存元素
    Table_cache_element **cache_element;
    // 字段
    Field **field;
    // 下一个数字字段
    Field **found_next_number_field;
    // 键信息
    KEY *key_info;
    // blob字段
    uint *blob_field;
    // 默认值
    uchar *default_values;
    // 注释
    LEX_STRING comment;
    // 压缩
    LEX_STRING compress;
    // 加密类型
    LEX_STRING encrypt_type;
    // 次要引擎
    LEX_CSTRING secondary_engine;
    // 是否次要加载
    bool secondary_load;
    // 表字符集
    const CHARSET_INFO *table_charset;
    // 所有设置
    MY_BITMAP all_set;
    // 表缓存键
    LEX_CSTRING table_cache_key;
    // 数据库
    LEX_CSTRING db;
    // 表名
    LEX_CSTRING table_name;
    // 路径
    LEX_STRING path;
    // 标准化路径
    LEX_CSTRING normalized_path;
    // 连接字符串
    LEX_STRING connect_string;
    // 引擎属性
    LEX_CSTRING engine_attribute;
    // 次要引擎属性
    LEX_CSTRING secondary_engine_attribute;
    // 使用的键
    Key_map keys_in_use;
    // 可见的索引
    Key_map visible_indexes;
    // 用于键读取的键
    Key_map keys_for_keyread;
    // 最小行数
    ha_rows min_rows;
    // 最大行数
    ha_rows max_rows;
    // 平均行长度
    ulong avg_row_length;
    // MySQL版本
    ulong mysql_version;
    // 记录长度
    ulong reclength;
    // 存储记录长度
    ulong stored_rec_length;
    // 自动扩展大小
    ulonglong autoextend_size;
    // 数据库插件引用
    plugin_ref db_plugin;
    // 行类型
    row_type row_type;
    // 真实行类型
    row_type real_row_type;
    // 临时表类型
    tmp_table_type tmp_table;
    // 临时处理器计数
    uint tmp_handler_count;
    // 临时打开计数
    uint tmp_open_count;
    // 键块大小
    uint32_t key_block_size;
    // 统计采样页面数
    uint stats_sample_pages;
    // 统计自动重新计算
    enum_stats_auto_recalc stats_auto_recalc;
    // NULL字节数
    uint null_bytes;
    // 最后一个NULL位位置
    uint last_null_bit_pos;
    // 字段数
    uint fields;
    // 记录缓冲长度
    uint rec_buff_length;
    // 键数
    uint keys;
    // 键部分数
    uint key_parts;
    // 最大键长度
    uint max_key_length;
    // 最大唯一键长度
    uint max_unique_length;
    // 总键长度
    uint total_key_length;
    // 是否不同
    bool is_distinct;
    // NULL字段数
    uint null_fields;
    // BLOB字段数
    uint blob_fields;
    // VARCHAR字段数
    uint varchar_fields;
    // 第一个未使用的临时键
    uint first_unused_tmp_key;
    // 最大临时键数
    uint max_tmp_keys;
    // 最大临时键部分数
    uint max_tmp_key_parts;
    // 键名
    Key_name *key_names;
    // 基本键对应的记录数
    ulong *base_rec_per_key;
    // 基本键对应的记录数（浮点数）
    rec_per_key_t *base_rec_per_key_float;
    // 数据库创建选项
    uint db_create_options;
    // 数据库选项使用情况
    uint db_options_in_use;
    // Rowid字段偏移
    uint rowid_field_offset;
    // 主键
    uint primary_key;
    // 下一个数字索引
    uint next_number_index;
    // 下一个数字键偏移
    uint next_number_key_offset;
    // 下一个数字键部分
    uint next_number_keypart;
    // 错误
    bool error;
    // 列位图大小
    uint column_bitmap_size;
    // 虚拟字段数
    uint vfields;
    // 生成的默认字段数
    uint gen_def_field_count;
    // 系统
    bool system;
    // 数据库低字节优先
    bool db_low_byte_first;
    // 崩溃
    bool crashed;
    // 是否视图
    bool is_view;
    // 是否正在打开中
    bool m_open_in_progress;
    // 表映射ID
    Table_id table_map_id;
    // 缓存的行日志检查
    int cached_row_logging_check;
    // 默认存储介质
    ha_storage_media default_storage_media;
    // 表空间
    const char *tablespace;
    // 分区信息
    partition_info *m_part_info;
    // 自动分区
    bool auto_partitioned;
    // 分区信息字符串
    char *partition_info_str;
    // 分区信息字符串长度
    uint partition_info_str_len;
    // 表字段定义缓存
    const TABLE_FIELD_DEF *table_field_def_cache;
    // 存储引擎共享对象
    Handler_share *ha_share;
    // PSI表共享对象
    PSI_table_share *m_psi;
    // 等待刷新列表
    Wait_for_flush_list m_flush_tickets;
    // 视图对象
    const dd::View *view_object;
    // 临时表定义
    dd::Table *tmp_table_def;
    // 可能临时键的所有者
    Query_block *owner_of_possible_tmp_keys;
    // 外键数
    uint foreign_keys;
    // 外键信息
    TABLE_SHARE_FOREIGN_KEY_INFO *foreign_key;
    // 外键父数
    uint foreign_key_parents;
    // 外键父信息
    TABLE_SHARE_FOREIGN_KEY_PARENT_INFO *foreign_key_parent;
    // 检查约束共享列表
    Sql_check_constraint_share_list *check_constraint_share_list;
    // 表共享架构只读
    TABLE_SHARE::Schema_read_only schema_read_only;

  private:
    // 引用计数
    unsigned int m_ref_count;
    // 版本
    unsigned long m_version;

  protected:
    // 次要引擎
    bool m_secondary_engine;

  public:
    // 构造函数
    TABLE_SHARE(void);
    TABLE_SHARE(unsigned long, bool);
    // 数据库类型
    handlerton * db_type(void) const;
    // 设置表缓存键
    void set_table_cache_key(char *, size_t);
    void set_table_cache_key(char *, const char *, size_t);
    // 获取表定义版本
    ulonglong get_table_def_version(void) const;
    // 获取版本
    unsigned long version(void) const;
    // 清除版本
    void clear_version(void);
    // 是否有旧版本
    bool has_old_version(void) const;
    // 获取表引用类型
    enum_table_ref_type get_table_ref_type(void) const;
    // 获取表引用版本
    ulonglong get_table_ref_version(void) const;
    // 是否缺少主键
    bool is_missing_primary_key(void) const;
    // 查找第一个未使用的临时键
    uint find_first_unused_tmp_key(const Key_map &);
    // 访问子图
    bool visit_subgraph(Wait_for_flush *, MDL_wait_for_graph_visitor *);
    // 等待旧版本
    bool wait_for_old_version(THD *, timespec *, uint);
    // 可用索引
    Key_map usable_indexes(const THD *) const;
    // 销毁
    void destroy(void);
    // 获取引用计数
    unsigned int ref_count(void) const;
    // 增加引用计数
    unsigned int increment_ref_count(void);
    // 减少引用计数
    unsigned int decrement_ref_count(void);
    // 是否主要引擎
    bool is_primary_engine(void) const;
    // 是否次要引擎
    bool is_secondary_engine(void) const;
    // 是否有次要引擎
    bool has_secondary_engine(void) const;
    // 是否被外键引用
    bool is_referenced_by_foreign_key(void) const;
};
```