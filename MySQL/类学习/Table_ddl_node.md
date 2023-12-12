- [PT\_column\_def 类注释](#pt_column_def-类注释)
- [PT\_table\_element 类定义](#pt_table_element-类定义)
- [Table\_ddl\_node 类定义](#table_ddl_node-类定义)
- [Parse\_tree\_node\_tmpl 类注释](#parse_tree_node_tmpl-类注释)
- [PT\_table\_constraint\_def 类定义](#pt_table_constraint_def-类定义)
- [PT\_check\_constraint 类定义](#pt_check_constraint-类定义)

# PT_column_def 类注释
```cpp
class PT_column_def : public PT_table_element {
  private:
    const LEX_STRING field_ident;  // 字段标识
    PT_field_def_base *field_def;  // 字段定义基类
    PT_table_constraint_def *opt_column_constraint;  // 可选列约束定义
    const char *opt_place;  // 可选位置

  public:
    PT_column_def(const POS &, const LEX_STRING &, PT_field_def_base *, PT_table_constraint_def *, const char *);
    virtual bool do_contextualize(context_t *);  // 执行上下文化
}
```

# PT_table_element 类定义
```cpp
class PT_table_element : public Parse_tree_node_tmpl<Table_ddl_parse_context> {
  protected:
    PT_table_element(const POS &);
}
```
# Table_ddl_node 类定义
```cpp
typedef Parse_tree_node_tmpl<Table_ddl_parse_context> Table_ddl_node;
```
# Parse_tree_node_tmpl 类注释
```cpp
class Parse_tree_node_tmpl<Context> [with Context = Table_ddl_parse_context] {
  private:
    bool contextualized;  // 上下文化标识

  public:
    POS m_pos;  // 位置

  private:
    Parse_tree_node_tmpl(const Parse_tree_node_tmpl<Context> &);  // 拷贝构造函数

  protected:
    Parse_tree_node_tmpl(void);  // 默认构造函数
    Parse_tree_node_tmpl(const POS &);  // 构造函数，带位置参数
    Parse_tree_node_tmpl(const POS &, const POS &);  // 构造函数，带两个位置参数

  private:
    void operator=(const Parse_tree_node_tmpl<Context> &);  // 赋值运算符重载

  public:
    static void * operator new(size_t, MEM_ROOT *, const std::nothrow_t &);  // new运算符重载
    static void operator delete(void *, size_t);  // delete运算符重载
    static void operator delete(void *, MEM_ROOT *, const std::nothrow_t &);  // delete运算符重载

  protected:
    bool begin_parse_tree(Show_parse_tree *);  // 开始解析树
    bool end_parse_tree(Show_parse_tree *);  // 结束解析树
    virtual bool do_contextualize(Context *);  // 执行上下文化
    virtual void add_json_info(Json_object *);  // 添加JSON信息

  public:
    ~Parse_tree_node_tmpl();  // 析构函数
    bool is_contextualized(void) const;  // 是否已上下文化
    virtual bool contextualize(Context *);  // 上下文化
    void error(Context *, const POS &) const;  // 错误处理函数
    void error(Context *, const POS &, const char *) const;  // 错误处理函数，带字符串参数
    void errorf(Context *, const POS &, const char *, ...) const;  // 格式化错误处理函数

    typedef Context context_t;  // 上下文类型定义
}
```

# PT_table_constraint_def 类定义
```cpp
class PT_table_constraint_def : public PT_table_element {
  protected:
    PT_table_constraint_def(const POS &);
}
```

# PT_check_constraint 类定义
```cpp
class PT_check_constraint : public PT_table_constraint_def {
  private:
    Sql_check_constraint_spec cc_spec;  // SQL检查约束规范

  public:
    PT_check_constraint(const POS &, LEX_STRING &, Item *, bool);  // 构造函数
    void set_column_name(const LEX_STRING &);  // 设置列名
    virtual bool do_contextualize(context_t *);  // 执行上下文化
}
```
