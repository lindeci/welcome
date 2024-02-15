```cpp
class Query_term_set_op : public Query_term {
private:
    Query_block *m_block;  // 查询块指针

public:
    mem_root_deque<Query_term*> m_children;  // 查询项指针数组
    int64_t m_last_distinct;  // 最后的去重标识
    int64_t m_first_distinct;  // 第一个的去重标识
    bool m_is_materialized;  // 是否已物化

protected:
    Query_term_set_op(MEM_ROOT *);  // 构造函数声明

public:
    virtual Query_block * query_block(void) const;  // 返回查询块指针
    bool set_block(Query_block *);  // 设置查询块
    virtual size_t child_count(void) const;  // 子项数量
    virtual bool open_result_tables(THD *, int);  // 打开结果表
    virtual void cleanup(bool);  // 清理
    virtual void destroy_tree(void);  // 销毁树结构
    bool has_mixed_distinct_operators(void);  // 是否有混合的去重操作符
    bool is_unary(void) const;  // 是否一元
    Mem_root_array<MaterializePathParameters::QueryBlock> setup_materialize_set_op(THD *, TABLE *, bool, bool);  // 设置物化集合操作

protected:
    void print(int, std::ostringstream &, const char *) const;  // 打印函数声明
}
```




```cpp
class Query_term_set_op : public Query_term {
  private:
    Query_block *m_block;
  public:
    mem_root_deque<Query_term*> m_children;
    int64_t m_last_distinct;
    int64_t m_first_distinct;
    bool m_is_materialized;
}

class Query_term {
  protected:
    Query_term_set_op *m_parent;
    Query_result *m_setop_query_result;
    bool m_owning_operand;
    Table_ref *m_result_table;
    mem_root_deque<Item*> *m_fields;
  private:
    uint m_curr_id;
}
```