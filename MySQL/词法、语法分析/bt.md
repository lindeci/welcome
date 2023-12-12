- [说明](#说明)
- [SQL](#sql)
- [LEX::make\_sql\_cmd(Parse\_tree\_root \*parse\_tree)](#lexmake_sql_cmdparse_tree_root-parse_tree)
- [Sql\_cmd \*PT\_select\_stmt::make\_cmd(THD \*thd)](#sql_cmd-pt_select_stmtmake_cmdthd-thd)
- [Parse\_context pc(thd, thd-\>lex-\>current\_query\_block())](#parse_context-pcthd-thd-lex-current_query_block)
- [m\_qe-\>contextualize(\&pc)](#m_qe-contextualizepc)
- [do\_contextualize(pc)](#do_contextualizepc)
- [bool PT\_query\_specification::do\_contextualize(Parse\_context \*pc)](#bool-pt_query_specificationdo_contextualizeparse_context-pc)

# 说明
在 MySQL 源码中，`PT_` 和 `PTI_` 开头的类都与解析树（Parse Tree）有关。

- `PT_` 开头的类：这些类通常与解析树的节点相关。在 MySQL 的源码中，你可能会看到很多以 `PT_` 开头的类，这些类通常代表 SQL 语句中的各种元素，如表达式、查询等。

- `PTI_` 开头的类：这些类是解析过程中的过渡 Item。它们都是继承自 `Parse_tree_item`（也是 Item 的子类）。在解析阶段，这些 `PTI_` 类会被转化成真正意义上的表达式树节点⁶。


# SQL
```SQL
select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func 
from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 

union all 

select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') 
from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 

order by id desc limit 3;
```
# LEX::make_sql_cmd(Parse_tree_root *parse_tree)
```cpp
bool LEX::make_sql_cmd(Parse_tree_root *parse_tree) {
  if (!will_contextualize) return false;

  m_sql_cmd = parse_tree->make_cmd(thd);
  if (m_sql_cmd == nullptr) return true;

  assert(m_sql_cmd->sql_command_code() == sql_command);

  return false;
}
```
```cpp
-exec p typeid(*parse_tree).name()
$20 = 0x6559ce0 <typeinfo name for PT_select_stmt> "14PT_select_stmt"
```
# Sql_cmd *PT_select_stmt::make_cmd(THD *thd)
```cpp
Sql_cmd *PT_select_stmt::make_cmd(THD *thd) {
  Parse_context pc(thd, thd->lex->current_query_block());

  thd->lex->sql_command = m_sql_command;

  if (m_qe->contextualize(&pc)) {
    return nullptr;
  }

  const bool has_into_clause_inside_query_block = thd->lex->result != nullptr;

  if (has_into_clause_inside_query_block && m_into != nullptr) {
    my_error(ER_MULTIPLE_INTO_CLAUSES, MYF(0));
    return nullptr;
  }
  if (contextualize_safe(&pc, m_into)) {
    return nullptr;
  }

  if (pc.finalize_query_expression()) return nullptr;

  if (m_into != nullptr && m_has_trailing_locking_clauses) {
    // Example: ... INTO ... FOR UPDATE;
    push_warning(thd, ER_WARN_DEPRECATED_INNER_INTO);
  } else if (has_into_clause_inside_query_block &&
             thd->lex->unit->is_set_operation()) {
    // Example: ... UNION ... INTO ...;
    if (!m_qe->has_trailing_into_clause()) {
      // Example: ... UNION SELECT * INTO OUTFILE 'foo' FROM ...;
      push_warning(thd, ER_WARN_DEPRECATED_INNER_INTO);
    } else if (m_has_trailing_locking_clauses) {
      // Example: ... UNION SELECT ... FROM ... INTO OUTFILE 'foo' FOR UPDATE;
      push_warning(thd, ER_WARN_DEPRECATED_INNER_INTO);
    }
  }

  DBUG_EXECUTE_IF("ast", Query_term *qn =
                             pc.select->master_query_expression()->query_term();
                  std::ostringstream buf; qn->debugPrint(0, buf);
                  DBUG_PRINT("ast", ("\n%s", buf.str().c_str())););

  if (thd->lex->sql_command == SQLCOM_SELECT)
    return new (thd->mem_root) Sql_cmd_select(thd->lex->result);
  else  // (thd->lex->sql_command == SQLCOM_DO)
    return new (thd->mem_root) Sql_cmd_do(nullptr);
}
```

```json
{
  "Query_tables_list": {
    "sql_command": "SQLCOM_END",
    "query_tables": "0x0",
    "query_tables_last": "0x7fff34004360",
    "query_tables_own_last": "0x0",
    "lock_tables_state": "Query_tables_list::LTS_NOT_LOCKED",
    "table_count": "0",
    "static BINLOG_STMT_UNSAFE_ALL_FLAGS": "67108863",
    "binlog_stmt_flags": "0",
    "stmt_accessed_table_flag": "0",
    "using_match": "false",
    "stmt_unsafe_with_mixed_mode": "false"
  },
  "_vptr.LEX": "0x8526e10 <vtable for LEX+16>",
  "unit": "0x7fff348d5180",
  "query_block": "0x7fff348d5268",
  "all_query_blocks_list": "0x7fff348d5268",
  "m_current_query_block": "0x7fff348d5268",
  "thd": "0x7fff34000da0",  
  "columns": {
    "<base_list>": {
      "first": "0x8a44470 <end_of_list>",
      "last": "0x7fff34004588", 
      "elements": "0"
    },
    "<No data fields>"
  },
},
"type": "0",
"m_sql_cmd": "0x0",
"select_number": "1",
"drop_if_exists": "false",
"grant_if_exists": "false",
"ignore_unknown_user": "false",
"drop_temporary": "false",
"parsing_options": {
  "allows_variable": "true",
  "allows_select_into": "true" 
},
"alter_info": "0x0",
"prepared_stmt_name": {
  "str": "0x0",
  "length": "0"
},
"prepared_stmt_code": {
  "str": "0x0",
  "length": "0"
},
"m_exec_started": "false",
"m_exec_completed": "false",
"sp_current_parsing_ctx": "0x0",
"m_statement_options": "0",
"stmt_definition_begin": "0x0",
"stmt_definition_end": "0x0",
"will_contextualize": "true",
"m_secondary_engine_context": "0x0",
"m_is_replication_deprecated_syntax_used": "false",
"m_was_replication_command_executed": "false",
"rewrite_required": "false"
}
```

# Parse_context pc(thd, thd->lex->current_query_block())
```cpp
-exec p pc
{
  "<Parse_context_base>": {
    "m_show_parse_tree": {
      "_M_t": {
        "<std::__uniq_ptr_impl<Show_parse_tree, std::default_delete<Show_parse_tree> >>": {
          "_M_t": {
            "<std::_Tuple_impl<0, Show_parse_tree*, std::default_delete<Show_parse_tree> >>": {
              "<std::_Tuple_impl<1, std::default_delete<Show_parse_tree> >>": {
                "<std::_Head_base<1, std::default_delete<Show_parse_tree>, true>>": {
                  "_M_head_impl": {
                    "<No data fields>"
                  }
                }
              },
              "<std::_Head_base<0, Show_parse_tree*, false>>": {
                "_M_head_impl": "0x0"
              }
            }  
          }
        }
      }
    },
    "thd": "0x7fff34000da0",
    "mem_root": "0x7fff34003710",
    "select": "0x7fff348d5268",
    "m_stack": {
      "static block_elements": "<optimized out>",
      "m_blocks": "0x7fff3488dec0",
      "m_begin_idx": "8",
      "m_end_idx": "9",
      "m_capacity": "16",
      "m_root": "0x7fff34003710",
      "m_generation": "1"
    }
  }
}
```

# m_qe->contextualize(&pc)
```cpp
  virtual bool contextualize(Context *pc) final {
    // For condition#2 below ... If position is empty, this item was not
    // created in the parser; so don't show it in the parse tree.
    if (pc->m_show_parse_tree == nullptr || this->m_pos.is_empty())
      return do_contextualize(pc);

    Show_parse_tree *tree = pc->m_show_parse_tree.get();

    if (begin_parse_tree(tree)) return true;

    if (do_contextualize(pc)) return true;

    if (end_parse_tree(tree)) return true;

    return false;
  }
```
# do_contextualize(pc)
```cpp
bool PT_query_expression::do_contextualize(Parse_context *pc) {
  pc->m_stack.push_back(
      QueryLevel(pc->mem_root, SC_QUERY_EXPRESSION, m_order != nullptr));  //压栈的主要内容只有SC_QUERY_EXPRESSION？
  if (contextualize_safe(pc, m_with_clause)) //此时m_with_clause为null，导致contextualize_safe直接返回
    return true; /* purecov: inspected */
  
  if (Parse_tree_node::do_contextualize(pc) || m_body->contextualize(pc))  //判断是否可以压栈 || 
    return true;
```

```cpp
bool PT_union::do_contextualize(Parse_context *pc) {
  return contextualize_setop(pc, QT_UNION,
                             m_is_distinct ? SC_UNION_DISTINCT : SC_UNION_ALL);
}
```

```cpp
//在 bool PT_set_operation::contextualize_setop( 中
-exec p *this
{
  "<PT_query_expression_body>": {
    "<Parse_tree_node_tmpl<Parse_context>>": {
      "_vptr.Parse_tree_node_tmpl": "0x860d700 <vtable for PT_union+16>",
      "contextualized": "true",
      "m_pos": {
        "cpp": {
          "start": "0x7fff348d5030 \"select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_I\"...",
          "end": "0x7fff348d5164 \" order by id desc limit 3\""
        },
        "raw": {
          "start": "0x7fff348d4ee0 \"select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_I\"...",
          "end": "0x7fff348d5014 \" order by id desc limit 3\""
        }
      }
    },
    "m_lhs": "0x7fff3488ba78",
    "m_is_distinct": "false",
    "m_rhs": "0x7fff3488da30",
    "m_into": "0x0",
    "m_is_rhs_in_parentheses": "false"
  }
}
```
```cpp
-exec p *m_lhs
{
  "<Parse_tree_node_tmpl<Parse_context>>": {
    "_vptr.Parse_tree_node_tmpl": "0x860d890 <vtable for PT_query_specification+16>",
    "contextualized": "false",
    "m_pos": {
      "cpp": {
        "start": "0x7fff348d5030 \"select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_I\"...",
        "end": "0x7fff348d50c8 \" union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3\""
      },
      "raw": {
        "start": "0x7fff348d4ee0 \"select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_I\"...",
        "end": "0x7fff348d4f78 \" union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3\""
      }
    }
  }
}

-exec p *m_rhs
{
  "<Parse_tree_node_tmpl<Parse_context>>": {
    "_vptr.Parse_tree_node_tmpl": "0x860d890 <vtable for PT_query_specification+16>",
    "contextualized": "false", 
    "m_pos": {
      "cpp": {
        "start": "0x7fff348d50d3 \"select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3\"",
        "end": "0x7fff348d5164 \" order by id desc limit 3\""
      },
      "raw": {
        "start": "0x7fff348d4f83 \"select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3\"",
        "end": "0x7fff348d5014 \" order by id desc limit 3\""
      }
    }
  }
}
```

```cpp
-exec p typeid(*m_lhs).name()
$31 = 0x6559d80 <typeinfo name for PT_query_specification> "22PT_query_specification"
-exec p typeid(*m_rhs).name()
$32 = 0x6559d80 <typeinfo name for PT_query_specification> "22PT_query_specification"
```

# bool PT_query_specification::do_contextualize(Parse_context *pc)
```cpp
-exec p *this

{
  "<PT_query_primary>": {
    "<PT_query_expression_body>": {
      "<Parse_tree_node_tmpl<Parse_context>>": {
        "_vptr.Parse_tree_node_tmpl": "0x860d890 <vtable for PT_query_specification+16>",
        "contextualized": "true",
        "m_pos": {
          "cpp": {
            "start": "0x7fff348d5030 \"select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_I\"...",
            "end": "0x7fff348d50c8 \" union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=8 order by id desc limit 3\""
          },
          "raw": {
            "start": "0x7fff348d4ee0 \"select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_I\"...",
            "end": "0x7fff348d4f78 \" union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=8 order by id desc limit 3\""
          }
        }
      } 
    },
    "opt_hints": "0x0",
    "options": {
      "query_spec_options": "0"
    },
    "item_list": "0x7fff348d57c0",
    "opt_into1": "0x0",
    "m_is_from_clause_implicit": "false",
    "from_clause": {
      "static has_trivial_destructor": "<optimized out>",
      "m_root": "0x7fff34003710",
      "m_array": "0x7fff3488b690",
      "m_size": "1",
      "m_capacity": "20"
    },
    "opt_where_clause": "0x7fff3488b9b0",
    "opt_group_clause": "0x0",
    "opt_having_clause": "0x0",
    "opt_window_clause": "0x0"
  }
}
```
```cpp
-exec p *item_list
{
   <Parse_tree_node_tmpl<Parse_context>> = {
      _vptr.Parse_tree_node_tmpl = 0x860c4e8 <vtable for PT_select_item_list+16>, 
      contextualized = false, 
      m_pos = {
         cpp = {
            start = 0x7fff34522657 "p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THR"..., 
            end = 0x7fff3452269d " from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p."...
         }, 
         raw = {
            start = 0x7fff34522507 "p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THR"..., 
            end = 0x7fff3452254d " from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p."...
         }
      }, 
      value = {
         static block_elements = <optimized out>, 
         m_blocks = 0x7fff34522e40, 
         m_begin_idx = 64, 
         m_end_idx = 70, 
         m_capacity = 128, 
         m_root = 0x7fff34003730, 
         m_generation = 6
      }
   }
}
```

在PT_item_list中
```cpp
  bool do_contextualize(Parse_context *pc) override {
    if (super::do_contextualize(pc)) return true;
    for (Item *&item : value) {
      if (item->itemize(pc, &item)) return true;
    }
    return false;
  }
```
```cpp
-exec p *item

{
   <Parse_tree_node_tmpl<Parse_context>> = {
      _vptr.Parse_tree_node_tmpl = 0x86078d8 <vtable for PTI_expr_with_alias+16>, 
      contextualized = false, 
      m_pos = {
         cpp = {
            start = 0x7fff34522657 "p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THR"..., 
            end = 0x7fff3452265b ",p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_"...
         }, 
         raw = {
            start = 0x7fff34522507 "p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THR"..., 
            end = 0x7fff3452250b ",p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_"...
         }
      }, 
      next_free = 0x0, 
      str_value = {
         m_ptr = 0x0, 
         m_length = 0, 
         m_charset = 0x86f5b20 <my_charset_bin>, 
         m_alloced_length = 0, 
         m_is_alloced = false
      }, 
      collation = {
         collation = 0x86f5b20 <my_charset_bin>, 
         derivation = DERIVATION_COERCIBLE, 
         repertoire = 3
      }, 
      item_name = {
         <Name_string> = {
            <Simple_cstring> = {
               m_str = 0x0, 
               m_length = 0
            }, 
            <No data fields>
         }, 
         m_is_autogenerated = true
      }, 
      orig_name = {
         <Name_string> = {
            <Simple_cstring> = {
               m_str = 0x0, 
               m_length = 0
            }, 
            <No data fields>
         }, 
         m_is_autogenerated = true
      }, 
      max_length = 0, 
      marker = Item::MARKER_NONE, 
      cmp_context = INVALID_RESULT, 
      m_ref_count = 0, 
      m_abandoned = false, 
      is_parser_item = true, 
      is_expensive_cache = -1 '\377', 
      m_data_type = 243 '\363', 
      fixed = false, 
      decimals = 0 '\000', 
      m_nullable = false, 
      null_value = false, 
      unsigned_flag = false, 
      m_is_window_function = false, 
      hidden = false, 
      m_in_check_constraint_exec_ctx = false, 
      static PROP_SUBQUERY = 1 '\001', 
      static PROP_STORED_PROGRAM = 2 '\002', 
      static PROP_AGGREGATION = 4 '\004', 
      static PROP_WINDOW_FUNCTION = 8 '\b', 
      static PROP_ROLLUP_EXPR = 16 '\020', 
      static PROP_GROUPING_FUNC = 32 ' ', 
      m_accum_properties = 0 '\000'
   }
}

```
```cpp
bool PTI_expr_with_alias::do_itemize(Parse_context *pc, Item **res) {
  if (super::do_itemize(pc, res) || expr->itemize(pc, &expr)) return true;
//-exec p *((PTI_expr_with_alias*)this)->expr
  if (alias.str) {
```
```cpp
-exec p *((PTI_expr_with_alias*)this)->expr

{
   <Parse_tree_node_tmpl<Parse_context>> = {
      _vptr.Parse_tree_node_tmpl = 0x854fb00 <vtable for Item_field+16>, 
      contextualized = true, 
      m_pos = {
         cpp = {start = 0x0, end = 0x0}, 
         raw = {start = 0x0, end = 0x0}
      }
   }, 
   next_free = 0x7fff34522c30, 
   str_value = {
      m_ptr = 0x0, 
      m_length = 0, 
      m_charset = 0x86f5b20 <my_charset_bin>, 
      m_alloced_length = 0, 
      m_is_alloced = false
   }, 
   collation = {
      collation = 0x86f5b20 <my_charset_bin>, 
      derivation = DERIVATION_IMPLICIT, 
      repertoire = 3
   }, 
   item_name = {
      <Name_string> = {
         <Simple_cstring> = {
            m_str = 0x7fff34522c28 "id", 
            m_length = 2
         }, 
         <No data fields>
      }, 
      m_is_autogenerated = true
   }, 
   orig_name = {
      <Name_string> = {
         <Simple_cstring> = {
            m_str = 0x0, 
            m_length = 0
         }, 
         <No data fields>
      }, 
      m_is_autogenerated = true
   }, 
   max_length = 0, 
   marker = Item::MARKER_NONE, 
   cmp_context = INVALID_RESULT, 
   m_ref_count = 0, 
   m_abandoned = false, 
   is_parser_item = true, 
   is_expensive_cache = -1 '\377', 
   m_data_type = 243 '\363', 
   fixed = false, 
   decimals = 0 '\000', 
   m_nullable = false, 
   null_value = false, 
   unsigned_flag = false, 
   m_is_window_function = false, 
   hidden = false, 
   m_in_check_constraint_exec_ctx = false, 
   static PROP_SUBQUERY = 1 '\001', 
   static PROP_STORED_PROGRAM = 2 '\002', 
   static PROP_AGGREGATION = 4 '\004', 
   static PROP_WINDOW_FUNCTION = 8 '\b', 
   static PROP_ROLLUP_EXPR = 16 '\020', 
   static PROP_GROUPING_FUNC = 32 ' ', 
   m_accum_properties = 0 '\000'
}

```

```cpp
bool Query_expression::ExecuteIteratorQuery(THD *thd) {
  ……
  mem_root_deque<Item *> *fields = get_field_list();



-exec p (*(*fields)[0])->item_name->m_str
$129 = 0x7fff34522908 "id"
-exec p (*(*fields)[2])->item_name->m_str
$130 = 0x7fff345230f0 "state"
-exec p (*(*fields)[3])->item_name->m_str
$131 = 0x7fff345232b0 "THREAD_ID"
-exec p (*(*fields)[4])->item_name->m_str
$132 = 0x7fff34523478 "THREAD_OS_ID"
-exec p (*(*fields)[5])->item_name->m_str
$133 = 0x7fff348dbd28 "func"
```


```cpp
bool Query_expression::ExecuteIteratorQuery(THD *thd) {
  ……
  mem_root_deque<Item *> *fields = get_field_list();
```

```cpp
-exec p ((Item_field*)(*((Item_func_eq*)(this->slave->m_where_cond))->cmp->left))->item_name->m_str
$182 = 0x7fff3488b710 "id"
*(Item_field*)(*((Item_func_eq*)(this->slave->m_where_cond))->cmp->left))
-exec p *((Item_int*)(*((Item_func_eq*)(this->slave->m_where_cond))->cmp->right))->item_name->m_str
$180 = 53 '5'

-exec p ((Item_field*)(*((Item_func_eq*)(this->slave->next->m_where_cond))->cmp->left))->item_name->m_str
$183 = 0x7fff3488d6c8 "id"
-exec p ((Item_int*)(*((Item_func_eq*)(this->slave->next->m_where_cond))->cmp->right))->item_name->m_str
$184 = 0x7fff3488d7a8 "8"
```

```cpp
Sql_cmd *PT_create_table_stmt::make_cmd(THD *thd) {
 ……
  } else {
    if (opt_table_element_list) {
      for (auto element : *opt_table_element_list) {
        if (element->contextualize(&pc2)) return nullptr;
      }
    }


-exec p *(PT_column_def*)(*(((Mem_root_array<PT_table_element*>)(((Mem_root_array<PT_table_element*> const*)opt_table_element_list)[0]))->m_array))
$219 = {
  <PT_table_element> = {
    <Parse_tree_node_tmpl<Table_ddl_parse_context>> = {
      _vptr.Parse_tree_node_tmpl = 0x860d2a8 <vtable for PT_column_def+16>,
      contextualized = false,
      m_pos = {
        cpp = {
          start = 0x7fff3488b398 "id int primary key)",
          end = 0x7fff3488b3aa ")"
        },
        raw = {
          start = 0x7fff3488b370 "id int primary key)",
          end = 0x7fff3488b382 ")"
        }
      }
    }, <No data fields>}, 
  members of PT_column_def:
  field_ident = {
    str = 0x7fff3488b868 "id",
    length = 2
  },
  field_def = 0x7fff3488b9b0,
  opt_column_constraint = 0x0,
  opt_place = 0x0
}


CREATE TABLE a (
    id INT UNSIGNED AUTO_INCREMENT primary key, -- 无符号整数，自增
    c1 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名', -- 字符串，不为空，字符集为utf8mb4
    c12 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '用户姓名', -- 字符串，不为空，字符集为utf8mb4
    c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'fuck' COMMENT '邮箱地址', -- 字符串，默认为空字符串，字符集为utf8mb4
    c22 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址' -- 字符串，默认为空字符串，字符集为utf8mb4
);

-exec p *(PT_field_def*)((*(PT_column_def*)((PT_table_element *)element))->field_def)
$10 = {<PT_field_def_base> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x85333c0 <vtable for PT_field_def+16>, contextualized = true, m_pos = {cpp = {start = 0x7fff34189048 "INT UNSIGNED AUTO_INCREMENT primary key, \n    c1 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名', \n    c12 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb"..., end = 0x7fff3418906f ", \n    c1 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名', \n    c12 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '用户姓名', \n "...}, raw = {start = 0x7fff34188e68 "INT UNSIGNED AUTO_INCREMENT primary key, \n    c1 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名', \n    c12 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb"..., end = 0x7fff34188e8f ", \n    c1 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名', \n    c12 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '用户姓名', \n "...}}}, type = MYSQL_TYPE_LONG, type_flags = 547, length = 0x0, dec = 0x0, charset = 0x0, has_explicit_collation = false, uint_geom_type = 0, interval_list = 0x0, alter_info_flags = 8, comment = {str = 0x6407d50 "", length = 0}, default_value = 0x0, on_update_value = 0x0, gcol_info = 0x0, default_val_info = 0x0, m_srid = {<std::_Optional_base<unsigned int, true, true>> = {<std::_Optional_base_impl<unsigned int, std::_Optional_base<unsigned int, true, true> >> = {<No data fields>}, _M_payload = {<std::_Optional_payload_base<unsigned int>> = {_M_payload = {_M_empty = {<No data fields>}, _M_value = 2408550287}, _M_engaged = false}, <No data fields>}}, <std::_Enable_copy_move<true, true, true, true, std::optional<unsigned int> >> = {<No data fields>}, <No data fields>}, check_const_spec_list = 0x7fff3418bd88, type_node = 0x7fff341896d0}, opt_attrs = 0x7fff34189750}
547=512+32+2+1

-exec p *(PT_field_def*)((*(PT_column_def*)((PT_table_element *)element))->field_def)
$11 = {<PT_field_def_base> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x85333c0 <vtable for PT_field_def+16>, contextualized = true, m_pos = {cpp = {start = 0x7fff34189079 "VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名', \n    c12 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '用户姓名', \n    c2 VARC"..., end = 0x7fff341890d5 ", \n    c12 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '用户姓名', \n    c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址',"...}, raw = {start = 0x7fff34188e99 "VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名', \n    c12 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '用户姓名', \n    c2 VARC"..., end = 0x7fff34188ef5 ", \n    c12 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '用户姓名', \n    c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址',"...}}}, type = MYSQL_TYPE_VARCHAR, type_flags = 1, length = 0x7fff34189a20 "50", dec = 0x0, charset = 0x884bee0 <my_charset_utf8mb4_unicode_ci>, has_explicit_collation = true, uint_geom_type = 0, interval_list = 0x0, alter_info_flags = 0, comment = {str = 0x7fff34189bc0 "用户姓名", length = 12}, default_value = 0x0, on_update_value = 0x0, gcol_info = 0x0, default_val_info = 0x0, m_srid = {<std::_Optional_base<unsigned int, true, true>> = {<std::_Optional_base_impl<unsigned int, std::_Optional_base<unsigned int, true, true> >> = {<No data fields>}, _M_payload = {<std::_Optional_payload_base<unsigned int>> = {_M_payload = {_M_empty = {<No data fields>}, _M_value = 2408550287}, _M_engaged = false}, <No data fields>}}, <std::_Enable_copy_move<true, true, true, true, std::optional<unsigned int> >> = {<No data fields>}, <No data fields>}, check_const_spec_list = 0x7fff3418c428, type_node = 0x7fff34189a30}, opt_attrs = 0x7fff34189ad0}

-exec p *(PT_field_def*)((*(PT_column_def*)((PT_table_element *)element))->field_def)
$12 = {<PT_field_def_base> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x85333c0 <vtable for PT_field_def+16>, contextualized = true, m_pos = {cpp = {start = 0x7fff341890e0 "VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '用户姓名', \n    c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址', \n    c22 V"..., end = 0x7fff34189133 ", \n    c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址', \n    c22 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT ", <incomplete sequence \351\202>...}, raw = {start = 0x7fff34188f00 "VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '用户姓名', \n    c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址', \n    c22 V"..., end = 0x7fff34188f53 ", \n    c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址', \n    c22 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT ", <incomplete sequence \351\202>...}}}, type = MYSQL_TYPE_VARCHAR, type_flags = 0, length = 0x7fff34189d30 "50", dec = 0x0, charset = 0x884bee0 <my_charset_utf8mb4_unicode_ci>, has_explicit_collation = true, uint_geom_type = 0, interval_list = 0x0, alter_info_flags = 0, comment = {str = 0x7fff34189ea0 "用户姓名", length = 12}, default_value = 0x0, on_update_value = 0x0, gcol_info = 0x0, default_val_info = 0x0, m_srid = {<std::_Optional_base<unsigned int, true, true>> = {<std::_Optional_base_impl<unsigned int, std::_Optional_base<unsigned int, true, true> >> = {<No data fields>}, _M_payload = {<std::_Optional_payload_base<unsigned int>> = {_M_payload = {_M_empty = {<No data fields>}, _M_value = 2408550287}, _M_engaged = false}, <No data fields>}}, <std::_Enable_copy_move<true, true, true, true, std::optional<unsigned int> >> = {<No data fields>}, <No data fields>}, check_const_spec_list = 0x7fff3418c948, type_node = 0x7fff34189d40}, opt_attrs = 0x7fff34189de0}

-exec p *(PT_field_def*)((*(PT_column_def*)((PT_table_element *)element))->field_def)
$13 = {<PT_field_def_base> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x85333c0 <vtable for PT_field_def+16>, contextualized = true, m_pos = {cpp = {start = 0x7fff3418913d "VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址', \n    c22 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址"..., end = 0x7fff3418919c ", \n    c22 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址' \n)"}, raw = {start = 0x7fff34188f5d "VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址', \n    c22 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址"..., end = 0x7fff34188fbc ", \n    c22 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址' \n)"}}}, type = MYSQL_TYPE_VARCHAR, type_flags = 0, length = 0x7fff3418a010 "100", dec = 0x0, charset = 0x884bee0 <my_charset_utf8mb4_unicode_ci>, has_explicit_collation = true, uint_geom_type = 0, interval_list = 0x0, alter_info_flags = 0, comment = {str = 0x7fff3418a298 "邮箱地址", length = 12}, default_value = 0x7fff3418a188, on_update_value = 0x0, gcol_info = 0x0, default_val_info = 0x0, m_srid = {<std::_Optional_base<unsigned int, true, true>> = {<std::_Optional_base_impl<unsigned int, std::_Optional_base<unsigned int, true, true> >> = {<No data fields>}, _M_payload = {<std::_Optional_payload_base<unsigned int>> = {_M_payload = {_M_empty = {<No data fields>}, _M_value = 2408550287}, _M_engaged = false}, <No data fields>}}, <std::_Enable_copy_move<true, true, true, true, std::optional<unsigned int> >> = {<No data fields>}, <No data fields>}, check_const_spec_list = 0x7fff3418ce68, type_node = 0x7fff3418a020}, opt_attrs = 0x7fff3418a0c0}

-exec p *(PT_field_def*)((*(PT_column_def*)((PT_table_element *)element))->field_def)
$14 = {<PT_field_def_base> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x85333c0 <vtable for PT_field_def+16>, contextualized = true, m_pos = {cpp = {start = 0x7fff341891a7 "VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址' \n)", end = 0x7fff34189206 " \n)"}, raw = {start = 0x7fff34188fc7 "VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱地址' \n)", end = 0x7fff34189026 " \n)"}}}, type = MYSQL_TYPE_VARCHAR, type_flags = 0, length = 0x7fff3418a408 "100", dec = 0x0, charset = 0x884bee0 <my_charset_utf8mb4_unicode_ci>, has_explicit_collation = true, uint_geom_type = 0, interval_list = 0x0, alter_info_flags = 0, comment = {str = 0x7fff3418a690 "邮箱地址", length = 12}, default_value = 0x7fff3418a580, on_update_value = 0x0, gcol_info = 0x0, default_val_info = 0x0, m_srid = {<std::_Optional_base<unsigned int, true, true>> = {<std::_Optional_base_impl<unsigned int, std::_Optional_base<unsigned int, true, true> >> = {<No data fields>}, _M_payload = {<std::_Optional_payload_base<unsigned int>> = {_M_payload = {_M_empty = {<No data fields>}, _M_value = 2408550287}, _M_engaged = false}, <No data fields>}}, <std::_Enable_copy_move<true, true, true, true, std::optional<unsigned int> >> = {<No data fields>}, <No data fields>}, check_const_spec_list = 0x7fff3418d388, type_node = 0x7fff3418a418}, opt_attrs = 0x7fff3418a4b8}


CREATE TABLE a (
    c22 int UNSIGNED,
    c23 int
);
-exec p *(PT_field_def*)((*(PT_column_def*)((PT_table_element *)element))->field_def)
$15 = {<PT_field_def_base> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x85333c0 <vtable for PT_field_def+16>, contextualized = true, m_pos = {cpp = {start = 0x7fff340a80b1 "int UNSIGNED,\n    c23 int\n)", end = 0x7fff340a80bd ",\n    c23 int\n)"}, raw = {start = 0x7fff340a8079 "int UNSIGNED,\n    c23 int\n)", end = 0x7fff340a8085 ",\n    c23 int\n)"}}}, type = MYSQL_TYPE_LONG, type_flags = 32, length = 0x0, dec = 0x0, charset = 0x0, has_explicit_collation = false, uint_geom_type = 0, interval_list = 0x0, alter_info_flags = 0, comment = {str = 0x6407d50 "", length = 0}, default_value = 0x0, on_update_value = 0x0, gcol_info = 0x0, default_val_info = 0x0, m_srid = {<std::_Optional_base<unsigned int, true, true>> = {<std::_Optional_base_impl<unsigned int, std::_Optional_base<unsigned int, true, true> >> = {<No data fields>}, _M_payload = {<std::_Optional_payload_base<unsigned int>> = {_M_payload = {_M_empty = {<No data fields>}, _M_value = 2408550287}, _M_engaged = false}, <No data fields>}}, <std::_Enable_copy_move<true, true, true, true, std::optional<unsigned int> >> = {<No data fields>}, <No data fields>}, check_const_spec_list = 0x7fff340a9eb8, type_node = 0x7fff340a8590}, opt_attrs = 0x0}

-exec p *(PT_field_def*)((*(PT_column_def*)((PT_table_element *)element))->field_def)
$16 = {<PT_field_def_base> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x85333c0 <vtable for PT_field_def+16>, contextualized = true, m_pos = {cpp = {start = 0x7fff340a80c7 "int\n)", end = 0x7fff340a80ca "\n)"}, raw = {start = 0x7fff340a808f "int\n)", end = 0x7fff340a8092 "\n)"}}}, type = MYSQL_TYPE_LONG, type_flags = 0, length = 0x0, dec = 0x0, charset = 0x0, has_explicit_collation = false, uint_geom_type = 0, interval_list = 0x0, alter_info_flags = 0, comment = {str = 0x6407d50 "", length = 0}, default_value = 0x0, on_update_value = 0x0, gcol_info = 0x0, default_val_info = 0x0, m_srid = {<std::_Optional_base<unsigned int, true, true>> = {<std::_Optional_base_impl<unsigned int, std::_Optional_base<unsigned int, true, true> >> = {<No data fields>}, _M_payload = {<std::_Optional_payload_base<unsigned int>> = {_M_payload = {_M_empty = {<No data fields>}, _M_value = 2408550287}, _M_engaged = false}, <No data fields>}}, <std::_Enable_copy_move<true, true, true, true, std::optional<unsigned int> >> = {<No data fields>}, <No data fields>}, check_const_spec_list = 0x7fff34189250, type_node = 0x7fff340a87c0}, opt_attrs = 0x0}



-exec p *(PT_field_def*)((*(PT_column_def*)(*(((Mem_root_array<PT_table_element*>)(((Mem_root_array<PT_table_element*> const*)opt_table_element_list)[0]))->m_array)))->field_def)
$9 = {<PT_field_def_base> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x85333c0 <vtable for PT_field_def+16>, contextualized = false, m_pos = {cpp = {start = 0x7fff341493f0 "INT UNSIGNED AUTO_INCREMENT primary key,      c1 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名',      c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb"..., end = 0x7fff34149417 ",      c1 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名',      c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱"...}, raw = {start = 0x7fff341492d8 "INT UNSIGNED AUTO_INCREMENT primary key,      c1 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名',      c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb"..., end = 0x7fff341492ff ",      c1 VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名',      c2 VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '邮箱"...}}}, type = MYSQL_TYPE_INVALID, type_flags = 0, length = 0x0, dec = 0x0, charset = 0x0, has_explicit_collation = false, uint_geom_type = 0, interval_list = 0x0, alter_info_flags = 0, comment = {str = 0x6407d50 "", length = 0}, default_value = 0x0, on_update_value = 0x0, gcol_info = 0x0, default_val_info = 0x0, m_srid = {<std::_Optional_base<unsigned int, true, true>> = {<std::_Optional_base_impl<unsigned int, std::_Optional_base<unsigned int, true, true> >> = {<No data fields>}, _M_payload = {<std::_Optional_payload_base<unsigned int>> = {_M_payload = {_M_empty = {<No data fields>}, _M_value = 2408550287}, _M_engaged = false}, <No data fields>}}, <std::_Enable_copy_move<true, true, true, true, std::optional<unsigned int> >> = {<No data fields>}, <No data fields>}, check_const_spec_list = 0x0, type_node = 0x7fff341499b0}, opt_attrs = 0x7fff34149a30}

```

```cpp
CREATE TABLE a (     c22 int UNSIGNED,     c23 int not null);

-exec p *(PT_field_def*)((*(PT_column_def*)((PT_table_element *)element))->field_def)
$17 = {<PT_field_def_base> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x85333c0 <vtable for PT_field_def+16>, contextualized = true, m_pos = {cpp = {start = 0x7fff34188ebf "int not null)", end = 0x7fff34188ecb ")"}, raw = {start = 0x7fff34188e7f "int not null)", end = 0x7fff34188e8b ")"}}}, type = MYSQL_TYPE_LONG, type_flags = 1, length = 0x0, dec = 0x0, charset = 0x0, has_explicit_collation = false, uint_geom_type = 0, interval_list = 0x0, alter_info_flags = 0, comment = {str = 0x6407d50 "", length = 0}, default_value = 0x0, on_update_value = 0x0, gcol_info = 0x0, default_val_info = 0x0, m_srid = {<std::_Optional_base<unsigned int, true, true>> = {<std::_Optional_base_impl<unsigned int, std::_Optional_base<unsigned int, true, true> >> = {<No data fields>}, _M_payload = {<std::_Optional_payload_base<unsigned int>> = {_M_payload = {_M_empty = {<No data fields>}, _M_value = 2408550287}, _M_engaged = false}, <No data fields>}}, <std::_Enable_copy_move<true, true, true, true, std::optional<unsigned int> >> = {<No data fields>}, <No data fields>}, check_const_spec_list = 0x7fff3418b2c8, type_node = 0x7fff341895c0}, opt_attrs = 0x7fff34189640}
```


```cpp
# include "sql/sql_class.h"
# include "sql/parse_tree_nodes.h"
/*
class PT_field_def_base : public Parse_tree_node_tmpl<Parse_context> {
  public:
    enum_field_types type;  // 枚举字段类型 {比如 MYSQL_TYPE_LONG、MYSQL_TYPE_VARCHAR、MYSQL_TYPE_TIMESTAMP 等}
    ulong type_flags;  // 类型标志 {1:NOT NULL 0:NULL ABLE}
    const char *length;  // 长度
    const char *dec;  // 小数位数
    const CHARSET_INFO *charset;  // 字符集信息
    bool has_explicit_collation;  // 是否有显式排序规则
    uint uint_geom_type;  // 无符号几何类型
    List<String> *interval_list;  // 区间列表
    alter_info_flags_t alter_info_flags;  // 修改信息标志
    LEX_CSTRING comment;  // 注释
    Item *default_value;  // 默认值
    Item *on_update_value;  // 更新时的值
    Value_generator *gcol_info;  // 值生成器信息
    Value_generator *default_val_info;  // 默认值信息
    std::optional<unsigned int> m_srid;  // 空间参考标识
    Sql_check_constraint_spec_list *check_const_spec_list;  // SQL检查约束规范列表
  protected:
    PT_type *type_node;  // 类型节点

    PT_field_def_base(const POS &, PT_type *);  // 带参数的构造函数
  public:
    virtual bool do_contextualize(Parse_context *);  // 上下文化函数

  private:
    typedef ulonglong alter_info_flags_t;  // 修改信息标志类型别名
}
*/
/*
#define NOT_NULL_FLAG 1     /**< Field can't be NULL */
#define PRI_KEY_FLAG 2      /**< Field is part of a primary key */
#define UNIQUE_KEY_FLAG 4   /**< Field is part of a unique key */
#define MULTIPLE_KEY_FLAG 8 /**< Field is part of a key */
#define BLOB_FLAG 16        /**< Field is a blob */
#define UNSIGNED_FLAG 32    /**< Field is unsigned */
#define ZEROFILL_FLAG 64    /**< Field is zerofill */
#define BINARY_FLAG 128     /**< Field is binary   */

/* The following are only sent to new clients */
#define ENUM_FLAG 256              /**< field is an enum */
#define AUTO_INCREMENT_FLAG 512    /**< field is a autoincrement field */
#define TIMESTAMP_FLAG 1024        /**< Field is a timestamp */
#define SET_FLAG 2048              /**< field is a set */
#define NO_DEFAULT_VALUE_FLAG 4096 /**< Field doesn't have default value */
#define ON_UPDATE_NOW_FLAG 8192    /**< Field is set to NOW on UPDATE */
#define NUM_FLAG 32768             /**< Field is num (for clients) */
#define PART_KEY_FLAG 16384        /**< Intern; Part of some key */
#define GROUP_FLAG 32768           /**< Intern: Group field */
#define UNIQUE_FLAG 65536          /**< Intern: Used by sql_yacc */
#define BINCMP_FLAG 131072         /**< Intern: Used by sql_yacc */
#define GET_FIXED_FIELDS_FLAG                                                  \
  (1 << 18)                               /**< Used to get fields in item tree \
                                           */
#define FIELD_IN_PART_FUNC_FLAG (1 << 19) /**< Field part of partition func */
/**
  Intern: Field in TABLE object for new version of altered table,
          which participates in a newly added index.
*
#define FIELD_IN_ADD_INDEX (1 << 20)
#define FIELD_IS_RENAMED (1 << 21)   /**< Intern: Field is being renamed */
#define FIELD_FLAGS_STORAGE_MEDIA 22 /**< Field storage media, bit 22-23 */
#define FIELD_FLAGS_STORAGE_MEDIA_MASK (3 << FIELD_FLAGS_STORAGE_MEDIA)
#define FIELD_FLAGS_COLUMN_FORMAT 24 /**< Field column format, bit 24-25 */
#define FIELD_FLAGS_COLUMN_FORMAT_MASK (3 << FIELD_FLAGS_COLUMN_FORMAT)
#define FIELD_IS_DROPPED (1 << 26) /**< Intern: Field is being dropped */
#define EXPLICIT_NULL_FLAG                        \
  (1 << 27) /**< Field is explicitly specified as \
               NULL by the user */
/* 1 << 28 is unused. */

/** Field will not be loaded in secondary engine. */
#define NOT_SECONDARY_FLAG (1 << 29)
/** Field is explicitly marked as invisible by the user. */
#define FIELD_IS_INVISIBLE (1 << 30)
*/

bool check_sql(THD thd,PT_table_element element) {
    PT_column_def column = dynamic_cast<*PT_column_def>element;
    if (!sql_check_allow_null)
        if (column->field_def->type_flags & NOT_NULL_FLAG != 1) {
            //异常：出现为空
        }
    if (!sql_check_allow_unsigned)
        if (column->field_def->type_flags & UNSIGNED_FLAG == 1) {
            //异常：出现unsigned
        }
    if (column->field_def->type == MYSQL_TYPE_STRING && column->field_def->length > sql_check_char_max_length)
    {
        //异常：char字段超长
    }
    if (sql_check_column_need_comment)
        if (column->field_def->comment->length == 0) {
            //异常：字段的注释为空
        }
    if (sql_check_column_need_default_value && (column->field_def->type == MYSQL_TYPE_STRING || column->field_def->type == MYSQL_TYPE_VARCHAR || column->field_def->type == MYSQL_TYPE_VAR_STRING))
    {
        //异常：字符串字段存在为空
    }
    return true;
}

/*
enum enum_field_types {
  MYSQL_TYPE_DECIMAL,
  MYSQL_TYPE_TINY,
  MYSQL_TYPE_SHORT,
  MYSQL_TYPE_LONG,
  MYSQL_TYPE_FLOAT,
  MYSQL_TYPE_DOUBLE,
  MYSQL_TYPE_NULL,
  MYSQL_TYPE_TIMESTAMP,
  MYSQL_TYPE_LONGLONG,
  MYSQL_TYPE_INT24,
  MYSQL_TYPE_DATE,
  MYSQL_TYPE_TIME,
  MYSQL_TYPE_DATETIME,
  MYSQL_TYPE_YEAR,
  MYSQL_TYPE_NEWDATE, /**< Internal to MySQL. Not used in protocol */
  MYSQL_TYPE_VARCHAR,
  MYSQL_TYPE_BIT,
  MYSQL_TYPE_TIMESTAMP2,
  MYSQL_TYPE_DATETIME2,   /**< Internal to MySQL. Not used in protocol */
  MYSQL_TYPE_TIME2,       /**< Internal to MySQL. Not used in protocol */
  MYSQL_TYPE_TYPED_ARRAY, /**< Used for replication only */
  MYSQL_TYPE_INVALID = 243,
  MYSQL_TYPE_BOOL = 244, /**< Currently just a placeholder */
  MYSQL_TYPE_JSON = 245,
  MYSQL_TYPE_NEWDECIMAL = 246,
  MYSQL_TYPE_ENUM = 247,
  MYSQL_TYPE_SET = 248,
  MYSQL_TYPE_TINY_BLOB = 249,
  MYSQL_TYPE_MEDIUM_BLOB = 250,
  MYSQL_TYPE_LONG_BLOB = 251,
  MYSQL_TYPE_BLOB = 252,
  MYSQL_TYPE_VAR_STRING = 253,
  MYSQL_TYPE_STRING = 254,
  MYSQL_TYPE_GEOMETRY = 255
};

*/
enum enum_field_types {
  MYSQL_TYPE_DECIMAL,       /**< 十进制数 */
  MYSQL_TYPE_TINY,          /**< 超小整数 */
  MYSQL_TYPE_SHORT,         /**< 短整数 */
  MYSQL_TYPE_LONG,          /**< 长整数 */
  MYSQL_TYPE_FLOAT,         /**< 单精度浮点数 */
  MYSQL_TYPE_DOUBLE,        /**< 双精度浮点数 */
  MYSQL_TYPE_NULL,          /**< 空值 */
  MYSQL_TYPE_TIMESTAMP,     /**< 时间戳 */
  MYSQL_TYPE_LONGLONG,      /**< 长长整数 */
  MYSQL_TYPE_INT24,         /**< 24 位整数 */
  MYSQL_TYPE_DATE,          /**< 日期 */
  MYSQL_TYPE_TIME,          /**< 时间 */
  MYSQL_TYPE_DATETIME,      /**< 日期时间 */
  MYSQL_TYPE_YEAR,          /**< 年份 */
  MYSQL_TYPE_NEWDATE,       /**< MySQL 内部使用，不在协议中使用 */
  MYSQL_TYPE_VARCHAR,       /**< 可变长度字符串 */
  MYSQL_TYPE_BIT,           /**< 位字段 */
  MYSQL_TYPE_TIMESTAMP2,    /**< MySQL 内部使用，不在协议中使用 */
  MYSQL_TYPE_DATETIME2,     /**< MySQL 内部使用，不在协议中使用 */
  MYSQL_TYPE_TIME2,         /**< MySQL 内部使用，不在协议中使用 */
  MYSQL_TYPE_TYPED_ARRAY,   /**< 仅用于复制 */
  MYSQL_TYPE_INVALID = 243, /**< 无效类型 */
  MYSQL_TYPE_BOOL = 244,    /**< 目前只是一个占位符 */
  MYSQL_TYPE_JSON = 245,    /**< JSON 类型 */
  MYSQL_TYPE_NEWDECIMAL = 246, /**< 新的十进制数 */
  MYSQL_TYPE_ENUM = 247,    /**< 枚举 */
  MYSQL_TYPE_SET = 248,     /**< 集合 */
  MYSQL_TYPE_TINY_BLOB = 249, /**< 超小 BLOB 类型 */
  MYSQL_TYPE_MEDIUM_BLOB = 250, /**< 中等 BLOB 类型 */
  MYSQL_TYPE_LONG_BLOB = 251, /**< 长 BLOB 类型 */
  MYSQL_TYPE_BLOB = 252,   /**< BLOB 类型 */
  MYSQL_TYPE_VAR_STRING = 253, /**< 可变长度字符串 */
  MYSQL_TYPE_STRING = 254,  /**< 字符串 */
  MYSQL_TYPE_GEOMETRY = 255  /**< 几何类型 */
};

```

```cpp
bool Query_expression::ExecuteIteratorQuery(THD *thd) {
  THD_STAGE_INFO(thd, stage_executing);
  DEBUG_SYNC(thd, "before_join_exec");

  Opt_trace_context *const trace = &thd->opt_trace;
  Opt_trace_object trace_wrapper(trace);
  Opt_trace_object trace_exec(trace, "join_execution");
  if (is_simple()) {
    trace_exec.add_select_number(first_query_block()->select_number);
  }
  Opt_trace_array trace_steps(trace, "steps");

  if (ClearForExecution()) {
    return true;
  }

  mem_root_deque<Item *> *fields = get_field_list();
  if (thd->m_check_sql_on) {
    fields = new (thd->mem_root) mem_root_deque<Item *>(thd->mem_root);
  }
  Query_result *query_result = this->query_result();
  assert(query_result != nullptr);

  if (query_result->start_execution(thd)) return true;

  if (query_result->send_result_set_metadata(
          thd, *fields, Protocol::SEND_NUM_ROWS | Protocol::SEND_EOF)) {
    return true;
  }

  set_executed();

  // Hand over the query to the secondary engine if needed.
  if (first_query_block()->join->override_executor_func != nullptr) {
    thd->current_found_rows = 0;
    for (Query_block *select = first_query_block(); select != nullptr;
         select = select->next_query_block()) {
      if (select->join->override_executor_func(select->join, query_result)) {
        return true;
      }
      thd->current_found_rows += select->join->send_records;
    }
    const bool calc_found_rows =
        (first_query_block()->active_options() & OPTION_FOUND_ROWS);
    if (!calc_found_rows) {
      // This is for backwards compatibility reasons only;
      // we have documented that without SQL_CALC_FOUND_ROWS,
      // we return the actual number of rows returned.
      thd->current_found_rows =
          std::min(thd->current_found_rows, select_limit_cnt);
    }
    return query_result->send_eof(thd);
  }

  if (item != nullptr) {
    item->reset_has_values();

    if (item->is_value_assigned()) {
      item->reset_value_assigned();  // Prepare for re-execution of this unit
      item->reset();
    }
  }

  // We need to accumulate in the first join's send_records as long as
  // we support SQL_CALC_FOUND_ROWS, since LimitOffsetIterator will use it
  // for reporting rows skipped by OFFSET or LIMIT. When we get rid of
  // SQL_CALC_FOUND_ROWS, we can use a local variable here instead.
  ha_rows *send_records_ptr;
  if (is_simple()) {
    // Not a UNION: found_rows() applies to the join.
    // LimitOffsetIterator will write skipped OFFSET rows into the JOIN's
    // send_records, so use that.
    send_records_ptr = &first_query_block()->join->send_records;
  } else if (set_operation()->m_is_materialized) {
    send_records_ptr = &query_term()->query_block()->join->send_records;
  } else {
    // UNION, but without a fake_query_block (may or may not have a
    // LIMIT): found_rows() applies to the outermost block. See
    // Query_expression::send_records for more information.
    send_records_ptr = &send_records;
  }
  *send_records_ptr = 0;

  thd->get_stmt_da()->reset_current_row_for_condition();

  {
    auto join_cleanup = create_scope_guard([this, thd] {
      for (Query_block *sl = first_query_block(); sl;
           sl = sl->next_query_block()) {
        JOIN *join = sl->join;
        join->join_free();
        thd->inc_examined_row_count(join->examined_rows);
      }
      if (!is_simple() && set_operation()->m_is_materialized)
        thd->inc_examined_row_count(
            query_term()->query_block()->join->examined_rows);
    });

    if (m_root_iterator->Init()) {
      return true;
    }

    PFSBatchMode pfs_batch_mode(m_root_iterator.get());

    for (;;) {
      int error = m_root_iterator->Read();
      DBUG_EXECUTE_IF("bug13822652_1", thd->killed = THD::KILL_QUERY;);

      if (error > 0 || thd->is_error())  // Fatal error
        return true;
      else if (error < 0)
        break;
      else if (thd->killed)  // Aborted by user
      {
        thd->send_kill_message();
        return true;
      }

      ++*send_records_ptr;

      if (query_result->send_data(thd, *fields)) {
        return true;
      }
      thd->get_stmt_da()->inc_current_row_for_condition();
    }

    // NOTE: join_cleanup must be done before we send EOF, so that we get the
    // row counts right.
  }

  thd->current_found_rows = *send_records_ptr;

  return query_result->send_eof(thd);
}
```
```cpp
-exec p *(Item_field*)((*fields)[0])
$16 = {
  <Item_ident> = {
    <Item> = {
      <Parse_tree_node_tmpl<Parse_context>> = {
        _vptr.Parse_tree_node_tmpl = 0x854fb00 <vtable for Item_field+16>,
        contextualized = true,
        m_pos = {
          cpp = {
            start = 0x0,
            end = 0x0
          },
          raw = {
            start = 0x0,
            end = 0x0
          }
        }
      }, 
      members of Item:
      next_free = 0x7fff34113208,
      str_value = {
        m_ptr = 0x0,
        m_length = 0,
        m_charset = 0x86f5b20 <my_charset_bin>,
        m_alloced_length = 0,
        m_is_alloced = false
      },
      collation = {
        collation = 0x884ffe0 <my_charset_utf8mb4_0900_ai_ci>,
        derivation = DERIVATION_IMPLICIT,
        repertoire = 3
      },
      item_name = {
        <Name_string> = {
          <Simple_cstring> = {
            m_str = 0x7fff34a444d0 "Variable_name",
            m_length = 13
          }, <No data fields>}, 
        members of Item_name_string:
        m_is_autogenerated = true
      },
      orig_name = {
        <Name_string> = {
          <Simple_cstring> = {
            m_str = 0x0,
            m_length = 0
          }, <No data fields>}, 
        members of Item_name_string:
        m_is_autogenerated = true
      },
      max_length = 256,
      marker = Item::MARKER_NONE,
      cmp_context = INVALID_RESULT,
      m_ref_count = 1,
      m_abandoned = false,
      is_parser_item = false,
      is_expensive_cache = -1 '\377',
      m_data_type = 15 '\017',
      fixed = true,
      decimals = 31 '\037',
      m_nullable = false,
      null_value = false,
      unsigned_flag = false,
      m_is_window_function = false,
      hidden = false,
      m_in_check_constraint_exec_ctx = false,
      static PROP_SUBQUERY = 1 '\001',
      static PROP_STORED_PROGRAM = 2 '\002',
      static PROP_AGGREGATION = 4 '\004',
      static PROP_WINDOW_FUNCTION = 8 '\b',
      static PROP_ROLLUP_EXPR = 16 '\020',
      static PROP_GROUPING_FUNC = 32 ' ',
      m_accum_properties = 0 '\000'
    }, 
    members of Item_ident:
    m_orig_db_name = 0x7fff341127a0 "performance_schema",
    m_orig_table_name = 0x7fff341127b8 "session_variables",
    m_orig_field_name = 0x7fff34a444d0 "Variable_name",
    m_alias_of_expr = false,
    context = 0x7fff34111d30,
    db_name = 0x6383b60 "",
    table_name = 0x659c4fd "session_variables",
    field_name = 0x7fff34a444d0 "Variable_name",
    cached_table = 0x7fff34a40570,
    depended_from = 0x0
  }, 
  members of Item_field:
  table_ref = 0x7fff34a40570,
  field = 0x7fff34a42b28,
  result_field = 0x7fff34a42b28,
  last_org_destination_field = 0x0,
  last_destination_field = 0x0,
  last_org_destination_field_memcpyable = 4294967295,
  last_destination_field_memcpyable = 4294967295,
  m_base_item_field = 0x0,
  m_protected_by_any_value = false,
  item_equal = 0x0,
  field_index = 0,
  item_equal_all_join_nests = 0x0,
  no_constant_propagation = false,
  have_privileges = 0,
  any_privileges = false,
  can_use_prefix_key = false
}
-exec p *(Item_field*)((*fields)[1])
$17 = {
  <Item_ident> = {
    <Item> = {
      <Parse_tree_node_tmpl<Parse_context>> = {
        _vptr.Parse_tree_node_tmpl = 0x854fb00 <vtable for Item_field+16>,
        contextualized = true,
        m_pos = {
          cpp = {
            start = 0x0,
            end = 0x0
          },
          raw = {
            start = 0x0,
            end = 0x0
          }
        }
      }, 
      members of Item:
      next_free = 0x7fff34a44360,
      str_value = {
        m_ptr = 0x0,
        m_length = 0,
        m_charset = 0x86f5b20 <my_charset_bin>,
        m_alloced_length = 0,
        m_is_alloced = false
      },
      collation = {
        collation = 0x884ffe0 <my_charset_utf8mb4_0900_ai_ci>,
        derivation = DERIVATION_IMPLICIT,
        repertoire = 3
      },
      item_name = {
        <Name_string> = {
          <Simple_cstring> = {
            m_str = 0x7fff34a44650 "Value",
            m_length = 5
          }, <No data fields>}, 
        members of Item_name_string:
        m_is_autogenerated = true
      },
      orig_name = {
        <Name_string> = {
          <Simple_cstring> = {
            m_str = 0x0,
            m_length = 0
          }, <No data fields>}, 
        members of Item_name_string:
        m_is_autogenerated = true
      },
      max_length = 4096,
      marker = Item::MARKER_NONE,
      cmp_context = INVALID_RESULT,
      m_ref_count = 1,
      m_abandoned = false,
      is_parser_item = false,
      is_expensive_cache = -1 '\377',
      m_data_type = 15 '\017',
      fixed = true,
      decimals = 31 '\037',
      m_nullable = true,
      null_value = false,
      unsigned_flag = false,
      m_is_window_function = false,
      hidden = false,
      m_in_check_constraint_exec_ctx = false,
      static PROP_SUBQUERY = 1 '\001',
      static PROP_STORED_PROGRAM = 2 '\002',
      static PROP_AGGREGATION = 4 '\004',
      static PROP_WINDOW_FUNCTION = 8 '\b',
      static PROP_ROLLUP_EXPR = 16 '\020',
      static PROP_GROUPING_FUNC = 32 ' ',
      m_accum_properties = 0 '\000'
    }, 
    members of Item_ident:
    m_orig_db_name = 0x7fff341127a0 "performance_schema",
    m_orig_table_name = 0x7fff341127b8 "session_variables",
    m_orig_field_name = 0x7fff34a44650 "Value",
    m_alias_of_expr = false,
    context = 0x7fff34111d30,
    db_name = 0x6383b60 "",
    table_name = 0x659c4fd "session_variables",
    field_name = 0x7fff34a44650 "Value",
    cached_table = 0x7fff34a40570,
    depended_from = 0x0
  }, 
  members of Item_field:
  table_ref = 0x7fff34a40570,
  field = 0x7fff34a42c18,
  result_field = 0x7fff34a42c18,
  last_org_destination_field = 0x0,
  last_destination_field = 0x0,
  last_org_destination_field_memcpyable = 4294967295,
  last_destination_field_memcpyable = 4294967295,
  m_base_item_field = 0x0,
  m_protected_by_any_value = false,
  item_equal = 0x0,
  field_index = 1,
  item_equal_all_join_nests = 0x0,
  no_constant_propagation = false,
  have_privileges = 0,
  any_privileges = false,
  can_use_prefix_key = false
}
```
```cpp
void Field::make_send_field(Send_field *field) const {
  field->db_name = orig_db_name ? orig_db_name : table->s->db.str;
  field->org_table_name = orig_table_name ? orig_table_name : "";
  field->table_name = table->alias;
  field->org_col_name = field_name;
  field->col_name = field_name;
  field->charsetnr = charset()->number;
  field->length = field_length;
  field->type = type();
  field->flags = all_flags();
  if (table->is_nullable()) field->flags &= ~NOT_NULL_FLAG;
  field->decimals = decimals();
  field->field = false;
}
```


