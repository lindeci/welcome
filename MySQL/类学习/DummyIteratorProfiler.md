
# DummyIteratorProfiler
```cpp
class DummyIteratorProfiler : public IteratorProfiler {
  public:
    static DummyIteratorProfiler::TimeStamp Now(void); // 静态函数 - 获取当前时间戳
    virtual double GetFirstRowMs(void) const; // 获取首行时间（毫秒）函数
    virtual double GetLastRowMs(void) const; // 获取末行时间（毫秒）函数
    virtual uint64_t GetNumInitCalls(void) const; // 获取初始化调用次数函数
    virtual uint64_t GetNumRows(void) const; // 获取行数函数
    void StopInit(DummyIteratorProfiler::TimeStamp); // 停止初始化函数
    void IncrementNumRows(uint64_t); // 增加行数函数
    void StopRead(DummyIteratorProfiler::TimeStamp, bool); // 停止读取函数
}

```

# IteratorProfiler
```cpp
class IteratorProfiler {
  public:
    virtual double GetFirstRowMs(void) const;
    virtual double GetLastRowMs(void) const;
    virtual uint64_t GetNumInitCalls(void) const;
    virtual uint64_t GetNumRows(void) const;
    ~IteratorProfiler();
}
```