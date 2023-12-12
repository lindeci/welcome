- [MaterializeIterator](#materializeiterator)
- [TableRowIterator](#tablerowiterator)
- [RowIterator](#rowiterator)

# MaterializeIterator
```cpp
-exec ptype this

class MaterializeIterator<DummyIteratorProfiler> [with Profiler = DummyIteratorProfiler] : public TableRowIterator {
  private:
    Mem_root_array<materialize_iterator::QueryBlock> m_query_blocks_to_materialize; // 待物化的查询块内存根数组
    unique_ptr_destroy_only m_table_iterator; // 唯一指针，用于销毁迭代器
    Common_table_expr *m_cte; // 公共表达式
    Query_expression *m_query_expression; // 查询表达式
    JOIN * const m_join; // 连接
    const int m_ref_slice; // 参考切片数
    const bool m_rematerialize; // 是否重新物化
    const bool m_reject_multiple_rows; // 拒绝多行
    const ha_rows m_limit_rows; // 限制的行数
    Mem_root_array<MaterializeIterator<Profiler>::Invalidator> m_invalidators; // 无效化器的物化迭代器内存根数组
    Profiler m_profiler; // 迭代器性能分析器
    Profiler m_table_iter_profiler; // 表迭代器性能分析器

  public:
    MaterializeIterator(THD *, Mem_root_array<materialize_iterator::QueryBlock>, const MaterializePathParameters *, unique_ptr_destroy_only, JOIN *); // 构造函数
    virtual bool Init(void); // 初始化函数
    virtual int Read(void); // 读取函数
    virtual void SetNullRowFlag(bool); // 设置空行标志函数
    virtual void StartPSIBatchMode(void); // 启动 PSI 批处理模式函数
    virtual void EndPSIBatchModeIfStarted(void); // 如果已启动，则结束 PSI 批处理模式函数
    virtual void UnlockRow(void); // 解锁行函数
    virtual const IteratorProfiler * GetProfiler(void) const; // 获取迭代器性能分析器函数
    const Profiler * GetTableIterProfiler(void) const; // 获取表迭代器性能分析器函数

  private:
    bool doing_hash_deduplication(void) const; // 是否进行哈希去重复函数
    bool doing_deduplication(void) const; // 是否进行去重复函数
    bool MaterializeRecursive(void); // 递归物化函数
    bool MaterializeQueryBlock(const materialize_iterator::QueryBlock &, ha_rows *); // 物化查询块函数
} * const;

```

# TableRowIterator
```cpp

 class TableRowIterator : public RowIterator {
  private:
    TABLE * const m_table; // 数据表指针

  public:
    TableRowIterator(THD *, TABLE *); // 构造函数
    virtual void UnlockRow(void); // 解锁行函数
    virtual void SetNullRowFlag(bool); // 设置空行标志函数
    virtual void StartPSIBatchMode(void); // 启动 PSI 批处理模式函数
    virtual void EndPSIBatchModeIfStarted(void); // 如果已启动，则结束 PSI 批处理模式函数

  protected:
    int HandleError(int); // 处理错误函数
    void PrintError(int); // 打印错误函数
    TABLE * table(void) const; // 获取数据表函数
}

```
TableRowIterator 有几个派生类，其中一些常见的派生类包括但可能不限于：
- MaterializeIterator： 该类用于支持材料化操作，实现了特定的材料化迭代逻辑，允许生成结果并按需访问已存储的数据，而不是重新计算。
- JoinCacheIterator： 这个迭代器实现了对连接缓存的迭代，用于管理连接查询的缓存。
- MultiRangeReadIterator： 用于在多个范围中读取数据的迭代器，适用于范围读取查询。
- RangeSeqNextIterator： 用于按范围顺序迭代下一行数据的迭代器，对于某些查询操作是十分关键的。
- RangeOptFlagIterator： 在查询优化过程中使用的迭代器，用于处理优化标志。


# RowIterator
```cpp
class RowIterator {
  private:
    THD * const m_thd; // 线程处理器指针

  public:
    RowIterator(THD *); // 构造函数
    RowIterator(const RowIterator &); // 拷贝构造函数
    RowIterator(RowIterator &&); // 移动构造函数
    ~RowIterator(); // 析构函数
    virtual bool Init(void); // 初始化函数
    virtual int Read(void); // 读取函数
    virtual void SetNullRowFlag(bool); // 设置空行标志函数
    virtual void UnlockRow(void); // 解锁行函数
    virtual const IteratorProfiler * GetProfiler(void) const; // 获取迭代器性能分析器函数
    virtual void SetOverrideProfiler(const IteratorProfiler *); // 设置覆盖性能分析器函数
    virtual void StartPSIBatchMode(void); // 启动 PSI 批处理模式函数
    virtual void EndPSIBatchModeIfStarted(void); // 如果已启动，则结束 PSI 批处理模式函数
    virtual RowIterator * real_iterator(void); // 获取真实迭代器函数
    virtual const RowIterator * real_iterator(void) const; // 获取真实迭代器函数

  protected:
    THD * thd(void) const; // 获取线程处理器指针函数
}

```