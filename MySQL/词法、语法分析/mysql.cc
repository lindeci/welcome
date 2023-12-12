#ifdef _WIN32
int win_main(int argc, char **argv)
#else
int mysqld_main(int argc, char **argv)
#endif
{
  initialize_stack_direction();

  // Substitute the full path to the executable in argv[0]
  substitute_progpath(argv);
  sysd::notify_connect();
  sysd::notify("STATUS=Server startup in progress\n");

  /*
    Perform basic thread library and malloc initialization,
    to be able to read defaults files and parse options.
  */
  my_progname = argv[0];
  calculate_mysql_home_from_my_progname();

#ifndef _WIN32
#ifdef WITH_PERFSCHEMA_STORAGE_ENGINE
  pre_initialize_performance_schema();
#endif /*WITH_PERFSCHEMA_STORAGE_ENGINE */
  // For windows, my_init() is called from the win specific mysqld_main
  if (my_init())  // init my_sys library & pthreads
  {
    LogErr(ERROR_LEVEL, ER_MYINIT_FAILED);
    flush_error_log_messages();
    return 1;
  }
#endif /* _WIN32 */

  orig_argc = argc;
  orig_argv = argv;
  my_getopt_use_args_separator = true;
  my_defaults_read_login_file = false;
  if (load_defaults(MYSQL_CONFIG_NAME, load_default_groups, &argc, &argv,
                    &argv_alloc)) {
    flush_error_log_messages();
    return 1;
  }

  /* Set data dir directory paths */
  strmake(mysql_real_data_home, get_relative_path(MYSQL_DATADIR),
          sizeof(mysql_real_data_home) - 1);

  /* Must be initialized early for comparison of options name */
  system_charset_info = &my_charset_utf8mb3_general_ci;

  /* Write mysys error messages to the error log. */
  local_message_hook = error_log_print;

  sys_var_init();

#ifdef _WIN32
  if (mysys::is_my_malloc_using_jemalloc()) {
    LogErr(INFORMATION_LEVEL, ER_MY_MALLOC_USING_JEMALLOC);
  } else {
    for (auto &msg : mysys::fetch_jemalloc_initialization_messages()) {
      LogErr(msg.m_severity, ER_MY_MALLOC_USING_JEMALLOC + msg.m_ecode,
             msg.m_message.c_str());
    }
  }
#endif
  /*
   Initialize variables cache for persisted variables, load persisted
   config file and append parse early  read only persisted variables
   to command line options if present.
  */
  bool arg_separator_added = false;
  if (persisted_variables_cache.init(&argc, &argv) ||
      persisted_variables_cache.load_persist_file() ||
      persisted_variables_cache.append_parse_early_variables(
          &argc, &argv, arg_separator_added)) {
    flush_error_log_messages();
    return 1;
  }

  remaining_argc = argc;
  remaining_argv = argv;

  init_variable_default_paths();

  int heo_error;

#ifdef WITH_PERFSCHEMA_STORAGE_ENGINE
  /*
    Initialize the array of performance schema instrument configurations.
  */
  init_pfs_instrument_array();
#endif /* WITH_PERFSCHEMA_STORAGE_ENGINE */

  heo_error = handle_early_options();

  // this is to prevent mtr from accidentally printing this log when it runs
  // mysqld with --verbose --help to extract version info and variable values
  // and when mysqld is run with --validate-config option
  if (!is_help_or_validate_option())
    LogErr(SYSTEM_LEVEL, opt_initialize ? ER_SRV_INIT_START : ER_SRV_START);

  init_sql_statement_names();
  ulong requested_open_files = 0;

  //  Init error log subsystem. This does not actually open the log yet.
  if (init_error_log()) unireg_abort(MYSQLD_ABORT_EXIT);
  if (!opt_validate_config) adjust_related_options(&requested_open_files);

#ifdef WITH_PERFSCHEMA_STORAGE_ENGINE
  if (heo_error == 0) {
    if (!is_help_or_validate_option() && !opt_initialize) {
      int pfs_rc;
      /* Add sizing hints from the server sizing parameters. */
      pfs_param.m_hints.m_table_definition_cache = table_def_size;
      pfs_param.m_hints.m_table_open_cache = table_cache_size;
      pfs_param.m_hints.m_max_connections = max_connections;
      pfs_param.m_hints.m_open_files_limit = requested_open_files;
      pfs_param.m_hints.m_max_prepared_stmt_count = max_prepared_stmt_count;

      pfs_rc = initialize_performance_schema(
          &pfs_param, &psi_thread_hook, &psi_mutex_hook, &psi_rwlock_hook,
          &psi_cond_hook, &psi_file_hook, &psi_socket_hook, &psi_table_hook,
          &psi_mdl_hook, &psi_idle_hook, &psi_stage_hook, &psi_statement_hook,
          &psi_transaction_hook, &psi_memory_hook, &psi_error_hook,
          &psi_data_lock_hook, &psi_system_hook, &psi_tls_channel_hook);
      if ((pfs_rc != 0) && pfs_param.m_enabled) {
        pfs_param.m_enabled = false;
        LogErr(WARNING_LEVEL, ER_PERFSCHEMA_INIT_FAILED);
      }
    }
  }
#endif /* WITH_PERFSCHEMA_STORAGE_ENGINE */

#ifdef WITH_LOCK_ORDER
  if (heo_error == 0) {
    if (lo_param.m_enabled && !opt_help && !opt_initialize) {
      int lo_rc;
      lo_rc = LO_init(&lo_param, &psi_thread_hook, &psi_mutex_hook,
                      &psi_rwlock_hook, &psi_cond_hook, &psi_file_hook,
                      &psi_socket_hook, &psi_table_hook, &psi_mdl_hook,
                      &psi_idle_hook, &psi_stage_hook, &psi_statement_hook,
                      &psi_transaction_hook, &psi_memory_hook);
      if (lo_rc != 0) {
        LogErr(WARNING_LEVEL, ER_LOCK_ORDER_INIT_FAILED);
      }
    }
  }
#endif /* WITH_LOCK_ORDER */

  /*
    Other provider of the instrumentation interface should
    initialize PSI_hook here:
    - HAVE_PSI_INTERFACE is for the instrumentation interface
    - WITH_PERFSCHEMA_STORAGE_ENGINE is for one implementation
      of the interface,
    but there could be alternate implementations, which is why
    these two defines are kept separate.
  */

#ifdef HAVE_PSI_INTERFACE
  /*
    Obtain the current performance schema instrumentation interface,
    if available.
  */

  void *service;

  if (psi_thread_hook != nullptr) {
    service = psi_thread_hook->get_interface(PSI_CURRENT_THREAD_VERSION);
    if (service != nullptr) {
      set_psi_thread_service(service);
    }
  }

  if (psi_mutex_hook != nullptr) {
    service = psi_mutex_hook->get_interface(PSI_CURRENT_MUTEX_VERSION);
    if (service != nullptr) {
      set_psi_mutex_service(service);
    }
  }

  if (psi_rwlock_hook != nullptr) {
    service = psi_rwlock_hook->get_interface(PSI_CURRENT_RWLOCK_VERSION);
    if (service != nullptr) {
      set_psi_rwlock_service(service);
    }
  }

  if (psi_cond_hook != nullptr) {
    service = psi_cond_hook->get_interface(PSI_CURRENT_COND_VERSION);
    if (service != nullptr) {
      set_psi_cond_service(service);
    }
  }

  if (psi_file_hook != nullptr) {
    service = psi_file_hook->get_interface(PSI_CURRENT_FILE_VERSION);
    if (service != nullptr) {
      set_psi_file_service(service);
    }
  }

  if (psi_socket_hook != nullptr) {
    service = psi_socket_hook->get_interface(PSI_CURRENT_SOCKET_VERSION);
    if (service != nullptr) {
      set_psi_socket_service(service);
    }
  }

  if (psi_table_hook != nullptr) {
    service = psi_table_hook->get_interface(PSI_CURRENT_TABLE_VERSION);
    if (service != nullptr) {
      set_psi_table_service(service);
    }
  }

  if (psi_mdl_hook != nullptr) {
    service = psi_mdl_hook->get_interface(PSI_CURRENT_MDL_VERSION);
    if (service != nullptr) {
      set_psi_mdl_service(service);
    }
  }

  if (psi_idle_hook != nullptr) {
    service = psi_idle_hook->get_interface(PSI_CURRENT_IDLE_VERSION);
    if (service != nullptr) {
      set_psi_idle_service(service);
    }
  }

  if (psi_stage_hook != nullptr) {
    service = psi_stage_hook->get_interface(PSI_CURRENT_STAGE_VERSION);
    if (service != nullptr) {
      set_psi_stage_service(service);
    }
  }

  if (psi_statement_hook != nullptr) {
    service = psi_statement_hook->get_interface(PSI_CURRENT_STATEMENT_VERSION);
    if (service != nullptr) {
      set_psi_statement_service(service);
    }
  }

  if (psi_transaction_hook != nullptr) {
    service =
        psi_transaction_hook->get_interface(PSI_CURRENT_TRANSACTION_VERSION);
    if (service != nullptr) {
      set_psi_transaction_service(service);
    }
  }

  if (psi_memory_hook != nullptr) {
    service = psi_memory_hook->get_interface(PSI_CURRENT_MEMORY_VERSION);
    if (service != nullptr) {
      set_psi_memory_service(service);
    }
  }

  if (psi_error_hook != nullptr) {
    service = psi_error_hook->get_interface(PSI_CURRENT_ERROR_VERSION);
    if (service != nullptr) {
      set_psi_error_service(service);
    }
  }

  if (psi_data_lock_hook != nullptr) {
    service = psi_data_lock_hook->get_interface(PSI_CURRENT_DATA_LOCK_VERSION);
    if (service != nullptr) {
      set_psi_data_lock_service(service);
    }
  }

  if (psi_system_hook != nullptr) {
    service = psi_system_hook->get_interface(PSI_CURRENT_SYSTEM_VERSION);
    if (service != nullptr) {
      set_psi_system_service(service);
    }
  }

  if (psi_tls_channel_hook != nullptr) {
    service =
        psi_tls_channel_hook->get_interface(PSI_CURRENT_TLS_CHANNEL_VERSION);
    if (service != nullptr) {
      set_psi_tls_channel_service(service);
    }
  }

  /*
    Now that we have parsed the command line arguments, and have initialized
    the performance schema itself, the next step is to register all the
    server instruments.
  */
  init_server_psi_keys();

  /*
    Now that some instrumentation is in place,
    recreate objects which were initialised early,
    so that they are instrumented as well.
  */
  my_thread_global_reinit();
#endif /* HAVE_PSI_INTERFACE */

  /* This limits ability to configure SSL library through config options */
  if (init_ssl()) {
    flush_error_log_messages();
    exit(MYSQLD_ABORT_EXIT);
  }

  /* Set umask as early as possible */
  umask(((~my_umask) & 0666));

  /*
    Initialize Components core subsystem early on, once we have PSI, which it
    uses. This part doesn't use any more MySQL-specific functionalities but
    error logging and PFS.
  */
  if (component_infrastructure_init()) {
    flush_error_log_messages();
    return 1;
  }

  {
    /* Must be initialized early because it is required by dynamic loader */
    files_charset_info = &my_charset_utf8mb3_general_ci;
    auto keyring_helper = std::make_unique<Plugin_and_data_dir_option_parser>(
        remaining_argc, remaining_argv);

    if (keyring_helper->valid() == false) {
      flush_error_log_messages();
      return 1;
    }

    if (initialize_manifest_file_components()) {
      flush_error_log_messages();
      return 1;
    }

    /*
      If keyring component was loaded through manifest file, services provided
      by such a component should get priority over keyring plugin. That's why
      we have to set defaults before proxy keyring services are loaded.
    */
    set_srv_keyring_implementation_as_default();
  }

  /*
    Append read only persisted variables to command line now.
    Note that if arg separator is already added, it will not
    be added again.
  */
  if (persisted_variables_cache.append_read_only_variables(
          &remaining_argc, &remaining_argv, arg_separator_added, false)) {
    flush_error_log_messages();
    return 1;
  }
  my_getopt_use_args_separator = false;

  /*
    Initialize Performance Schema component services.
  */
#ifdef HAVE_PSI_THREAD_INTERFACE
  if (!is_help_or_validate_option() && !opt_initialize) {
    register_pfs_notification_service();
    register_pfs_resource_group_service();
  }
#endif

  // Initialize the resource group subsystem.
  auto res_grp_mgr = resourcegroups::Resource_group_mgr::instance();
  if (!is_help_or_validate_option() && !opt_initialize) {
    if (res_grp_mgr->init()) {
      LogErr(ERROR_LEVEL, ER_RESOURCE_GROUP_SUBSYSTEM_INIT_FAILED);
      unireg_abort(MYSQLD_ABORT_EXIT);
    }
  }

#ifdef HAVE_PSI_THREAD_INTERFACE
  /* Instrument the main thread */
  PSI_thread *psi = PSI_THREAD_CALL(new_thread)(key_thread_main, 0, nullptr, 0);
  PSI_THREAD_CALL(set_thread_os_id)(psi);
  PSI_THREAD_CALL(set_thread)(psi);
#endif /* HAVE_PSI_THREAD_INTERFACE */

  /* Initialize audit interface globals. Audit plugins are inited later. */
  mysql_audit_initialize();

  Srv_session::module_init();

  /*
    Perform basic query log initialization. Should be called after
    MY_INIT, as it initializes mutexes.
  */
  query_logger.init();

  if (heo_error) {
    /*
      Parsing command line option failed,
      Since we don't have a workable remaining_argc/remaining_argv
      to continue the server initialization, this is as far as this
      code can go.
      This is the best effort to log meaningful messages:
      - messages will be printed to stderr, which is not redirected yet,
      - messages will be printed in the NT event log, for windows.
    */
    flush_error_log_messages();
    /*
      Not enough initializations for unireg_abort()
      Using exit() for windows.
    */
    exit(MYSQLD_ABORT_EXIT);
  }

  if (init_common_variables()) {
    setup_error_log();
    unireg_abort(MYSQLD_ABORT_EXIT);  // Will do exit
  }

  keyring_lockable_init();

  my_init_signals();
  /*
    Install server's my_abort routine to assure my_aborts prints signal info
    sequentially without sudden termination.
  */
  set_my_abort(my_server_abort);

  size_t guardize = 0;
#ifndef _WIN32
  int retval = pthread_attr_getguardsize(&connection_attrib, &guardize);
  assert(retval == 0);
  if (retval != 0) guardize = my_thread_stack_size;
#endif

#if defined(__ia64__) || defined(__ia64)
  /*
    Peculiar things with ia64 platforms - it seems we only have half the
    stack size in reality, so we have to double it here
  */
  guardize = my_thread_stack_size;
#endif

  if (0 != my_thread_attr_setstacksize(&connection_attrib,
                                       my_thread_stack_size + guardize)) {
    assert(false);
  }

  {
    /* Retrieve used stack size;  Needed for checking stack overflows */
    size_t stack_size = 0;
    my_thread_attr_getstacksize(&connection_attrib, &stack_size);

    /* We must check if stack_size = 0 as Solaris 2.9 can return 0 here */
    if (stack_size && stack_size < (my_thread_stack_size + guardize)) {
      LogErr(WARNING_LEVEL, ER_STACKSIZE_UNEXPECTED,
             my_thread_stack_size + guardize, (long)stack_size);
#if defined(__ia64__) || defined(__ia64)
      my_thread_stack_size = stack_size / 2;
#else
      my_thread_stack_size = static_cast<ulong>(stack_size - guardize);
#endif
    }
  }

#ifndef NDEBUG
  test_lc_time_sz();
  srand(static_cast<uint>(time(nullptr)));
#endif

#if !defined(_WIN32)

  if (opt_initialize && opt_daemonize) {
    fprintf(stderr, "Initialize and daemon options are incompatible.\n");
    unireg_abort(MYSQLD_ABORT_EXIT);
  }

  if (opt_daemonize && log_error_dest == disabled_my_option &&
      (isatty(STDOUT_FILENO) || isatty(STDERR_FILENO))) {
    // Just use the default in this case.
    log_error_dest = "";
  }

  if (opt_daemonize && !opt_validate_config) {
    if (chdir("/") < 0) {
      LogErr(ERROR_LEVEL, ER_CANNOT_CHANGE_TO_ROOT_DIR, strerror(errno));
      unireg_abort(MYSQLD_ABORT_EXIT);
    }

    if ((pipe_write_fd = mysqld::runtime::mysqld_daemonize()) < -1) {
      LogErr(ERROR_LEVEL, ER_FAILED_START_MYSQLD_DAEMON);
      unireg_abort(MYSQLD_ABORT_EXIT);
    }

    if (pipe_write_fd < 0) {
      // This is the launching process and the daemon appears to have
      // started ok (Need to call unireg_abort with success here to
      // clean up resources in the launching process.
      unireg_abort(MYSQLD_SUCCESS_EXIT);
    }

    // Need to update the value of current_pid so that it reflects the
    // pid of the daemon (the previous value was set by unireg_init()
    // while still in the launcher process.
    current_pid = static_cast<ulong>(getpid());
  }
#endif

#ifndef _WIN32
  user_info = check_user(mysqld_user);
  if (!user_info.IsVoid()) {
#if HAVE_CHOWN
    if (unlikely(opt_initialize)) {
      /* need to change the owner of the freshly created data directory */
      MY_STAT stat;
      char errbuf[MYSYS_STRERROR_SIZE];
      bool must_chown = true;

      /* fetch the directory's owner */
      if (!my_stat(mysql_real_data_home, &stat, MYF(0))) {
        LogErr(INFORMATION_LEVEL, ER_CANT_STAT_DATADIR, my_errno(),
               my_strerror(errbuf, sizeof(errbuf), my_errno()));
      }
      /* Don't change it if it's already the same as SElinux stops this */
      else if (stat.st_uid == user_info.pw_uid &&
               stat.st_gid == user_info.pw_gid)
        must_chown = false;

      if (must_chown &&
          chown(mysql_real_data_home, user_info.pw_uid, user_info.pw_gid)) {
        LogErr(ERROR_LEVEL, ER_CANT_CHOWN_DATADIR, mysqld_user);
        unireg_abort(1);
      }
    }
#endif

#if defined(HAVE_MLOCKALL) && defined(MCL_CURRENT)
    if (locked_in_memory)  // getuid() == 0 here
      set_effective_user(user_info);
    else
#endif
      set_user(mysqld_user, user_info);
  }
#endif  // !_WIN32

  /*
   initiate key migration if any one of the migration specific
   options are provided.
  */
  if (opt_keyring_migration_source || opt_keyring_migration_destination ||
      migrate_connect_options) {
    int exit_state = MYSQLD_ABORT_EXIT;
    while (true) {
      Migrate_keyring mk;
      my_getopt_skip_unknown = true;
      if (mk.init(remaining_argc, remaining_argv, opt_keyring_migration_source,
                  opt_keyring_migration_destination, opt_keyring_migration_user,
                  opt_keyring_migration_host, opt_keyring_migration_password,
                  opt_keyring_migration_socket, opt_keyring_migration_port,
                  opt_keyring_migration_to_component)) {
        LogErr(ERROR_LEVEL, ER_KEYRING_MIGRATION_FAILED);
        log_error_dest = "stderr";
        flush_error_log_messages();
        break;
      }

      if (mk.execute()) {
        LogErr(ERROR_LEVEL, ER_KEYRING_MIGRATION_FAILED);
        log_error_dest = "stderr";
        flush_error_log_messages();
        break;
      }

      my_getopt_skip_unknown = false;
      LogErr(INFORMATION_LEVEL, ER_KEYRING_MIGRATION_SUCCESSFUL);
      log_error_dest = "stderr";
      flush_error_log_messages();
      exit_state = MYSQLD_SUCCESS_EXIT;
      break;
    }
    unireg_abort(exit_state);
  }

  /*
   We have enough space for fiddling with the argv, continue
  */
  if (!(is_help_or_validate_option()) &&
      my_setwd(mysql_real_data_home, MYF(0))) {
    char errbuf[MYSYS_STRERROR_SIZE];

    LogErr(ERROR_LEVEL, ER_CANT_SET_DATA_DIR, mysql_real_data_home, errno,
           my_strerror(errbuf, sizeof(errbuf), errno));
    unireg_abort(MYSQLD_ABORT_EXIT); /* purecov: inspected */
  }

  /*
   The subsequent calls may take a long time : e.g. innodb log read.
   Thus set the long running service control manager timeout
  */
#if defined(_WIN32)
  if (windows_service) {
    if (setup_service_status_cmd_processed_handle())
      unireg_abort(MYSQLD_ABORT_EXIT);

    char buf[32];
    snprintf(buf, sizeof(buf), "T %lu", slow_start_timeout);
    const Service_status_msg msg(buf);
    send_service_status(msg);
  }
#endif

  /* Determine default TCP port and unix socket name */
  set_ports();

  if (init_server_components()) unireg_abort(MYSQLD_ABORT_EXIT);

  if (!server_id_supplied)
    LogErr(INFORMATION_LEVEL, ER_WARN_NO_SERVERID_SPECIFIED);

  /*
    Add server_uuid to the sid_map.  This must be done after
    server_uuid has been initialized in init_server_auto_options and
    after the binary log (and sid_map file) has been initialized in
    init_server_components().

    No error message is needed: init_sid_map() prints a message.

    Strictly speaking, this is not currently needed when
    opt_bin_log==0, since the variables that gtid_state->init
    initializes are not currently used in that case.  But we call it
    regardless to avoid possible future bugs if gtid_state ever
    needs to do anything else.
  */
  global_sid_lock->wrlock();
  const int gtid_ret = gtid_state->init();
  global_sid_lock->unlock();

  if (gtid_ret) unireg_abort(MYSQLD_ABORT_EXIT);

  if (!opt_initialize && !opt_initialize_insecure) {
    // Initialize executed_gtids from mysql.gtid_executed table.
    if (gtid_state->read_gtid_executed_from_table() == -1) unireg_abort(1);
  }

  if (opt_bin_log) {
    /*
      Initialize GLOBAL.GTID_EXECUTED and GLOBAL.GTID_PURGED from
      gtid_executed table and binlog files during server startup.
    */
    Gtid_set *executed_gtids =
        const_cast<Gtid_set *>(gtid_state->get_executed_gtids());
    Gtid_set *lost_gtids = const_cast<Gtid_set *>(gtid_state->get_lost_gtids());
    Gtid_set *gtids_only_in_table =
        const_cast<Gtid_set *>(gtid_state->get_gtids_only_in_table());
    Gtid_set *previous_gtids_logged =
        const_cast<Gtid_set *>(gtid_state->get_previous_gtids_logged());

    Gtid_set purged_gtids_from_binlog(global_sid_map, global_sid_lock);
    Gtid_set gtids_in_binlog(global_sid_map, global_sid_lock);
    Gtid_set gtids_in_binlog_not_in_table(global_sid_map, global_sid_lock);

    if (mysql_bin_log.init_gtid_sets(
            &gtids_in_binlog, &purged_gtids_from_binlog,
            opt_source_verify_checksum, true /*true=need lock*/,
            nullptr /*trx_parser*/, nullptr /*partial_trx*/,
            true /*is_server_starting*/))
      unireg_abort(MYSQLD_ABORT_EXIT);

    global_sid_lock->wrlock();

    purged_gtids_from_binlog.dbug_print("purged_gtids_from_binlog");
    gtids_in_binlog.dbug_print("gtids_in_binlog");

    if (!gtids_in_binlog.is_empty() &&
        !gtids_in_binlog.is_subset(executed_gtids)) {
      gtids_in_binlog_not_in_table.add_gtid_set(&gtids_in_binlog);
      if (!executed_gtids->is_empty())
        gtids_in_binlog_not_in_table.remove_gtid_set(executed_gtids);
      /*
        Save unsaved GTIDs into gtid_executed table, in the following
        four cases:
          1. the upgrade case.
          2. the case that a slave is provisioned from a backup of
             the master and the slave is cleaned by RESET MASTER
             and RESET SLAVE before this.
          3. the case that no binlog rotation happened from the
             last RESET MASTER on the server before it crashes.
          4. The set of GTIDs of the last binlog is not saved into the
             gtid_executed table if server crashes, so we save it into
             gtid_executed table and executed_gtids during recovery
             from the crash.
      */
      if (gtid_state->save(&gtids_in_binlog_not_in_table) == -1) {
        global_sid_lock->unlock();
        unireg_abort(MYSQLD_ABORT_EXIT);
      }
      executed_gtids->add_gtid_set(&gtids_in_binlog_not_in_table);
    }

    /* gtids_only_in_table= executed_gtids - gtids_in_binlog */
    if (gtids_only_in_table->add_gtid_set(executed_gtids) != RETURN_STATUS_OK) {
      global_sid_lock->unlock();
      unireg_abort(MYSQLD_ABORT_EXIT);
    }
    gtids_only_in_table->remove_gtid_set(&gtids_in_binlog);
    /*
      lost_gtids = executed_gtids -
                   (gtids_in_binlog - purged_gtids_from_binlog)
                 = gtids_only_in_table + purged_gtids_from_binlog;
    */
    assert(lost_gtids->is_empty());
    if (lost_gtids->add_gtid_set(gtids_only_in_table) != RETURN_STATUS_OK ||
        lost_gtids->add_gtid_set(&purged_gtids_from_binlog) !=
            RETURN_STATUS_OK) {
      global_sid_lock->unlock();
      unireg_abort(MYSQLD_ABORT_EXIT);
    }

    /* Prepare previous_gtids_logged for next binlog */
    if (previous_gtids_logged->add_gtid_set(&gtids_in_binlog) !=
        RETURN_STATUS_OK) {
      global_sid_lock->unlock();
      unireg_abort(MYSQLD_ABORT_EXIT);
    }

    /*
      Write the previous set of gtids at this point because during
      the creation of the binary log this is not done as we cannot
      move the init_gtid_sets() to a place before opening the binary
      log. This requires some investigation.

      /Alfranio
    */
    Previous_gtids_log_event prev_gtids_ev(&gtids_in_binlog);

    global_sid_lock->unlock();

    (prev_gtids_ev.common_footer)->checksum_alg =
        static_cast<enum_binlog_checksum_alg>(binlog_checksum_options);

    if (mysql_bin_log.write_event_to_binlog_and_sync(&prev_gtids_ev))
      unireg_abort(MYSQLD_ABORT_EXIT);

    // run auto purge member function. It will evaluate auto purge controls
    // and configuration, calculate which log files are to be purged, and
    // if any file is to be purged, it will purge it. This is all encapsulated
    // insiude the auto purge member function.
    //
    // Note on the DBUG_EVALUATE_IF usage below:
    // - when compiling it out: the condition evaluates to true, thus
    //   mysql_bin_log.auto_purge_at_server_startup() runs
    // - when "expire_logs_always_at_start" is set: evaluates to false,
    //   thus mysql_bin_log.purge_logs_before_date() runs
    // - when "expire_logs_always_at_start" is not set: evaluates to true,
    //   this mysql_bin_log.auto_purge_at_server_startup() runs
    if (DBUG_EVALUATE_IF("expire_logs_always_at_start", false, true))
      mysql_bin_log.auto_purge_at_server_startup();
    else if (expire_logs_days > 0 || binlog_expire_logs_seconds > 0)
      mysql_bin_log.purge_logs_before_date(time(nullptr), true);

    (void)RUN_HOOK(server_state, after_engine_recovery, (nullptr));
  }

  if (init_ssl_communication()) unireg_abort(MYSQLD_ABORT_EXIT);
  if (network_init()) unireg_abort(MYSQLD_ABORT_EXIT);

#ifdef _WIN32
  if (opt_require_secure_transport && !opt_enable_shared_memory &&
      !have_ssl() && !opt_initialize) {
    LogErr(ERROR_LEVEL, ER_TRANSPORTS_WHAT_TRANSPORTS);
    unireg_abort(MYSQLD_ABORT_EXIT);
  }
#endif

  /*
   Initialize my_str_malloc(), my_str_realloc() and my_str_free()
  */
  my_str_malloc = &my_str_malloc_mysqld;
  my_str_free = &my_str_free_mysqld;
  my_str_realloc = &my_str_realloc_mysqld;

  error_handler_hook = my_message_sql;

  bool abort = false;

  /* Save pid of this process in a file */
  if (!opt_initialize) {
    if (create_pid_file()) abort = true;
  }

  /* Read the optimizer cost model configuration tables */
  if (!opt_initialize) reload_optimizer_cost_constants();

  if (
      /*
        Read components table to restore previously installed components. This
        requires read access to mysql.component table.
      */
      (!opt_initialize && mysql_component_infrastructure_init()) ||
      mysql_rm_tmp_tables()) {
    abort = true;
  }

  /* we do want to exit if there are any other unknown options */
  if (remaining_argc > 1) {
    int ho_error;
    struct my_option no_opts[] = {{nullptr, 0, nullptr, nullptr, nullptr,
                                   nullptr, GET_NO_ARG, NO_ARG, 0, 0, 0,
                                   nullptr, 0, nullptr}};
    /*
      We need to eat any 'loose' arguments first before we conclude
      that there are unprocessed options.
    */
    my_getopt_skip_unknown = false;

    if ((ho_error = handle_options(&remaining_argc, &remaining_argv, no_opts,
                                   mysqld_get_one_option)))
      abort = true;
    else {
      /* Add back the program name handle_options removes */
      remaining_argc++;
      remaining_argv--;
      my_getopt_skip_unknown = true;

      if (remaining_argc > 1) {
        LogErr(ERROR_LEVEL, ER_EXCESS_ARGUMENTS, remaining_argv[1]);
        LogErr(INFORMATION_LEVEL, ER_VERBOSE_HINT);
        abort = true;
      }
    }
  }

  if (abort || acl_init(opt_noacl)) {
    if (!abort) LogErr(ERROR_LEVEL, ER_PRIVILEGE_SYSTEM_INIT_FAILED);
    abort = true;
    opt_noacl = true;
  }

  /*
   if running with --initialize, explicitly allocate the memory
   to be used by ACL objects.
  */
  if (opt_initialize) init_acl_memory();

  if (abort || my_tz_init((THD *)nullptr, default_tz_name, opt_initialize) ||
      grant_init(opt_noacl)) {
    set_connection_events_loop_aborted(true);

    delete_pid_file(MYF(MY_WME));

    unireg_abort(MYSQLD_ABORT_EXIT);
  }

  /*
    Bootstrap the dynamic privilege service implementation
  */
  if (dynamic_privilege_init()) {
    LogErr(WARNING_LEVEL, ER_PERSISTENT_PRIVILEGES_BOOTSTRAP);
  }

  /*
    In the case of upgrade, the bootstrap thread would have already initialized
    the structures necessary for federated server from mysql.servers table.
    Hence we need not initialize them again here.
  */
  if (!opt_initialize && (dd::upgrade::no_server_upgrade_required() ||
                          opt_upgrade_mode == UPGRADE_MINIMAL))
    servers_init(nullptr);

  if (!opt_noacl) {
    udf_read_functions_table();
  }

  init_status_vars();
  /* If running with --initialize, do not start replication. */
  if (opt_initialize) opt_skip_replica_start = true;

  check_binlog_cache_size(nullptr);
  check_binlog_stmt_cache_size(nullptr);

  binlog_unsafe_map_init();

  const ReplicaInitializer replica_initializer(
      opt_initialize, opt_skip_replica_start, rpl_channel_filters,
      &opt_replica_skip_errors);

#ifdef WITH_LOCK_ORDER
  if (!opt_initialize) {
    LO_activate();
  }
#endif /* WITH_LOCK_ORDER */

#ifdef WITH_PERFSCHEMA_STORAGE_ENGINE
  initialize_performance_schema_acl(opt_initialize);
#endif /* WITH_PERFSCHEMA_STORAGE_ENGINE */

  initialize_information_schema_acl();

  (void)RUN_HOOK(server_state, after_recovery, (nullptr));

  if (Events::init(opt_noacl || opt_initialize))
    unireg_abort(MYSQLD_ABORT_EXIT);

#ifndef _WIN32
  //  Start signal handler thread.
  start_signal_handler();
#endif
  if (opt_authentication_policy &&
      validate_authentication_policy(opt_authentication_policy)) {
    /* --authentication_policy is set to invalid value */
    LogErr(ERROR_LEVEL, ER_INVALID_AUTHENTICATION_POLICY);
    return 1;
  } else {
    /* update the value */
    update_authentication_policy();
  }
  /* set all persistent options */
  if (persisted_variables_cache.set_persisted_options(false)) {
    LogErr(ERROR_LEVEL, ER_CANT_SET_UP_PERSISTED_VALUES);
    flush_error_log_messages();
    return 1;
  }

  /*
    Invoke the bootstrap thread, if required.
  */
  process_bootstrap();

  /* Initialize command maps */
  init_command_maps();

  /*
    Event must be invoked after error_handler_hook is assigned to
    my_message_sql, otherwise my_message will not cause the event to abort.
  */
  void *argv_p = argv;
  if (mysql_event_tracking_startup_notify(
          AUDIT_EVENT(EVENT_TRACKING_STARTUP_STARTUP),
          static_cast<const char **>(argv_p), argc))
    unireg_abort(MYSQLD_ABORT_EXIT);

#ifdef _WIN32
  create_shutdown_and_restart_thread();
#endif
  if (mysqld_process_must_end_at_startup) {
#if !defined(_WIN32)
    if (opt_daemonize) mysqld::runtime::signal_parent(pipe_write_fd, 1);
#endif
    unireg_abort(MYSQLD_SUCCESS_EXIT);
  }

  start_handle_manager();

  create_compress_gtid_table_thread();

  LogEvent()
      .type(LOG_TYPE_ERROR)
      .subsys(LOG_SUBSYSTEM_TAG)
      .prio(SYSTEM_LEVEL)
      .lookup(ER_SERVER_STARTUP_MSG, my_progname, server_version,
#ifdef HAVE_SYS_UN_H
              (opt_initialize ? "" : mysqld_unix_port),
#else
              "",
#endif
              mysqld_port, MYSQL_COMPILATION_COMMENT_SERVER);

  if (!opt_disable_networking && my_admin_bind_addr_str)
    LogEvent()
        .type(LOG_TYPE_ERROR)
        .subsys(LOG_SUBSYSTEM_TAG)
        .prio(SYSTEM_LEVEL)
        .lookup(ER_SERVER_STARTUP_ADMIN_INTERFACE, my_admin_bind_addr_str,
                mysqld_admin_port, MYSQL_COMPILATION_COMMENT);

#if defined(_WIN32)
  if (windows_service) {
    const Service_status_msg s("R");
    send_service_status(s);
  }
#endif

  server_components_initialized();

  /*
    Set opt_super_readonly here because if opt_super_readonly is set
    in get_option, it will create problem while setting up event scheduler.
  */
  set_super_read_only_post_init();

  DBUG_PRINT("info", ("Block, listening for incoming connections"));

  (void)MYSQL_SET_STAGE(0, __FILE__, __LINE__);

  server_operational_state = SERVER_OPERATING;
  sysd::notify("READY=1\nSTATUS=Server is operational\nMAIN_PID=", getpid(),
               "\n");

  (void)RUN_HOOK(server_state, before_handle_connection, (nullptr));

#if defined(_WIN32)
  if (mysqld_socket_acceptor != nullptr)
    mysqld_socket_acceptor->check_and_spawn_admin_connection_handler_thread();
  setup_conn_event_handler_threads();
#else
  mysql_mutex_lock(&LOCK_socket_listener_active);
  // Make it possible for the signal handler to kill the listener.
  socket_listener_active = true;
  mysql_mutex_unlock(&LOCK_socket_listener_active);

  if (opt_daemonize) {
    if (nstdout != nullptr) {
      // Show the pid on stdout if daemonizing and connected to tty
      fprintf(nstdout, "mysqld is running as pid %lu\n", current_pid);
      fclose(nstdout);
      nstdout = nullptr;
    }

    mysqld::runtime::signal_parent(pipe_write_fd, 1);
  }

  mysqld_socket_acceptor->check_and_spawn_admin_connection_handler_thread();
  mysqld_socket_acceptor->connection_event_loop();
#endif /* _WIN32 */
  server_operational_state = SERVER_SHUTTING_DOWN;
  sysd::notify("STOPPING=1\nSTATUS=Server shutdown in progress\n");

  DBUG_PRINT("info", ("No longer listening for incoming connections"));

  mysql_event_tracking_shutdown_notify(
      AUDIT_EVENT(EVENT_TRACKING_SHUTDOWN_SHUTDOWN),
      EVENT_TRACKING_SHUTDOWN_REASON_SHUTDOWN, MYSQLD_SUCCESS_EXIT);

  terminate_compress_gtid_table_thread();
  /*
    Save set of GTIDs of the last binlog into gtid_executed table
    on server shutdown.
  */
  if (opt_bin_log)
    if (gtid_state->save_gtids_of_last_binlog_into_table())
      LogErr(WARNING_LEVEL, ER_CANT_SAVE_GTIDS);

#ifndef _WIN32
  mysql_mutex_lock(&LOCK_socket_listener_active);
  // Notify the signal handler that we have stopped listening for connections.
  socket_listener_active = false;
  mysql_cond_broadcast(&COND_socket_listener_active);
  mysql_mutex_unlock(&LOCK_socket_listener_active);
#endif  // !_WIN32

#ifdef HAVE_PSI_THREAD_INTERFACE
  /*
    Disable the main thread instrumentation,
    to avoid recording events during the shutdown.
  */
  PSI_THREAD_CALL(delete_current_thread)();
#endif /* HAVE_PSI_THREAD_INTERFACE */

  DBUG_PRINT("info", ("Waiting for shutdown proceed"));
  int ret = 0;
#ifdef _WIN32
  if (shutdown_restart_thr_handle.handle)
    ret = my_thread_join(&shutdown_restart_thr_handle, NULL);
  shutdown_restart_thr_handle.handle = NULL;
  if (0 != ret)
    LogErr(WARNING_LEVEL, ER_CANT_JOIN_SHUTDOWN_THREAD, "shutdown ", ret);
#else
  if (signal_thread_id.thread != 0)
    ret = my_thread_join(&signal_thread_id, nullptr);
  signal_thread_id.thread = 0;
  if (0 != ret)
    LogErr(WARNING_LEVEL, ER_CANT_JOIN_SHUTDOWN_THREAD, "signal_", ret);
#endif  // _WIN32

  clean_up(true);
  mysqld_exit(signal_hand_thr_exit_code);
}