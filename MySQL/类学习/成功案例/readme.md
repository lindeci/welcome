#ifndef CHECK_SQL_SEND_INCLUDED
#define CHECK_SQL_SEND_INCLUDED

#include "sql/protocol.h"
#include "sql/sql_class.h"

// SQL 审核时，返回给客户端的元数据
// 如果不添加 inline，则会报错：下面两个函数在 sql/check_sql_send.h 文件中被定义，同时被 sql_cmd_ddl_table.cc 和 sql_union.cc 引用了，这导致了多次定义。
inline bool check_sql_send_field_metadata(THD *thd) {
    thd->get_protocol()->start_result_metadata(5, Protocol::SEND_NUM_ROWS | Protocol::SEND_EOF, thd->variables.character_set_results);    

    Send_field* my_send_field = new Send_field();
    my_send_field->db_name = "test";
    my_send_field->table_name = "check_sql";
    my_send_field->org_table_name = "check_sql";
    my_send_field->length = 256;
    my_send_field->charsetnr = 255;
    my_send_field->flags = 4097;
    my_send_field->decimals = 0;
    my_send_field->type = MYSQL_TYPE_VARCHAR;
    my_send_field->field = true;

    
    my_send_field->col_name = "schema_name";
    my_send_field->org_col_name = "table_name";
    thd->get_protocol()->start_row();
    thd->get_protocol()->send_field_metadata(my_send_field, thd->variables.character_set_results);
    thd->get_protocol()->end_row();

    my_send_field->col_name = "table_name";
    my_send_field->org_col_name = "table_name";
    thd->get_protocol()->start_row();
    thd->get_protocol()->send_field_metadata(my_send_field, thd->variables.character_set_results);
    thd->get_protocol()->end_row();

    my_send_field->col_name = "column_name";
    my_send_field->org_col_name = "column_name";
    thd->get_protocol()->start_row();
    thd->get_protocol()->send_field_metadata(my_send_field, thd->variables.character_set_results);
    thd->get_protocol()->end_row();

    my_send_field->col_name = "error_info";
    my_send_field->org_col_name = "error_info";
    thd->get_protocol()->start_row();
    thd->get_protocol()->send_field_metadata(my_send_field, thd->variables.character_set_results);
    thd->get_protocol()->end_row();

    my_send_field->col_name = "sql_info";
    my_send_field->org_col_name = "sql_info";
    thd->get_protocol()->start_row();
    thd->get_protocol()->send_field_metadata(my_send_field, thd->variables.character_set_results);
    thd->get_protocol()->end_row();

    thd->get_protocol()->end_result_metadata();
    return true;
}

inline bool check_sql_send_data(THD *thd) {

    for (auto item = thd->lex->m_tmp_check_sql_results->begin(); item != thd->lex->m_tmp_check_sql_results->end(); item++) {
        thd->get_protocol()->start_row();
        thd->get_protocol()->store_string((*item)->database_name, strlen((*item)->database_name), thd->variables.character_set_results);
        thd->get_protocol()->store_string((*item)->table_name, strlen((*item)->table_name), thd->variables.character_set_results);
        thd->get_protocol()->store_string((*item)->column, strlen((*item)->column), thd->variables.character_set_results);
        thd->get_protocol()->store_string((*item)->error, strlen((*item)->error), thd->variables.character_set_results);
        thd->get_protocol()->store_string((*item)->sql_info, strlen((*item)->sql_info), thd->variables.character_set_results);
        thd->inc_sent_row_count(1);
        thd->get_protocol()->end_row();
    }
    return true;
}
#endif /* CHECK_SQL_SEND_INCLUDED */










#ifndef CHECK_SQL_INCLUDED
#define CHECK_SQL_INCLUDED

#include "sql/sql_class.h"
#include "sql/parse_tree_nodes.h"
#include "sql/protocol.h"

