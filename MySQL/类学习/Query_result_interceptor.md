- [Query\_result\_interceptor](#query_result_interceptor)
- [Query\_result](#query_result)

# Query_result_interceptor
```cpp
class Query_result_interceptor : public Query_result {
  public:
    Query_result_interceptor(void); /**< 构造函数 */
    virtual uint field_count(const mem_root_deque<Item*> &) const; /**< 返回字段数量 */
    virtual bool send_result_set_metadata(THD *, const mem_root_deque<Item*> &, uint); /**< 发送结果集元数据 */
    virtual bool is_interceptor(void) const; /**< 判断是否为拦截器 */
}
```

# Query_result
```cpp
class Query_result {
  protected:
    Query_expression *unit; /**< 查询表达式单元 */

  public:
    ha_rows estimated_rowcount; /**< 估计的行数 */
    double estimated_cost; /**< 估计的成本 */

    Query_result(void); /**< 构造函数 */
    ~Query_result(); /**< 析构函数 */

    virtual bool needs_file_privilege(void) const; /**< 判断是否需要文件权限 */
    virtual bool change_query_result(THD *, Query_result *); /**< 更改查询结果 */
    virtual bool need_explain_interceptor(void) const; /**< 判断是否需要解释拦截器 */
    virtual bool prepare(THD *, const mem_root_deque<Item*> &, Query_expression *); /**< 准备执行 */
    virtual bool start_execution(THD *); /**< 开始执行 */
    virtual bool create_table_for_query_block(THD *); /**< 为查询块创建表 */
    virtual uint field_count(const mem_root_deque<Item*> &) const; /**< 返回字段数量 */
    virtual bool send_result_set_metadata(THD *, const mem_root_deque<Item*> &, uint); /**< 发送结果集元数据 */
    virtual bool send_data(THD *, const mem_root_deque<Item*> &); /**< 发送数据 */
    virtual bool send_eof(THD *); /**< 发送结束标记 */
    virtual bool check_supports_cursor(void) const; /**< 检查是否支持游标 */
    virtual void abort_result_set(THD *); /**< 中止结果集 */
    virtual bool reset(void); /**< 重置 */
    virtual void cleanup(void); /**< 清理 */
    virtual bool is_interceptor(void) const; /**< 判断是否为拦截器 */
    virtual void set_limit(ha_rows); /**< 设置限制 */
    virtual Server_side_cursor * cursor(void) const; /**< 获取游标 */
}
```