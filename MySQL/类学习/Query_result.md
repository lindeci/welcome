- [Query\_result](#query_result)
- [Query\_result\_interceptor](#query_result_interceptor)

# Query_result
class Query_result {
  protected:
    Query_expression *unit;
  public:
    ha_rows estimated_rowcount;
    double estimated_cost;

    Query_result(void);
    ~Query_result();
    virtual bool needs_file_privilege(void) const;
    virtual bool change_query_result(THD *, Query_result *);
    virtual bool need_explain_interceptor(void) const;
    virtual bool prepare(THD *, const mem_root_deque<Item*> &, Query_expression *);
    virtual bool start_execution(THD *);
    virtual bool create_table_for_query_block(THD *);
    virtual uint field_count(const mem_root_deque<Item*> &) const;
    virtual bool send_result_set_metadata(THD *, const mem_root_deque<Item*> &, uint);
    virtual bool send_data(THD *, const mem_root_deque<Item*> &);
    virtual bool send_eof(THD *);
    virtual bool check_supports_cursor(void) const;
    virtual void abort_result_set(THD *);
    virtual bool reset(void);
    virtual void cleanup(void);
    virtual bool is_interceptor(void) const;
    virtual void set_limit(ha_rows);
    virtual Server_side_cursor * cursor(void) const;
}

# Query_result_interceptor
class Query_result_interceptor : public Query_result {
  public:
    Query_result_interceptor(void);
    virtual uint field_count(const mem_root_deque<Item*> &) const;
    virtual bool send_result_set_metadata(THD *, const mem_root_deque<Item*> &, uint);
    virtual bool is_interceptor(void) const;
}
