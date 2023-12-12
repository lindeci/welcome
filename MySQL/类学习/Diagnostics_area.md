
```cpp
-exec p *da
$18 = {
  m_stacked_da = 0x0,
  m_condition_root = {
    static s_dummy_target = 0 '\000',
    m_current_block = 0x7f30e0136f20,
    m_current_free_start = 0x7f30e0136f30 '\217' <repeats 200 times>...,
    m_current_free_end = 0x7f30e0137730 "\217\217\217\217\217\217\217\217U",
    m_block_size = 3072,
    m_orig_block_size = 2048,
    m_max_capacity = 0,
    m_allocated_size = 2048,
    m_error_for_capacity_exceeded = false,
    m_error_handler = 0x56023e03181f <sql_alloc_error_handler()>,
    m_psi_key = 0
  },
  m_conditions_list = {
    <I_P_List_counter> = {
      m_counter = 0
    }, 
    <I_P_List_fast_push_back<Sql_condition>> = {
      m_last = 0x7f30e0003ad8
    }, 
    members of I_P_List<Sql_condition, I_P_List_adapter<Sql_condition, &Sql_condition::m_next_condition, &Sql_condition::m_prev_condition>, I_P_List_counter, I_P_List_fast_push_back<Sql_condition> >:
    m_first = 0x0
  },
  m_preexisting_sql_conditions = {
    <base_list> = {
      first = 0x560243b9ce30 <end_of_list>,
      last = 0x7f30e0003ae0,
      elements = 0
    }, <No data fields>},
  m_is_sent = false,
  m_can_overwrite_status = false,
  m_allow_unlimited_conditions = false,
  m_status = Diagnostics_area::DA_EOF,
  m_message_text = "Unknown table 'test.ldc'\000; database doesn't exist\000nual that corresponds to your MySQL server version for the right syntax to use near ', c1 int, c2 text,`as` int, index idx(c1,c2))' at line 1", '\000' <repeats 320 times>,
  m_returned_sqlstate = "42S02",
  m_mysql_errno = 1051,
  m_affected_rows = 0,
  m_last_insert_id = 0,
  m_last_statement_cond_count = 0,
  m_current_statement_cond_count = 0,
  m_current_statement_cond_count_by_qb = {0, 0, 0},
  m_current_row_for_condition = 1,
  m_saved_error_count = 0,
  m_saved_warn_count = 0
}
```
# Diagnostics_area
```cpp
class Diagnostics_area {
  private:
    Diagnostics_area *m_stacked_da;
    MEM_ROOT m_condition_root;
    Sql_condition_list m_conditions_list;
    List<Sql_condition const> m_preexisting_sql_conditions;
    bool m_is_sent;
    bool m_can_overwrite_status;
    bool m_allow_unlimited_conditions;
    Diagnostics_area::enum_diagnostics_status m_status;
    char m_message_text[512];
    char m_returned_sqlstate[6];
    uint m_mysql_errno;
    ulonglong m_affected_rows;
    ulonglong m_last_insert_id;
    uint m_last_statement_cond_count;
    uint m_current_statement_cond_count;
    uint m_current_statement_cond_count_by_qb[3];
    ulong m_current_row_for_condition;
    ulong m_saved_error_count;
    ulong m_saved_warn_count;

  public:
    Diagnostics_area(bool);
    ~Diagnostics_area();
    void set_overwrite_status(bool);
    bool is_sent(void) const;
    void set_is_sent(bool);
    void set_ok_status(ulonglong, ulonglong, const char *);
    void set_eof_status(THD *);
    void set_error_status(THD *, uint);
    void set_error_status(uint, const char *, const char *);
    void disable_status(void);
    void reset_diagnostics_area(void);
    bool is_set(void) const;
    bool is_error(void) const;
    bool is_eof(void) const;
    bool is_ok(void) const;
    bool is_disabled(void) const;
    Diagnostics_area::enum_diagnostics_status status(void) const;
    const char * message_text(void) const;
    uint mysql_errno(void) const;
    const char * returned_sqlstate(void) const;
    ulonglong affected_rows(void) const;
    ulonglong last_insert_id(void) const;
    uint last_statement_cond_count(void) const;
    ulong current_statement_cond_count(void) const;
    void reset_statement_cond_count(void);
    bool has_sql_condition(const char *, size_t) const;
    bool has_sql_condition(uint) const;
    void reset_condition_info(THD *);
    ulong current_row_for_condition(void) const;
    void inc_current_row_for_condition(void);
    void set_current_row_for_condition(ulong);
    void reset_current_row_for_condition(void);
    ulong error_count(THD *) const;
    ulong warn_count(THD *) const;
    uint cond_count(void) const;
    Sql_condition_iterator sql_conditions(void) const;
    const char * get_first_condition_message(void);
    void reserve_number_of_conditions(THD *, uint);
    Sql_condition * push_warning(THD *, uint, const char *, Sql_condition::enum_severity_level, const char *);
  private:
    Sql_condition * push_warning(THD *, const Sql_condition *);
  public:
    void mark_preexisting_sql_conditions(void);
    void copy_new_sql_conditions(THD *, const Diagnostics_area *);
    void copy_sql_conditions_from_da(THD *, const Diagnostics_area *);
    void copy_non_errors_from_da(THD *, const Diagnostics_area *);
    Sql_condition * error_condition(void) const;
  private:
    void push_diagnostics_area(THD *, Diagnostics_area *, bool);
    Diagnostics_area * pop_diagnostics_area(void);
    const Diagnostics_area * stacked_da(void) const;

  public:
    typedef I_P_List<Sql_condition, I_P_List_adapter<Sql_condition, &Sql_condition::m_next_condition, &Sql_condition::m_prev_condition>, I_P_List_counter, I_P_List_fast_push_back<Sql_condition> >::Const_Iterator Sql_condition_iterator;
  private:
    typedef I_P_List<Sql_condition, I_P_List_adapter<Sql_condition, &Sql_condition::m_next_condition, &Sql_condition::m_prev_condition>, I_P_List_counter, I_P_List_fast_push_back<Sql_condition> > Sql_condition_list;
}
```