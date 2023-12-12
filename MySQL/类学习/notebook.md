```c
-exec p *(thd->lex)
$87 = {
  <Query_tables_list> = {
    sql_command = SQLCOM_SELECT,
    query_tables = 0x7fff348dc138,
    query_tables_last = 0x7fff348e0780,
    query_tables_own_last = 0x0,
    sroutines = {
      _M_t = {
        <std::__uniq_ptr_impl<malloc_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, Sroutine_hash_entry*, std::hash<std::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::equal_to<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > >, std::default_delete<malloc_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, Sroutine_hash_entry*, std::hash<std::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::equal_to<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > > > >> = {
          _M_t = {
            <std::_Tuple_impl<0, malloc_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, Sroutine_hash_entry*, std::hash<std::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::equal_to<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, std::default_delete<malloc_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, Sroutine_hash_entry*, std::hash<std::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::equal_to<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > > > >> = {
              <std::_Tuple_impl<1, std::default_delete<malloc_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, Sroutine_hash_entry*, std::hash<std::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::equal_to<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > > > >> = {
                <std::_Head_base<1, std::default_delete<malloc_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, Sroutine_hash_entry*, std::hash<std::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::equal_to<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > > >, true>> = {
                  _M_head_impl = {<No data fields>}
                }, <No data fields>}, 
              <std::_Head_base<0, malloc_unordered_map<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, Sroutine_hash_entry*, std::hash<std::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::equal_to<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, false>> = {
                _M_head_impl = 0x0
              }, <No data fields>}, <No data fields>}
        }, <No data fields>}
    },
    sroutines_list = {
      elements = 0,
      first = 0x0,
      next = 0x7fff340043a8
    },
    sroutines_list_own_last = 0x7fff340043a8,
    sroutines_list_own_elements = 0,
    lock_tables_state = Query_tables_list::LTS_LOCKED,
    table_count = 4,
    static BINLOG_STMT_UNSAFE_ALL_FLAGS = 67108863,
    static binlog_stmt_unsafe_errcode = {1668, 1670, 1671, 1672, 1673, 1674, 1675, 1692, 1693, 1714, 1715, 1722, 1716, 1717, 1718, 1723, 1719, 1724, 1727, 3006, 3570, 3571, 3199, 13425, 4010, 4112},
    binlog_stmt_flags = 3,
    stmt_accessed_table_flag = 2,
    using_match = false,
    stmt_unsafe_with_mixed_mode = false
  }, 
  members of LEX:
  _vptr.LEX = 0x8526e10 <vtable for LEX+16>,
  unit = 0x7fff34522480,
  query_block = 0x7fff34522568,
  all_query_blocks_list = 0x7fff348dea38,
  m_current_query_block = 0x7fff34522568,
  is_explain_analyze = false,
  using_hypergraph_optimizer = false,
  name = {
    str = 0x0,
    length = 0
  },
  help_arg = 0x0,
  to_log = 0x0,
  x509_subject = 0x0,
  x509_issuer = 0x0,
  ssl_cipher = 0x0,
  wild = 0x0,
  result = 0x0,
  binlog_stmt_arg = {
    str = 0x0,
    length = 0
  },
  ident = {
    str = 0x0,
    length = 0
  },
  grant_user = 0x0,
  alter_password = {
    update_password_expired_fields = false,
    update_password_expired_column = false,
    use_default_password_lifetime = true,
    expire_after_days = 0,
    update_account_locked_column = false,
    account_locked = false,
    password_history_length = 0,
    use_default_password_history = true,
    update_password_history = false,
    password_reuse_interval = 0,
    use_default_password_reuse_interval = true,
    update_password_reuse_interval = false,
    failed_login_attempts = 0,
    update_failed_login_attempts = false,
    password_lock_time = 0,
    update_password_lock_time = false,
    update_password_require_current = Lex_acl_attrib_udyn::UNCHANGED
  },
  alter_user_attribute = enum_alter_user_attribute::ALTER_USER_COMMENT_NOT_USED,
  alter_user_comment_text = {
    str = 0x0,
    length = 0
  },
  grant_as = {
    grant_as_used = false,
    role_type = role_enum::ROLE_NONE,
    user = 0x0,
    role_list = 0x0
  },
  thd = 0x7fff34000dc0,
  opt_hints_global = 0x0,
  plugins = {
    static Has_trivial_destructor = <optimized out>,
    static initial_capacity = <optimized out>,
    m_psi_key = 0,
    m_inline_size = -1,
    {
      m_ext = {
        m_array_ptr = 0x7fff345c7f50,
        m_alloced_size = 0,
        m_alloced_capacity = 128
      },
      m_buff = {0x7fff345c7f50, 0x0, 0x80, 0x7fff34130e20, 0x7fff3416b790, 0x7fff34170340, 0x7fff341a35f0, 0x7fff3419fe10, 0x7fff341a9c90, 0x7fff341a0d40, 0x7fff341c5380, 0x7fff341c62e0, 0x7fff341df940, 0x7fff341f0290, 0x7fff34213100, 0x7fff341ff2e0}
    }
  },
  insert_table = 0x0,
  insert_table_leaf = 0x0,
  create_view_query_block = {
    str = 0x0,
    length = 0
  },
  part_info = 0x0,
  definer = 0x0,
  users_list = {
    <base_list> = {
      first = 0x8a44470 <end_of_list>,
      last = 0x7fff34004590,
      elements = 0
    }, <No data fields>},
  columns = {
    <base_list> = {
      first = 0x8a44470 <end_of_list>,
      last = 0x7fff340045a8,
      elements = 0
    }, <No data fields>},
  dynamic_privileges = {
    <base_list> = {
      first = 0x8a44470 <end_of_list>,
      last = 0x7fff340045c0,
      elements = 0
    }, <No data fields>},
  default_roles = 0x0,
  bulk_insert_row_cnt = 0,
  purge_value_list = {
    <base_list> = {
      first = 0x8a44470 <end_of_list>,
      last = 0x7fff340045e8,
      elements = 0
    }, <No data fields>},
  kill_value_list = {
    <base_list> = {
      first = 0x8a44470 <end_of_list>,
      last = 0x7fff34004600,
      elements = 0
    }, <No data fields>},
  var_list = {
    <base_list> = {
      first = 0x8a44470 <end_of_list>,
      last = 0x7fff34004618,
      elements = 0
    }, <No data fields>},
  set_var_list = {
    <base_list> = {
      first = 0x8a44470 <end_of_list>,
      last = 0x7fff34004630,
      elements = 0
    }, <No data fields>},
  param_list = {
    <base_list> = {
      first = 0x8a44470 <end_of_list>,
      last = 0x7fff34004648,
      elements = 0
    }, <No data fields>},
  insert_update_values_map = 0x0,
  context_stack = {
    <base_list> = {
      first = 0x7fff345228f0,
      last = 0x7fff345228f0,
      elements = 1
    }, <No data fields>},
  in_sum_func = 0x0,
  udf = {
    name = {
      str = 0x0,
      length = 0
    },
    returns = STRING_RESULT,
    type = 0,
    dl = 0x0,
    dlhandle = 0x0,
    func = 0x0,
    func_init = 0x0,
    func_deinit = 0x0,
    func_clear = 0x0,
    func_add = 0x0,
    usage_count = 0
  },
  check_opt = {
    flags = 0,
    sql_flags = 0,
    key_cache = 0x0
  },
  create_info = 0x0,
  key_create_info = {
    algorithm = HA_KEY_ALG_SE_SPECIFIC,
    is_algorithm_explicit = false,
    block_size = 0,
    parser_name = {
      str = 0x0,
      length = 0
    },
    comment = {
      str = 0x0,
      length = 0
    },
    is_visible = true,
    m_engine_attribute = {
      str = 0x6368790 "",
      length = 0
    },
    m_secondary_engine_attribute = {
      str = 0x6368790 "",
      length = 0
    }
  },
  mi = {
    host = 0x0,
    user = 0x0,
    password = 0x0,
    log_file_name = 0x0,
    bind_addr = 0x0,
    network_namespace = 0x0,
    port = 0,
    connect_retry = 0,
    heartbeat_period = 0,
    sql_delay = 0,
    pos = 0,
    server_id = 0,
    retry_count = 0,
    gtid = 0x0,
    view_id = 0x0,
    channel = 0x0,
    gtid_until_condition = LEX_MASTER_INFO::UNTIL_SQL_BEFORE_GTIDS,
    until_after_gaps = false,
    slave_until = false,
    for_channel = false,
    ssl = LEX_MASTER_INFO::LEX_MI_UNCHANGED,
    ssl_verify_server_cert = LEX_MASTER_INFO::LEX_MI_UNCHANGED,
    heartbeat_opt = LEX_MASTER_INFO::LEX_MI_UNCHANGED,
    repl_ignore_server_ids_opt = LEX_MASTER_INFO::LEX_MI_UNCHANGED,
    retry_count_opt = LEX_MASTER_INFO::LEX_MI_UNCHANGED,
    auto_position = LEX_MASTER_INFO::LEX_MI_UNCHANGED,
    port_opt = LEX_MASTER_INFO::LEX_MI_UNCHANGED,
    get_public_key = LEX_MASTER_INFO::LEX_MI_UNCHANGED,
    m_source_connection_auto_failover = LEX_MASTER_INFO::LEX_MI_UNCHANGED,
    m_gtid_only = LEX_MASTER_INFO::LEX_MI_UNCHANGED,
    ssl_key = 0x0,
    ssl_cert = 0x0,
    ssl_ca = 0x0,
    ssl_capath = 0x0,
    ssl_cipher = 0x0,
    ssl_crl = 0x0,
    ssl_crlpath = 0x0,
    tls_version = 0x0,
    tls_ciphersuites = LEX_MASTER_INFO::UNSPECIFIED,
    tls_ciphersuites_string = 0x0,
    public_key_path = 0x0,
    relay_log_name = 0x0,
    relay_log_pos = 0,
    compression_algorithm = 0x0,
    zstd_compression_level = 0,
    repl_ignore_server_ids = {
      static Has_trivial_destructor = <optimized out>,
      static initial_capacity = <optimized out>,
      m_psi_key = 0,
      m_inline_size = 0,
      {
        m_ext = {
          m_array_ptr = 0x0,
          m_alloced_size = 0,
          m_alloced_capacity = 0
        },
        m_buff = {0, 0}
      }
    },
    privilege_checks_none = false,
    privilege_checks_username = 0x0,
    privilege_checks_hostname = 0x0,
    require_row_format = 0,
    require_table_primary_key_check = LEX_MASTER_INFO::LEX_MI_PK_CHECK_UNCHANGED,
    assign_gtids_to_anonymous_transactions_type = LEX_MASTER_INFO::LEX_MI_ANONYMOUS_TO_GTID_UNCHANGED,
    assign_gtids_to_anonymous_transactions_manual_uuid = 0x0
  },
  slave_connection = {
    user = 0x0,
    password = 0x0,
    plugin_auth = 0x0,
    plugin_dir = 0x0
  },
  server_options = {
    static PORT_NOT_SET = -1,
    m_server_name = {
      str = 0x0,
      length = 0
    },
    m_port = -1,
    m_host = {
      str = 0x0,
      length = 0
    },
    m_db = {
      str = 0x0,
      length = 0
    },
    m_username = {
      str = 0x0,
      length = 0
    },
    m_password = {
      str = 0x0,
      length = 0
    },
    m_scheme = {
      str = 0x0,
      length = 0
    },
    m_socket = {
      str = 0x0,
      length = 0
    },
    m_owner = {
      str = 0x0,
      length = 0
    }
  },
  mqh = {
    questions = 0,
    updates = 0,
    conn_per_hour = 0,
    user_conn = 0,
    specified_limits = 0
  },
  reset_slave_info = {
    all = false
  },
  type = 0,
  allow_sum_func = 0,
  m_deny_window_func = 0,
  m_subquery_to_derived_is_impossible = false,
  m_sql_cmd = 0x7fff348e3fc8,
  expr_allows_subselect = true,
  reparse_common_table_expr_at = 0,
  reparse_derived_table_condition = false,
  reparse_derived_table_params_at = {
    <std::_Vector_base<unsigned int, std::allocator<unsigned int> >> = {
      _M_impl = {
        <std::allocator<unsigned int>> = {
          <__gnu_cxx::new_allocator<unsigned int>> = {<No data fields>}, <No data fields>}, 
        <std::_Vector_base<unsigned int, std::allocator<unsigned int> >::_Vector_impl_data> = {
          _M_start = 0x0,
          _M_finish = 0x0,
          _M_end_of_storage = 0x0
        }, <No data fields>}
    }, <No data fields>},
  ssl_type = SSL_TYPE_NOT_SPECIFIED,
  duplicates = DUP_ERROR,
  tx_isolation = ISO_READ_UNCOMMITTED,
  option_type = OPT_DEFAULT,
  create_view_mode = enum_view_create_mode::VIEW_CREATE_NEW,
  show_profile_query_id = 0,
  profile_options = 0,
  grant = 0,
  grant_tot_col = 0,
  grant_privilege = false,
  slave_thd_opt = 0,
  start_transaction_opt = 0,
  select_number = 3,
  create_view_algorithm = 0 '\000',
  create_view_check = 0 '\000',
  context_analysis_only = 0 '\000',
  drop_if_exists = false,
  grant_if_exists = false,
  ignore_unknown_user = false,
  drop_temporary = false,
  autocommit = false,
  verbose = false,
  no_write_to_binlog = false,
  m_extended_show = false,
  tx_chain = TVL_YES,
  tx_release = TVL_YES,
  safe_to_cache_query = true,
  m_has_udf = false,
  ignore = false,
  parsing_options = {
    allows_variable = true,
    allows_select_into = true
  },
  alter_info = 0x0,
  prepared_stmt_name = {
    str = 0x0,
    length = 0
  },
  prepared_stmt_code = {
    str = 0x0,
    length = 0
  },
  prepared_stmt_code_is_varref = false,
  prepared_stmt_params = {
    <base_list> = {
      first = 0x8a44470 <end_of_list>,
      last = 0x7fff34004a48,
      elements = 0
    }, <No data fields>},
  sphead = 0x0,
  spname = 0x0,
  sp_lex_in_use = false,
  all_privileges = false,
  contains_plaintext_password = false,
  keep_diagnostics = DA_KEEP_NOTHING,
  next_binlog_file_nr = 0,
  m_broken = false,
  m_exec_started = true,
  m_exec_completed = true,
  sp_current_parsing_ctx = 0x0,
  m_statement_options = 0,
  sp_chistics = {
    comment = {
      str = 0x0,
      length = 0
    },
    suid = SP_IS_DEFAULT_SUID,
    detistic = false,
    daccess = SP_DEFAULT_ACCESS,
    language = {
      str = 0x0,
      length = 0
    }
  },
  event_parse_data = 0x0,
  only_view = false,
  create_view_suid = 1 '\001',
  stmt_definition_begin = 0x0,
  stmt_definition_end = 0x0,
  use_only_table_context = false,
  is_lex_started = true,
  in_update_value_clause = false,
  explain_format = 0x0,
  max_execution_time = 0,
  binlog_need_explicit_defaults_ts = false,
  will_contextualize = true,
  m_IS_table_stats = {
    m_key = {
      static npos = <optimized out>,
      _M_dataplus = {
        <Stateless_allocator<char, dd::String_type_alloc, My_free_functor>> = {<No data fields>}, 
        members of std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Alloc_hider:
        _M_p = 0x8a43018 <std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Rep::_S_empty_rep_storage+24> ""
      }
    },
    m_error = {
      static npos = <optimized out>,
      _M_dataplus = {
        <Stateless_allocator<char, dd::String_type_alloc, My_free_functor>> = {<No data fields>}, 
        members of std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Alloc_hider:
        _M_p = 0x8a43018 <std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Rep::_S_empty_rep_storage+24> ""
      }
    },
    m_checksum = 0,
    m_read_stats_by_open = false,
    m_stats = {
      data_file_length = 0,
      max_data_file_length = 0,
      index_file_length = 0,
      max_index_file_length = 0,
      delete_length = 0,
      auto_increment_value = 0,
      records = 0,
      deleted = 0,
      mean_rec_length = 0,
      create_time = 0,
      check_time = 0,
      update_time = 0,
      block_size = 0,
      mrr_length_per_rec = 0,
      table_in_mem_estimate = -1
    }
  },
  m_IS_tablespace_stats = {
    m_key = {
      static npos = <optimized out>,
      _M_dataplus = {
        <Stateless_allocator<char, dd::String_type_alloc, My_free_functor>> = {<No data fields>}, 
        members of std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Alloc_hider:
        _M_p = 0x8a43018 <std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Rep::_S_empty_rep_storage+24> ""
      }
    },
    m_found_error = false,
    m_stats = {
      m_id = 0,
      m_type = {
        static npos = <optimized out>,
        _M_dataplus = {
          <Stateless_allocator<char, dd::String_type_alloc, My_free_functor>> = {<No data fields>}, 
          members of std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Alloc_hider:
          _M_p = 0x8a43018 <std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Rep::_S_empty_rep_storage+24> ""
        }
      },
      m_logfile_group_name = {
        static npos = <optimized out>,
        _M_dataplus = {
          <Stateless_allocator<char, dd::String_type_alloc, My_free_functor>> = {<No data fields>}, 
          members of std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Alloc_hider:
          _M_p = 0x8a43018 <std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Rep::_S_empty_rep_storage+24> ""
        }
      },
      m_logfile_group_number = 18446744073709551615,
      m_free_extents = 0,
      m_total_extents = 0,
      m_extent_size = 0,
      m_initial_size = 0,
      m_maximum_size = 0,
      m_autoextend_size = 0,
      m_version = 18446744073709551615,
      m_row_format = {
        static npos = <optimized out>,
        _M_dataplus = {
          <Stateless_allocator<char, dd::String_type_alloc, My_free_functor>> = {<No data fields>}, 
          members of std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Alloc_hider:
          _M_p = 0x8a43018 <std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Rep::_S_empty_rep_storage+24> ""
        }
      },
      m_data_free = 0,
      m_status = {
        static npos = <optimized out>,
        _M_dataplus = {
          <Stateless_allocator<char, dd::String_type_alloc, My_free_functor>> = {<No data fields>}, 
          members of std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Alloc_hider:
          _M_p = 0x8a43018 <std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Rep::_S_empty_rep_storage+24> ""
        }
      },
      m_extra = {
        static npos = <optimized out>,
        _M_dataplus = {
          <Stateless_allocator<char, dd::String_type_alloc, My_free_functor>> = {<No data fields>}, 
          members of std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Alloc_hider:
          _M_p = 0x8a43018 <std::basic_string<char, std::char_traits<char>, Stateless_allocator<char, dd::String_type_alloc, My_free_functor> >::_Rep::_S_empty_rep_storage+24> ""
        }
      }
    }
  },
  m_secondary_engine_context = 0x0,
  m_is_replication_deprecated_syntax_used = false,
  m_was_replication_command_executed = false,
  rewrite_required = false
}
```