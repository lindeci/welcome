- [缩略版](#缩略版)

# 缩略版
```cpp
struct TABLE {
  public:
    TABLE_SHARE *s;  // 数据表共享信息
    handler *file;  // 数据表处理程序
    TABLE *next;  // 下一个数据表
    TABLE *prev;  // 前一个数据表
  private:
    TABLE *cache_next;  // 缓存下一个数据表
    TABLE **cache_prev;  // 缓存前一个数据表
  public:
    const Table_histograms *histograms;  // 数据表直方图信息
    MY_BITMAP fields_for_functional_indexes;  // 用于函数索引的字段位图
    THD *in_use;  // 数据表当前使用的线程
    Field **field;  // 数据表字段数组
    uint hidden_field_count;  // 隐藏字段数量
    uchar *record[2];  // 记录缓冲区
    uchar *write_row_record;  // 写入行记录缓冲区
    uchar *insert_values;  // 插入值数组
    Record_buffer m_record_buffer;  // 记录缓冲区
    Key_map covering_keys;  // 覆盖键位图
    Key_map quick_keys;  // 快速查找键位图
    Key_map merge_keys;  // 合并键位图
    Key_map possible_quick_keys;  // 可能的快速查找键位图
    Key_map keys_in_use_for_query;  // 用于查询的键位图
    Key_map keys_in_use_for_group_by;  // 用于分组的键位图
    Key_map keys_in_use_for_order_by;  // 用于排序的键位图
    KEY *key_info;  // 键信息
    KEY_PART_INFO *base_key_parts;  // 基本键部分信息
    Field *next_number_field;  // 下一个编号字段
    Field *found_next_number_field;  // 已找到的下一个编号字段
    Field **vfield;  // 虚拟字段数组
    Field **gen_def_fields_ptr;  // 生成的默认字段指针
    Field *hash_field;  // 哈希字段
    ha_rows m_limit_rows;  // 限制的行数
  private:
    Field_longlong *m_set_counter;  // 设置计数器
    bool m_except;  // 是否为除法查询
    bool m_last_operation_is_distinct;  // 上次操作是否为DISTINCT
  public:
    Field *fts_doc_id_field;  // 全文搜索文档ID字段
    Table_trigger_dispatcher *triggers;  // 表触发器分发器
    Table_ref *pos_in_table_list;  // 表在表列表中的位置
    Table_ref *pos_in_locked_tables;  // 表在锁定表列表中的位置
    ORDER *group;  // 分组信息
    const char *alias;  // 表别名
    uchar *null_flags;  // NULL标志数组
    uchar *null_flags_saved;  // 保存的NULL标志数组
    MY_BITMAP def_read_set;  // 默认读取位图
    MY_BITMAP def_write_set;  // 默认写入位图
    MY_BITMAP tmp_set;  // 临时位图
    MY_BITMAP pack_row_tmp_set;  // 打包行的临时位图
    MY_BITMAP cond_set;  // 条件位图
    MY_BITMAP def_fields_set_during_insert;  // 插入时设置的字段位图
    MY_BITMAP *read_set;  // 读取位图指针
    MY_BITMAP *write_set;  // 写入位图指针
    MY_BITMAP read_set_internal;  // 内部读取位图
    MY_BITMAP *fields_set_during_insert;  // 插入时设置的字段位图指针
    query_id_t query_id;  // 查询ID
    ha_rows quick_rows[64];  // 快速查找行数数组
    key_part_map const_key_parts[64];  // 常量键部分位图
    uint quick_key_parts[64];  // 快速查找键部分
    uint quick_n_ranges[64];  // 快速查找范围数量
    ha_rows quick_condition_rows;  // 快速查找条件行数
    uint lock_position;  // 锁定位置
    uint lock_data_start;  // 锁定数据起始位置
    uint lock_count;  // 锁定计数
    uint db_stat;  // 数据库状态
    int current_lock;  // 当前锁定
    Sql_table_check_constraint_list *table_check_constraint_list;  // 表检查约束列表
  private:
    bool nullable;  // 是否可空
    uint8 m_status;  // 状态
  public:
    bool null_row;  // 空行
    bool copy_blobs;  // 复制BLOB
    bool force_index;  // 强制使用索引
    bool force_index_order;  // 强制使用索引的顺序
    bool force_index_group;  // 强制使用索引的分组
    bool const_table;  // 常量表
    bool no_rows;  // 无行
    bool key_read;  // 键读取
    bool no_keyread;  // 无键读取
    bool no_replicate;  // 无复制
    bool open_by_handler;  // 由处理程序打开
    bool autoinc_field_has_explicit_non_null_value;  // 自增字段是否具有显式非NULL值
    bool alias_name_used;  // 是否使用别名
    bool get_fields_in_item_tree;  // 获取项树中的字段
  private:
    bool m_invalid_dict;  // 无效的字典
    bool m_invalid_stats;  // 无效的统计信息
    bool created;  // 是否已创建
  public:
    bool materialized;  // 材料化的
    struct {
        JOIN_TAB *join_tab;  // 连接表
        QEP_TAB *qep_tab;  // QEP表
        thr_lock_type lock_type;  // 锁类型
        bool not_exists_optimize;  // 不存在优化
        bool impossible_range;  // 不可能的范围
    } reginfo;  // 注册信息
    MEM_ROOT mem_root;  // 内存根
    Blob_mem_storage *blob_storage;  // BLOB内存存储
    SortingIterator *sorting_iterator;  // 排序迭代器
    SortingIterator *duplicate_removal_iterator;  // 去重迭代器
    Sort_result unique_result;  // 唯一结果
    partition_info *part_info;  // 分区信息
    bool all_partitions_pruned_away;  // 所有分区被修剪
    MDL_ticket *mdl_ticket;  // MDL锁票
  private:
    Cost_model_table m_cost_model;  // 成本模型
    uint tmp_table_seq_id;  // 临时表序列ID
    MY_BITMAP *m_partial_update_columns;  // 部分更新字段位图
    Partial_update_info *m_partial_update_info;  // 部分更新信息
    bool should_binlog_drop_if_temp_flag;  // 如果是临时标志，则应该在二进制日志中丢弃
  // ... (后续方法成员略)
}


# 详细版
```cpp
struct TABLE {
  public:
    TABLE_SHARE *s;
    handler *file;
    TABLE *next;
    TABLE *prev;
  private:
    TABLE *cache_next;
    TABLE **cache_prev;
  public:
    const Table_histograms *histograms;
    MY_BITMAP fields_for_functional_indexes;
    THD *in_use;
    Field **field;
    uint hidden_field_count;
    uchar *record[2];
    uchar *write_row_record;
    uchar *insert_values;
    Record_buffer m_record_buffer;
    Key_map covering_keys;
    Key_map quick_keys;
    Key_map merge_keys;
    Key_map possible_quick_keys;
    Key_map keys_in_use_for_query;
    Key_map keys_in_use_for_group_by;
    Key_map keys_in_use_for_order_by;
    KEY *key_info;
    KEY_PART_INFO *base_key_parts;
    Field *next_number_field;
    Field *found_next_number_field;
    Field **vfield;
    Field **gen_def_fields_ptr;
    Field *hash_field;
    ha_rows m_limit_rows;
  private:
    Field_longlong *m_set_counter;
    bool m_except;
    bool m_last_operation_is_distinct;
  public:
    Field *fts_doc_id_field;
    Table_trigger_dispatcher *triggers;
    Table_ref *pos_in_table_list;
    Table_ref *pos_in_locked_tables;
    ORDER *group;
    const char *alias;
    uchar *null_flags;
    uchar *null_flags_saved;
    MY_BITMAP def_read_set;
    MY_BITMAP def_write_set;
    MY_BITMAP tmp_set;
    MY_BITMAP pack_row_tmp_set;
    MY_BITMAP cond_set;
    MY_BITMAP def_fields_set_during_insert;
    MY_BITMAP *read_set;
    MY_BITMAP *write_set;
    MY_BITMAP read_set_internal;
    MY_BITMAP *fields_set_during_insert;
    query_id_t query_id;
    ha_rows quick_rows[64];
    key_part_map const_key_parts[64];
    uint quick_key_parts[64];
    uint quick_n_ranges[64];
    ha_rows quick_condition_rows;
    uint lock_position;
    uint lock_data_start;
    uint lock_count;
    uint db_stat;
    int current_lock;
    Sql_table_check_constraint_list *table_check_constraint_list;
  private:
    bool nullable;
    uint8 m_status;
  public:
    bool null_row;
    bool copy_blobs;
    bool force_index;
    bool force_index_order;
    bool force_index_group;
    bool const_table;
    bool no_rows;
    bool key_read;
    bool no_keyread;
    bool no_replicate;
    bool open_by_handler;
    bool autoinc_field_has_explicit_non_null_value;
    bool alias_name_used;
    bool get_fields_in_item_tree;
  private:
    bool m_invalid_dict;
    bool m_invalid_stats;
    bool created;
  public:
    bool materialized;
    struct {
        JOIN_TAB *join_tab;
        QEP_TAB *qep_tab;
        thr_lock_type lock_type;
        bool not_exists_optimize;
        bool impossible_range;
    } reginfo;
    MEM_ROOT mem_root;
    Blob_mem_storage *blob_storage;
    SortingIterator *sorting_iterator;
    SortingIterator *duplicate_removal_iterator;
    Sort_result unique_result;
    partition_info *part_info;
    bool all_partitions_pruned_away;
    MDL_ticket *mdl_ticket;
  private:
    Cost_model_table m_cost_model;
    uint tmp_table_seq_id;
    MY_BITMAP *m_partial_update_columns;
    Partial_update_info *m_partial_update_info;
    bool should_binlog_drop_if_temp_flag;

  public:
    bool is_union_or_table(void) const;
    bool is_intersect(void) const;
    bool is_except(void) const;
    bool is_distinct(void) const;
    void set_set_counter(Field_longlong *, bool);
    void set_distinct(bool);
    Field_longlong * set_counter(void);
    void reset(void);
    void init(THD *, Table_ref *);
    bool init_tmp_table(THD *, TABLE_SHARE *, MEM_ROOT *, CHARSET_INFO *, const char *, Field **, uint *, bool);
    bool fill_item_list(mem_root_deque<Item*> *) const;
    void clear_column_bitmaps(void);
    void prepare_for_position(void);
    void mark_column_used(Field *, enum_mark_columns);
    void mark_columns_used_by_index_no_reset(uint, MY_BITMAP *, uint) const;
    void mark_columns_used_by_index(uint);
    void mark_auto_increment_column(void);
    void mark_columns_needed_for_update(THD *, bool);
    void mark_columns_needed_for_delete(THD *);
    void mark_columns_needed_for_insert(THD *);
    void mark_columns_per_binlog_row_image(THD *);
    void mark_generated_columns(bool);
    void mark_gcol_in_maps(const Field *);
    void mark_check_constraint_columns(bool);
    void column_bitmaps_set(MY_BITMAP *, MY_BITMAP *);
    void column_bitmaps_set_no_signal(MY_BITMAP *, MY_BITMAP *);
    void use_all_columns(void);
    void default_column_bitmaps(void);
    void invalidate_dict(void);
    void invalidate_stats(void);
    bool has_invalid_dict(void) const;
    bool has_invalid_stats(void);
    Field ** visible_field_ptr(void) const;
    uint visible_field_count(void) const;
    bool alloc_tmp_keys(uint, uint, bool);
    bool add_tmp_key(Field_map *, bool, bool);
    void move_tmp_key(int, bool);
    void drop_unused_tmp_keys(bool);
    void set_keyread(bool);
    bool index_contains_some_virtual_gcol(uint) const;
    void update_const_key_parts(Item *);
    bool check_read_removal(uint);
    ptrdiff_t default_values_offset(void) const;
    bool has_storage_handler(void) const;
    void set_storage_handler(handler *);
    bool is_created(void) const;
    void set_created(void);
    void set_deleted(void);
    void set_nullable(void);
    bool is_nullable(void) const;
    bool has_gcol(void) const;
    void set_not_started(void);
    bool is_started(void) const;
    void set_found_row(void);
    void set_no_row(void);
    void set_row_status_from_handler(int);
    void set_null_row(void);
    void reset_null_row(void);
    void set_updated_row(void);
    void set_deleted_row(void);
    bool has_row(void) const;
    bool has_null_row(void) const;
    bool has_updated_row(void) const;
    bool has_deleted_row(void) const;
    void save_null_flags(void);
    void restore_null_flags(void);
    bool empty_result_table(void);
    void init_cost_model(const Cost_model_server *);
    const Cost_model_table * cost_model(void) const;
    void bind_value_generators_to_fields(void);
    void cleanup_value_generator_items(void);
    void set_tmp_table_seq_id(uint);
    void update_covering_prefix_keys(Field *, uint16, Key_map *);
    handler * get_primary_handler(void) const;
    bool has_binary_diff_columns(void) const;
    const Binary_diff_vector * get_binary_diffs(const Field *) const;
    bool mark_column_for_partial_update(const Field *);
    bool is_marked_for_partial_update(const Field *) const;
    bool has_columns_marked_for_partial_update(void) const;
    bool setup_partial_update(bool);
    bool setup_partial_update(void);
    bool add_binary_diff(const Field *, size_t, size_t);
    void clear_partial_update_diffs(void);
    void cleanup_partial_update(void);
    void disable_binary_diffs_for_current_row(const Field *);
    void disable_logical_diffs_for_current_row(const Field *) const;
    String * get_partial_update_buffer(void);
    void add_logical_diff(const Field_json *, const Json_seekable_path &, enum_json_diff_operation, const Json_wrapper *);
    const Json_diff_vector * get_logical_diffs(const Field_json *) const;
    bool is_binary_diff_enabled(const Field *) const;
    bool is_logical_diff_enabled(const Field *) const;
    void blobs_need_not_keep_old_value(void);
    void set_binlog_drop_if_temp(bool);
    bool should_binlog_drop_if_temp(void) const;
    const histograms::Histogram * find_histogram(uint) const;
}
```