bool check_sql(THD *thd, PT_table_element *element, const char* db_name, const char* table_name) {
    // 在线程描述中，设置 m_check_sql_on 为 true
    thd->lex->m_check_sql_on = true;
    // 把 函数参数中的 PT_table_element 类型向下转换为 PT_column_def 类型
    PT_column_def *column = dynamic_cast<PT_column_def*>(element);
    // 检查字段是否允许为 NULL
    if (!sql_check_allow_null)
        if ((column->get_field_def()->type_flags & NOT_NULL_FLAG) != 1) {
            const m_tmp_check_sql_result *error_info = new m_tmp_check_sql_result{
                .database_name = db_name,
                .table_name = table_name,
                .column = column->get_field_ident().str,
                .error = "该字段允许为 NULL",
                .sql_info = strndup(column->m_pos.raw.start, column->m_pos.raw.length())
            };
            thd->lex->m_tmp_check_sql_results->push_back(error_info);
            //-exec p *(((Mem_root_array<const m_tmp_check_sql_result *> *)thd->lex->m_tmp_check_sql_results)->m_array[0])
            //-exec p *(((Mem_root_array<const m_tmp_check_sql_result *> *)thd->lex->m_tmp_check_sql_results)->m_array[1])
        }
    // 检查字段是否允许为 unsigned
    if (!sql_check_allow_unsigned)
        if ((column->get_field_def()->type_flags & UNSIGNED_FLAG)) {
            const m_tmp_check_sql_result *error_info = new m_tmp_check_sql_result{
                .database_name = db_name,
                .table_name = table_name,
                .column = column->get_field_ident().str,
                .error = "该字段允许为 unsigned",
                .sql_info = strndup(column->m_pos.raw.start, column->m_pos.raw.length())
            };
            thd->lex->m_tmp_check_sql_results->push_back(error_info);
        }
    // 检查 varchar 字段是否超长
    if ((column->get_field_def()->type) == MYSQL_TYPE_STRING && atoi(column->get_field_def()->length) > sql_check_char_max_length)
    {
        const m_tmp_check_sql_result *error_info = new m_tmp_check_sql_result{
            .database_name = db_name,
            .table_name = table_name,
            .column = column->get_field_ident().str,
            .error = ("该字段允许长度超过 " + std::to_string(sql_check_char_max_length)).c_str(),
            .sql_info = strndup(column->m_pos.raw.start, column->m_pos.raw.length())
        };
        thd->lex->m_tmp_check_sql_results->push_back(error_info);
    }
    // 检查字段是否有注释
    if (sql_check_column_need_comment)
        if ((column->get_field_def()->comment.length) == 0) {
            const m_tmp_check_sql_result *error_info = new m_tmp_check_sql_result{
                .database_name = db_name,
                .table_name = table_name,
                .column = column->get_field_ident().str,
                .error = "该字段没有 comment",
                .sql_info = strndup(column->m_pos.raw.start, column->m_pos.raw.length())
            };
            thd->lex->m_tmp_check_sql_results->push_back(error_info);
        }
    // 检查字段是否有默认值
    if (sql_check_column_need_default_value && (column->get_field_def()->type == MYSQL_TYPE_STRING || column->get_field_def()->type == MYSQL_TYPE_VARCHAR || column->get_field_def()->type == MYSQL_TYPE_VAR_STRING))
    {
        const m_tmp_check_sql_result *error_info = new m_tmp_check_sql_result{
            .database_name = db_name,
            .table_name = table_name,
            .column = column->get_field_ident().str,
            .error = "该字段没有默认值",
            .sql_info = strndup(column->m_pos.raw.start, column->m_pos.raw.length())
        };
        thd->lex->m_tmp_check_sql_results->push_back(error_info);
    }
    return true;
}
#endif /* CHECK_SQL_INCLUDED */




# sql/mysqld.cc
```cpp

bool opt_table_encryption_privilege_check = false;

bool sql_check = true;
bool sql_check_has_primary = true;
bool sql_check_need_primary = true;
bool sql_check_column_need_comment = true;
bool sql_check_allow_keyword = false;
bool sql_check_need_primary_number = true;
bool sql_check_allow_unsigned = false;
bool sql_check_insert_need_column = true;
bool sql_check_allow_null = false;
bool sql_check_allow_drop_table = true;
int32 sql_check_max_columns_per_index = 6;
bool sql_check_dml_need_where = true;
bool sql_check_column_need_default_value = true;
bool sql_check_allow_drop_database = true;
int32 sql_check_max_indexs_per_table = 8;
bool sql_check_dml_allow_order = true;
int32 sql_check_char_max_length = 255;
bool sql_check_dml_allow_select = true;
```

# sql/mysqld.h
```cpp
extern bool sql_check;
extern bool sql_check_has_primary;
extern bool sql_check_need_primary;
extern bool sql_check_column_need_comment;
extern bool sql_check_allow_keyword;
extern bool sql_check_need_primary_number;
extern bool sql_check_allow_unsigned;
extern bool sql_check_insert_need_column;
extern bool sql_check_allow_null;
extern bool sql_check_allow_drop_table;
extern int32 sql_check_max_columns_per_index;
extern bool sql_check_dml_need_where;
extern bool sql_check_column_need_default_value;
extern bool sql_check_allow_drop_database;
extern int32 sql_check_max_indexs_per_table;
extern bool sql_check_dml_allow_order;
extern int32 sql_check_char_max_length;
extern bool sql_check_dml_allow_select;
```


# sql/sql_cmd_ddl_table.cc
```cpp
      res = mysql_create_like_table(thd, create_table, query_expression_tables,
                                    &create_info);
    } else {
      /* Regular CREATE TABLE */
      // 如果是非用户线程，或者非 SQL 审核状态
      if (thd->thread_id() <= 1 || !sql_check || !thd->lex->m_check_sql_on)
        res = mysql_create_table(thd, create_table, &create_info, &alter_info);
    }
    /* Pop Strict_error_handler */
    if (!lex->is_ignore() && thd->is_strict_mode()) thd->pop_internal_handler();
    if (!res) {
      /* in case of create temp tables if @@session_track_state_change is
         ON then send session state notification in OK packet */
      if (create_info.options & HA_LEX_CREATE_TMP_TABLE &&
          thd->session_tracker.get_tracker(SESSION_STATE_CHANGE_TRACKER)
              ->is_enabled())
        thd->session_tracker.get_tracker(SESSION_STATE_CHANGE_TRACKER)
            ->mark_as_changed(thd, {});
      if (!(thd->thread_id() <= 1 || !sql_check || !thd->lex->m_check_sql_on)){
        check_sql_send_field_metadata(thd);
        check_sql_send_data(thd);
        //my_ok(thd);
        my_eof(thd);
      }else      
      my_ok(thd);
    }
```


struct m_tmp_check_sql_result {
  //数据库名
  const char* database_name;
  //表名
  const char* table_name;
  //字段名
  const char* column;
  //不符合规范的信息
  const char* error;
  //原始 SQL 相关信息
  const char* sql_info;
};


  // m_check_sql_on 为 ture 时表示 THD 刚进行了 SQL 审核，为 false 时表示 按官方流程执行
  bool m_check_sql_on;
  // SQL 审核时，把所有的不符合规范信息存储在 m_tmp_check_sql_results 数组
  Mem_root_array<const m_tmp_check_sql_result *> *m_tmp_check_sql_results = nullptr;

