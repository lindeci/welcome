# -*- coding: utf-8 -*-

"""
整体流程：先遍历对象的指针，放在全局的LIST中，同时把连线防盗 g_line 中，
然后先打印对象，再打印连线
"""
import gdb
import sqlparse

BLOCK_ELEMENTS = 128

g_space = 3          # 缩进空间大小
g_bin_len = 16       # 打印二级制的长度
g_gdb_conv = 'g_gdb_conv'    # gdb 时设置的临时变量

g_query_expression_list = []            # 全局 query_expression 的 list，里面的元素是指针
g_query_block_list = []                 # 全局 query_block 的 list，里面的元素是指针
g_query_term_list = []                  # 全局 query_term 的 list，里面的元素是指针, 只存放 ['Query_term_except','Query_term_intersect','Query_term_unary','Query_term_union'] 这4种类型
g_table_ref_list = []                   # 全局 Table_ref 的 list, 里面的元素是指针
g_mem_root_deque__Table_ref__list = []  # 全局 mem_root_deque<Table_ref*> 的 list, 面的元素是指针
g_natural_join_column_list = []         # 全局 Natural_join_column 的 list，里面的元素是指针
g_list__natural_join_column__list = []  # 全局 List<Natural_join_column> *join_columns 的 list，里面的元素是指针
g_Item_field_list = []
g_line = []                             # 遍历对象时，如果两个对象之间有连线，则把连线信息插入这个列表。里面的元素时字符串
g_error = []


# 把 MySQL 源码中的 List 转换为 python 中的 list
# @list List的指针或者值
# 返回 list
def List_to_list(list):
    if list.type.code == gdb.TYPE_CODE_PTR:
        list = list.dereference()
    out_list = []
    nodetype = list.type.template_argument(0)
    first = list['first']
    last = list['last'].dereference()
    elements = list['elements']
    while first != last:
        info = first['info']
        info_dynamic_type = info.cast(nodetype.pointer()).dynamic_type
        out_list.append(info.cast(info_dynamic_type))
        first = first['next']
    return out_list

# 把 MySQL 源码中的 mem_root_deque 转换为 python 中的 list
# @deque mem_root_deque的指针或者值
# 返回 list
def mem_root_deque_to_list(deque):
    if deque.type.code == gdb.TYPE_CODE_PTR:
        deque = deque.dereference()
    out_list = []
    m_begin_idx = deque['m_begin_idx']
    m_end_idx = deque['m_end_idx']
    while m_begin_idx != m_end_idx:
        element = deque['m_blocks'][m_begin_idx / BLOCK_ELEMENTS]['elements'][m_begin_idx % BLOCK_ELEMENTS]
        out_list.append(element)
        m_begin_idx += 1
    return out_list

# 把 MySQL 源码中的 SQL_I_List 转换为 python 中的 list
# @list SQL_I_List的值
# 返回 list
def SQL_I_List_to_list(list, next_key = 'next_local'):
    out_list = []
    elements = list['elements']
    if (elements == 0):
        return out_list
    item = list['first']
    out_list.append(item)
    while elements > 1:
        item = item[next_key]
        out_list.append(item)
        elements -= 1
    return out_list

# 把 MySQL 源码中的 Mem_root_array 转换为 python 中的 list
# @array Mem_root_array的值
# 返回 list
def Mem_root_array_to_list(array):
    if array.type.code == gdb.TYPE_CODE_PTR:
        array = array.dereference()
    out_list = []
    m_size = array.dereference()['m_size']
    for i in range(m_size):
        out_list.append(array.dereference()['m_array'][i])
    return out_list


def table_ref_to_list(table_ref, next_key):
    out_list = []
    while table_ref:
        out_list.append(table_ref)
        table_ref = table_ref.dereference()[next_key]
    return out_list

class MysqlCommand(gdb.Command):
    def __init__(self):
        super(MysqlCommand, self).__init__(
            "mysql", gdb.COMMAND_USER, prefix=True)

# 打印 Query_expression
# @expr Query_expression的指针或者对象
def display_Query_expression(expr):
    if expr.type.code == gdb.TYPE_CODE_PTR:
        expr = expr.dereference()

    for key, value in expr.address.items():
        print(f"    {key} => {value}")

    print(f"map Query_expression_{str(expr.address)} #header:lightblue {{")
    print(f"    master => {expr['master']}")
    print(f"    slave => {expr['slave']}")
    print(f"    next => {expr['next']}")
    if expr['prev'] != 0x0:
        print(f"    prev.dereference => {expr['prev'].dereference()}")
    else:
        print(f"    prev.dereference => {expr['prev']}")
    print(f"    m_query_term => {expr['m_query_term']}")
    print(f"    select_limit_cnt => {expr['select_limit_cnt']}")
    print(f"    offset_limit_cnt => {expr['offset_limit_cnt']}")
    print(f"    prepared => {expr['prepared']}")
    print(f"    optimized => {expr['optimized']}")
    print(f"    executed => {expr['executed']}")
    print(f"}}")
    
    print(f"note right of Query_expression_{str(expr.address)}")
    gdb.set_convenience_variable(g_gdb_conv,expr.address)
    gdb.execute('call thd->gdb_str.set("", 0, system_charset_info)')
    gdb.execute('call $g_gdb_conv->print(thd, &(thd->gdb_str), QT_ORDINARY)')
    gdb_str = gdb.parse_and_eval('thd->gdb_str.c_ptr_safe()').string()
    formatted_sql = sqlparse.format(gdb_str, reindent=True, keyword_case='upper')
    print(f"{formatted_sql}")
    print(f"end note")
    print()

# 打印 Query_block
# @block Query_block的指针或者对象
def display_Query_block(block):
    if block.type.code == gdb.TYPE_CODE_PTR:
        block = block.dereference()
    print(f"map Query_block_{str(block.address)} #header:gold {{")
    print(f"    master => {block['master']}")
    print(f"    slave => {block['slave']}")
    print(f"    next => {block['next']}")
    if block['link_prev'] != 0x0:
        print(f"    link_prev.dereference => {block['link_prev'].dereference()}")
    else:
        print(f"    link_prev.dereference => {block['link_prev']}")    
    if (block['select_limit'] != 0x0):
        print(f"    select_limit => {block['select_limit'].cast(block['select_limit'].dynamic_type).dereference()['value']}")
    else:
        print(f"    select_limit => 0x0")
    if (block['offset_limit'] != 0x0):
        print(f"    offset_limit => {block['offset_limit'].cast(block['offset_limit'].dynamic_type).dereference()['value']}")
    else:
        print(f"    offset_limit => 0x0")
    
    print(f"    m_table_list => {block['m_table_list'].address}")    
    print(f"    leaf_tables => {block['leaf_tables']}")
    print(f"    m_table_nest => {block['m_table_nest'].address}")

    print(f"    sj_nests => {block['sj_nests'].address}")
    print(f"    order_list => {block['order_list'].address}")
    print(f"    select_list_tables => {block['select_list_tables']}")
    print(f"    outer_join => {block['outer_join']}")
    print(f"    join => {block['join'].address}")
    print(f"    m_current_table_nest => {block['m_current_table_nest']}")
    print(f"    cond_value => {block['cond_value']}")
    print(f"    having_value => {block['having_value']}")

    print(f"    m_where_cond => {block['m_where_cond']}")
    print(f"    m_having_cond => {block['m_having_cond']}")
    print(f"    has_sj_nests => {block['has_sj_nests']}")
    print(f"    has_aj_nests => {block['has_aj_nests']}")
    print(f"    m_right_joins => {block['m_right_joins']}")

    print(f"}}")

    print(f"note right of Query_block_{str(block.address)}")
    gdb.set_convenience_variable(g_gdb_conv,block.address)
    gdb.execute('call thd->gdb_str.set("", 0, system_charset_info)')
    gdb.execute('call $g_gdb_conv->print(thd, &(thd->gdb_str), QT_ORDINARY)')
    gdb_str = gdb.parse_and_eval('thd->gdb_str.c_ptr_safe()').string()
    formatted_sql = sqlparse.format(gdb_str, reindent=True, keyword_case='upper')
    print(f"{formatted_sql}")
    print(f"end note")
    print()

    
    if (block['m_table_list'].address != 0x0):
        print(f"map SQL_I_List__Table_ref_{block['m_table_list'].address} {{")
        for i in SQL_I_List_to_list(block['m_table_list'], 'next_local'):
            print(f"    {i} => {i.dynamic_type}")
        print(f"}}")

# 打印 Query_term，包含子类的 Query_term_except、Query_term_intersect、Query_term_unary、Query_term_union，不包含 Query_block
# @term Query_term的指针或者对象
def display_Query_term(term):
    if term.type.code == gdb.TYPE_CODE_PTR:
        term = term.dereference()
    dynamic_type = term.dynamic_type
    if str(dynamic_type) in ['Query_term_except','Query_term_intersect','Query_term_unary','Query_term_union']:
        new_term = term.cast(dynamic_type)        
        print(f"map Query_term_{str(new_term.address)} #header:lightgreen {{")
        print(f"    __dynamic_type => {dynamic_type}")
        print(f"    m_block => {new_term['m_block']}")
        print(f"    m_children => {new_term['m_children'].address}")
        print(f"    m_last_distinct => {new_term['m_last_distinct']}")
        print(f"    m_first_distinct => {new_term['m_first_distinct']}")
        print(f"    m_is_materialized => {new_term['m_is_materialized']}")
        print(f"}}")

        m_children_list = mem_root_deque_to_list(new_term['m_children'])
        print(f"map mem_root_deque__Query_term_{new_term['m_children'].address} #header:pink {{")
        for i in m_children_list:
            if i.type.code == gdb.TYPE_CODE_PTR:
                i = i.dereference()
            print(f"    {i.address} => {i.dynamic_type}")
        print(f"}}")

        for i in m_children_list:
            if i not in g_query_term_list and i not in g_query_block_list:
                g_query_term_list.append(i)
                display_Query_term(i)

    else:
        print("dynamic_type type error in display_Query_term_set_op.")

# 打印 Table_ref
# @term Query_term的指针或者对象
def display_Table_ref(table_ref):
    if table_ref.type.code == gdb.TYPE_CODE_PTR:
        table_ref = table_ref.dereference()
    print(f"map Table_ref_{table_ref.address} {{")
    if table_ref['db'] != 0x0:
        print(f"    db => {table_ref['db'].string()}")
    if table_ref['table_name'] != 0x0:
        print(f"    table_name => {table_ref['table_name'].string()}")
    if table_ref['alias'] != 0x0:
        print(f"    alias => {table_ref['alias'].string()}")
    print(f"    m_tableno => {table_ref['m_tableno']}")
    print(f"    next_local => {table_ref['next_local']}")
    print(f"    next_leaf => {table_ref['next_leaf']}")
    print(f"    partition_names => {table_ref['partition_names']}")
    print(f"    index_hints => {table_ref['index_hints']}")
    print(f"    view => {table_ref['view']}")
    print(f"    derived => {table_ref['derived']}")
    print(f"    schema_table => {table_ref['schema_table']}")
    print(f"    effective_algorithm => {table_ref['effective_algorithm']}")
    print(f"    field_translation => {table_ref['field_translation']}")
    print(f"    natural_join => {table_ref['natural_join']}")
    print(f"    join_using_fields => {table_ref['join_using_fields']}")
    print(f"    m_join_cond => {table_ref['m_join_cond']}")
    print(f"    m_is_sj_or_aj_nest => {table_ref['m_is_sj_or_aj_nest']}")
    print(f"    sj_inner_tables => {table_ref['sj_inner_tables']}")
    print(f"    is_natural_join => {table_ref['is_natural_join']}")
    print(f"    join_using_fields => {table_ref['join_using_fields']}")
    print(f"    join_columns => {table_ref['join_columns']}")
    print(f"    is_join_columns_complete => {table_ref['is_join_columns_complete']}")
    print(f"    join_order_swapped => {table_ref['join_order_swapped']}")
    print(f"    straight => {table_ref['straight']}")
    print(f"    join_cond_dep_tables => {table_ref['join_cond_dep_tables']}")
    print(f"    nested_join => {table_ref['nested_join']}")
    print(f"    embedding => {table_ref['embedding']}")
    print(f"    join_list => {table_ref['join_list']}")
    print(f"    m_join_cond_optim => {table_ref['m_join_cond_optim']}")
    print(f"    cond_equal => {table_ref['cond_equal']}")
    print(f"}}")

    print(f"note right of Table_ref_{str(table_ref.address)}")
    gdb.set_convenience_variable(g_gdb_conv,table_ref.address)
    gdb.execute('call thd->gdb_str.set("", 0, system_charset_info)')
    gdb.execute('call $g_gdb_conv->print(thd, &(thd->gdb_str), QT_ORDINARY)')
    gdb_str = gdb.parse_and_eval('thd->gdb_str->m_ptr').string()
    #formatted_sql = sqlparse.format(gdb_str, reindent=True, keyword_case='upper')
    print(f"{gdb_str}")
    print(f"end note")

    if table_ref['m_join_cond_optim'] not in [0x0, 0x1]:
        print(f"note right of Table_ref_{str(table_ref.address)}")
        gdb.set_convenience_variable(g_gdb_conv,table_ref['m_join_cond_optim'].cast(table_ref['m_join_cond_optim'].dynamic_type))
        gdb.execute('call thd->gdb_str.set("", 0, system_charset_info)')
        gdb.execute('call $g_gdb_conv->print(thd, &(thd->gdb_str), QT_ORDINARY)')
        gdb_str = gdb.parse_and_eval('thd->gdb_str.c_ptr_safe()').string()
        formatted_sql = sqlparse.format(gdb_str, reindent=True, keyword_case='upper')
        print(f"m_join_cond_optim:   {formatted_sql}")
        print(f"end note")
    print()

    if table_ref['m_join_cond'] not in [0x0, 0x1]:
        print(f"note right of Table_ref_{str(table_ref.address)}")
        gdb.set_convenience_variable(g_gdb_conv,table_ref['m_join_cond'].cast(table_ref['m_join_cond'].dynamic_type))
        gdb.execute('call thd->gdb_str.set("", 0, system_charset_info)')
        gdb.execute('call $g_gdb_conv->print(thd, &(thd->gdb_str), QT_ORDINARY)')
        gdb_str = gdb.parse_and_eval('thd->gdb_str.c_ptr_safe()').string()
        formatted_sql = sqlparse.format(gdb_str, reindent=True, keyword_case='upper')
        print(f"m_join_cond:   {formatted_sql}")
        print(f"end note")
    print()


# 打印 mem_root_deque__Table_ref
# @deque mem_root_deque的指针或者对象
def display_mem_root_deque__Table_ref(deque):
    if deque.type.code == gdb.TYPE_CODE_PTR:
        deque = deque.dereference()
    print(f"map mem_root_deque__Table_ref_{deque.address} {{")
    for i in mem_root_deque_to_list(deque):
        print(f"    {i}=> {i.dynamic_type}")
    print(f"}}")

# List<Natural_join_column> *join_columns; // 连接列列表

def display_list__natural_join_column__list(list):
    if list.type.code == gdb.TYPE_CODE_PTR:
        list = list.dereference()
    print(f"map natural_join_column__list_{list.address} {{")
    for i in List_to_list(list):
        print(f"    {i.address} => natural_join_column *")
    print(f"}}")

def display_g_natural_join_column_list(natural_join_column):
    if natural_join_column.type.code == gdb.TYPE_CODE_PTR:
        natural_join_column = natural_join_column.dereference()
    print(f"map natural_join_column_{natural_join_column.address} {{")
    print(f"    view_field => {natural_join_column['view_field']}")
    print(f"    table_field => {natural_join_column['table_field']}")
    print(f"    table_ref => {natural_join_column['table_ref']}")
    print(f"    is_common => {natural_join_column['is_common']}")
    print(f"}}")

def display_Item_field(item):
    if item.type.code == gdb.TYPE_CODE_PTR:
        item = item.dereference()
    print(f"map Item_field_{item.address} {{")
    print(f"    table_ref => {item['table_ref']}")
    print(f"    field.field_name => {item['field']['field_name'].string()}")
    print(f"    field.table_name => {item['field']['table_name'].dereference().string()}")
    # print(f"    field.orig_db_name => {item['field']['orig_db_name'].string()}")
    print(f"    item_equal => {item['item_equal']}")
    print(f"    item_equal_all_join_nests => {item['item_equal_all_join_nests']}")
    print(f"    field_index => {item['field_index']}")
    print(f"}}")

def display_join(join):
    if join.type.code == gdb.TYPE_CODE_PTR:
        join = join.dereference()
    print(f"map JOIN_{join.address} {{")
    print(f"    query_block => {join['query_block']}")
    print(f"    thd => {join[thd]}")
    print(f"    grouped => {join[grouped]}")
    print(f"    const_table_map => {join[const_table_map]}")
    print(f"    found_const_table_map => {join[found_const_table_map]}")
    print(f"    fields => {join[fields]}")
    print(f"    tmp_table_param => {join[tmp_table_param]}")
    print(f"    lock => {join[lock]}")
    print(f"    implicit_grouping => {join[implicit_grouping]}")
    print(f"    select_distinct => {join[select_distinct]}")
    print(f"    keyuse_array => {join[keyuse_array]}")
    print(f"    order => {join[order]}")
    print(f"    group_list => {join[group_list]}")
    print(f"    m_windows => {join[m_windows]}")
    print(f"    where_cond => {join[where_cond]}")
    print(f"    having_cond => {join[having_cond]}")
    print(f"    having_for_explain => {join[having_for_explain]}")
    print(f"    tables_list => {join[tables_list]}")
    print(f"    current_ref_item_slice => {join[current_ref_item_slice]}")
    print(f"    with_json_agg => {join[with_json_agg]}")
    print(f"    rollup_state => {join[rollup_state]}")
    print(f"    explain_flags => {join[explain_flags]}")
    print(f"    send_group_parts => {join[send_group_parts]}")
    print(f"    thd => {join[thd]}")
    print(f"}}")

def display_QEP_shared(share):
    if share.type.code == gdb.TYPE_CODE_PTR:
        share = share.dereference()
    print(f"map QEP_shared_{share.address} {{")
    print(f"    m_join => {share[m_join]}")
    print(f"    m_idx => {share[m_idx]}")
    print(f"    m_table => {share[m_table]}")
    print(f"    m_position => {share[m_position]}")
    print(f"    m_sj_mat_exec => {share[m_sj_mat_exec]}")
    print(f"    m_first_sj_inner => {share[m_first_sj_inner]}")
    print(f"    m_last_sj_inner => {share[m_last_sj_inner]}")
    print(f"    m_first_inner => {share[m_first_inner]}")
    print(f"    m_last_inner => {share[m_last_inner]}")
    print(f"    m_first_upper => {share[m_first_upper]}")
    print(f"    m_ref => {share[m_ref]}")
    print(f"    m_index => {share[m_index]}")
    print(f"    m_condition => {share[m_condition]}")
    print(f"    m_condition_is_pushed_to_sort => {share[m_condition_is_pushed_to_sort]}")
    print(f"    m_records => {share[m_records]}")
    print(f"    m_range_scan => {share[m_range_scan]}")
    print(f"    prefix_tables_map => {share[prefix_tables_map]}")
    print(f"    added_tables_map => {share[added_tables_map]}")
    print(f"    m_ft_func => {share[m_ft_func]}")
    print(f"    m_skip_records_in_range => {share[m_skip_records_in_range]}")
    print(f"}}")

def display_JOIN_TAB(JOIN_TAB):
    if JOIN_TAB.type.code == gdb.TYPE_CODE_PTR:
        JOIN_TAB = JOIN_TAB.dereference()
    print(f"map JOIN_TAB_{JOIN_TAB.address} {{")
    print(f"    table_ref => {JOIN_TAB[table_ref]}")
    print(f"    m_keyuse => {JOIN_TAB[m_keyuse]}")
    print(f"    m_join_cond_ref => {JOIN_TAB[m_join_cond_ref]}")
    print(f"    cond_equal => {JOIN_TAB[cond_equal]}")
    print(f"    worst_seeks => {JOIN_TAB[worst_seeks]}")
    print(f"    const_keys => {JOIN_TAB[const_keys]}")
    print(f"    checked_keys => {JOIN_TAB[checked_keys]}")
    print(f"    skip_scan_keys => {JOIN_TAB[skip_scan_keys]}")
    print(f"    needed_reg => {JOIN_TAB[needed_reg]}")
    print(f"    quick_order_tested => {JOIN_TAB[quick_order_tested]}")
    print(f"    found_records => {JOIN_TAB[found_records]}")
    print(f"    read_time => {JOIN_TAB[read_time]}")
    print(f"    dependent => {JOIN_TAB[dependent]}")
    print(f"    key_dependent => {JOIN_TAB[key_dependent]}")
    print(f"    used_fieldlength => {JOIN_TAB[used_fieldlength]}")
    print(f"    use_quick => {JOIN_TAB[use_quick]}")
    print(f"    m_use_join_cache => {JOIN_TAB[m_use_join_cache]}")
    print(f"    emb_sj_nest => {JOIN_TAB[emb_sj_nest]}")
    print(f"    embedding_map => {JOIN_TAB[embedding_map]}")
    print(f"    join_cache_flags => {JOIN_TAB[join_cache_flags]}")
    print(f"    reversed_access => {JOIN_TAB[reversed_access]}")
    print(f"}}")

def display_QEP_TABB(QEP_TAB):
    if QEP_TAB.type.code == gdb.TYPE_CODE_PTR:
        QEP_TAB = QEP_TAB.dereference()
    print(f"map QEP_TAB_{QEP_TAB.address} {{")
    print(f"    table_ref => {QEP_TAB[table_ref]}")
    print(f"    flush_weedout_table => {QEP_TAB[flush_weedout_table]}")
    print(f"    check_weed_out_table => {QEP_TAB[check_weed_out_table]}")
    print(f"    firstmatch_return => {QEP_TAB[firstmatch_return]}")
    print(f"    loosescan_key_len => {QEP_TAB[loosescan_key_len]}")
    print(f"    rematerialize => {QEP_TAB[rematerialize]}")
    print(f"    materialize_table => {QEP_TAB[materialize_table]}")
    print(f"    using_dynamic_range => {QEP_TAB[using_dynamic_range]}")
    print(f"    needs_duplicate_removal => {QEP_TAB[needs_duplicate_removal]}")
    print(f"    not_used_in_distinct => {QEP_TAB[not_used_in_distinct]}")
    print(f"    having => {QEP_TAB[having]}")
    print(f"    op_type => {QEP_TAB[op_type]}")
    print(f"    tmp_table_param => {QEP_TAB[tmp_table_param]}")
    print(f"    filesort => {QEP_TAB[filesort]}")
    print(f"    filesort_pushed_order => {QEP_TAB[filesort_pushed_order]}")
    print(f"    ref_item_slice => {QEP_TAB[ref_item_slice]}")
    print(f"    m_condition_optim => {QEP_TAB[m_condition_optim]}")
    print(f"    m_keyread_optim => {QEP_TAB[m_keyread_optim]}")
    print(f"    m_reversed_access => {QEP_TAB[m_reversed_access]}")
    print(f"    lateral_derived_tables_depend_on_me => {QEP_TAB[lateral_derived_tables_depend_on_me]}")
    print(f"    invalidators => {QEP_TAB[invalidators]}")
    print(f"}}")

def print_class():
    print("class Query_term { \n"
            "    # Query_term_set_op *m_parent \n"
            "    # Query_result *m_setop_query_result \n"
            "    # bool m_owning_operand \n"
            "    # Table_ref *m_result_table \n"
            "    # mem_root_deque<Item*> *m_fields \n"
            "    - uint m_curr_id \n"
            "} \n"
            "note right of Query_term::m_fields \n"
            "    字段列表 \n"
            "end note \n"
            )

    print("class Query_term_set_op { \n"
            "    - Query_block *m_block \n"
            "    + mem_root_deque<Query_term*> m_children \n"
            "    + int64_t m_last_distinct \n"
            "    + int64_t m_first_distinct \n"
            "    + bool m_is_materialized \n"
            "} \n"
            "note right of Query_term_set_op::m_block \n"
            "    所属的 Query_block\n"
            "end note \n"
            )

    print("class Query_block { \n"
            "    + SQL_I_List<Table_ref> m_table_list \n"
            "    + Table_ref *leaf_tables \n"
            "    + Item *select_limit \n"
            "    + Item *offset_limit \n"
            "} \n"
            "note right of Query_block::m_table_list \n"
            "    Query_block 中所有的 Table_ref\n"
            "end note \n"
            "note right of Query_block::leaf_tables \n"
            "    Query_block 结果逻辑优化后的所有 Table_ref，通过 next_leaf 遍历\n"
            "end note \n"
            "note right of Query_block::select_limit \n"
            "    SQL 中的 limit 值\n"
            "end note \n"
            "note right of Query_block::offset_limit \n"
            "    SQL 中的 offset 值\n"
            "end note \n"
            )

    print("class Query_term_except { \n"
            "} \n"
            )

    print("class Query_term_intersect { \n"
            "} \n"
            )

    print("class Query_term_unary { \n"
            "} \n"
            )

    print("class Query_term_union { \n"
            "} \n"
            )



    print("class Table_ref { \n"
            "    + const char *db \n"
            "    + const char *table_name \n"
            "    + const char *alias \n"
            "    + List<String> *partition_names \n"
            "    + List<Index_hint> *index_hints \n"
            "    + LEX *view                                 \n"                            
            "    + Query_expression *derived  \n"
            "    + ST_SCHEMA_TABLE *schema_table  \n"
            "    + enum_view_algorithm effective_algorithm  \n"
            "    + Field_translator *field_translation  \n"
            "    + Table_ref *natural_join  \n"  
            "    + Item *m_join_cond            \n"
            "    + m_is_sj_or_aj_nest            \n"
            "    + table_map sj_inner_tables            \n"
            "    + Lbool is_natural_join            \n"
            "    + List<String> *join_using_fields            \n"
            "    + List<Natural_join_column> *join_columns            \n"
            "    + bool is_join_columns_complete            \n"
            "    + bool outer_join            \n"
            "    + bool join_order_swapped            \n"
            "    + bool straight            \n"
            "    + table_map join_cond_dep_tables            \n"
            "    + NESTED_JOIN *nested_join \n"
            "    + Table_ref *embedding            \n"
            "    + mem_root_deque<Table_ref*> *join_list            \n"
            "    + Item *m_join_cond_optim            \n"
            "    + COND_EQUAL *cond_equal            \n"

            "} \n"
            "note right of Table_ref \n"
            "  Table reference in the FROM clause.                                        \n"
            "                                                                             \n"
            "  These table references can be of several types that correspond to          \n"
            "  different SQL elements. Below we list all types of TABLE_LISTs with        \n"
            "  the necessary conditions to determine when a Table_ref instance            \n"
            "  belongs to a certain type.                                                 \n"
            "                                                                             \n"
            "  1) table (Table_ref::view == NULL)                                         \n"
            "     - base table                                                            \n"
            "       (Table_ref::derived == NULL)                                          \n"
            "     - subquery - Table_ref::table is a temp table                           \n"
            "       (Table_ref::derived != NULL)                                          \n"
            "     - information schema table                                              \n"
            "       (Table_ref::schema_table != NULL)                                     \n"
            "       NOTICE: for schema tables Table_ref::field_translation may be != NULL \n"
            "  2) view (Table_ref::view != NULL)                                          \n"
            "     - merge    (Table_ref::effective_algorithm == VIEW_ALGORITHM_MERGE)     \n"
            "           also (Table_ref::field_translation != NULL)                       \n"
            "     - temptable(Table_ref::effective_algorithm == VIEW_ALGORITHM_TEMPTABLE) \n"
            "           also (Table_ref::field_translation == NULL)                       \n"
            "  3) nested table reference (Table_ref::nested_join != NULL)                 \n"
            "     - table sequence - e.g. (t1, t2, t3)                                    \n"
            "       TODO: how to distinguish from a JOIN?                                 \n"
            "     - general JOIN                                                          \n"
            "       TODO: how to distinguish from a table sequence?                       \n"
            "     - NATURAL JOIN                                                          \n"
            "       (Table_ref::natural_join != NULL)                                     \n"
            "       - JOIN ... USING                                                      \n"
            "         (Table_ref::join_using_fields != NULL)                              \n"
            "     - semi-join                                                             \n"
            "       ;                                                                     \n"
            "end note                                                                     \n"

            "note right of Table_ref::m_join_cond \n"
            "    连接条件\n"
            "end note                                                                     \n"

            "note right of Table_ref::m_is_sj_or_aj_nest \n"
            "     是否是 SJ 或 AJ\n"
            "end note                                                                     \n"

            "note right of Table_ref::sj_inner_tables \n"
            "    SJ 的内表\n"
            "end note                                                                     \n"

            "note right of Table_ref::natural_join \n"
            "    NATURE JOIN 的 Table_ref \n"
            "end note                                                                     \n"

            "note right of Table_ref::is_natural_join \n"
            "    是否是 NATURE JOIN\n"
            "end note                                                                     \n"

            "note right of Table_ref::join_using_fields \n"
            "    JOIN XXX USING 的字段列表名  \n"
            "end note                                                                     \n"

            "note right of Table_ref::join_columns \n"
            "    JOIN 的谓词的字段列表\n"
            "end note                                                                     \n"

            "note right of Table_ref::is_join_columns_complete \n"
            "    ... \n"
            "end note                                                                     \n"

            "note right of Table_ref::outer_join \n"
            "    是否是 OUTER JOIN \n"
            "end note                                                                     \n"

            "note right of Table_ref::join_order_swapped \n"
            "    JOIN ORDER 是否 SWAPPED\n"
            "end note                                                                     \n"

            "note right of Table_ref::straight \n"
            "    ... \n"
            "end note                                                                     \n"

            "note right of Table_ref::join_cond_dep_tables \n"
            "     连接条件依赖的表 \n"
            "end note                                                                     \n"

            "note right of Table_ref::nested_join \n"
            "     ... \n"
            "end note                                                                     \n"

            "note right of Table_ref::embedding \n"
            "    ... \n"
            "end note                                                                     \n"

            "note right of Table_ref::join_list \n"
            "    ... \n"
            "end note                                                                     \n"

            "note right of Table_ref::m_join_cond_optim \n"
            "    优化后的连接条件 \n"
            "end note                                                                     \n"

            "note right of Table_ref::cond_equal \n"
            "    ... \n"
            "end note                                                                     \n"
    )

    print("Query_block -up-|> Query_term")
    print("Query_term_set_op -up-|> Query_term")
    print("Query_term_unary -up-|> Query_term_set_op")
    print("Query_term_union -up-|> Query_term_set_op")
    print("Query_term_except -up-|> Query_term_set_op")
    print("Query_term_intersect -up-|> Query_term_set_op")

class GDB_expr(gdb.Command):
    def __init__(self):
        super(GDB_expr, self).__init__("mysql expr", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        del g_query_expression_list[:]
        del g_query_block_list[:]
        del g_query_term_list[:]
        del g_table_ref_list[:]
        del g_mem_root_deque__Table_ref__list[:]
        del g_natural_join_column_list[:]
        del g_list__natural_join_column__list[:]
        del g_Item_field_list[:]
        del g_line[:]
        del g_error[:]

        expr = gdb.parse_and_eval(arg)
        self.traverse_expressions(expr)

        print("@startuml")
        for i in g_query_expression_list:
            display_Query_expression(i)

        for i in g_query_block_list:
            display_Query_block(i)
        
        for i in g_query_term_list:
            display_Query_term(i)

        for i in g_table_ref_list:
            display_Table_ref(i)

        for i in g_mem_root_deque__Table_ref__list:
            display_mem_root_deque__Table_ref(i)

        for i in g_list__natural_join_column__list:
            display_list__natural_join_column__list(i)

        for i in g_natural_join_column_list:
            display_g_natural_join_column_list(i)

        for i in g_Item_field_list:
            display_Item_field(i)

        for i in g_line:
            print(str(i))

        #print_class()
        
        print("@enduml")

        
    # 探索 Query_block
    # @expr query_block 的指针
    # note 只有不在 g_query_block_list 中的 @block 才会进入这个函数
    def traverse_blocks(self, block):
        g_query_block_list.append(block)

        if (block.dereference()['master'] != 0x0):
            g_line.append(f"Query_block_{str(block)} -up-> Query_expression_{block.dereference()['master']} : master")
            if (block.dereference()['master'] not in g_query_expression_list):                
                self.traverse_expressions(block.dereference()['master'])

        if (block.dereference()['slave'] != 0x0):
            g_line.append(f"Query_block_{str(block)} -down-> Query_expression_{block.dereference()['slave']} : slave")
            if (block.dereference()['slave'] not in g_query_expression_list):
                self.traverse_expressions(block.dereference()['slave'])

        if (block.dereference()['next'] != 0x0):
            g_line.append(f"Query_block_{str(block)} --> Query_block_{block.dereference()['next']} : next")
            if (block.dereference()['next'] not in g_query_block_list):
                self.traverse_blocks(block.dereference()['next'])

        if (block.dereference()['link_prev'] != 0x0 and block.dereference()['link_prev'].dereference() != 0x0):
            g_line.append(f"Query_block_{str(block)} --> Query_block_{block.dereference()['link_prev'].dereference()} : link_prev.dereference")
            if (block.dereference()['link_prev'].dereference() not in g_query_block_list):                
                self.traverse_blocks(block.dereference()['link_prev'].dereference())

        if (block['m_table_list'].address != 0x0):
            g_line.append(f"Query_block_{str(block)} --> SQL_I_List__Table_ref_{block['m_table_list'].address} : m_table_list")
            m_table_list = SQL_I_List_to_list(block['m_table_list'], 'next_local')
            for i in m_table_list:
                g_line.append(f"SQL_I_List__Table_ref_{block['m_table_list'].address} --> Table_ref_{i} : {i}")
                if i not in g_table_ref_list:
                    g_table_ref_list.append(i)
                    if (i['next_local'] != 0x0):
                        g_line.append(f"Table_ref_{i}::next_local --> Table_ref_{i['next_local']}")
                    if (i['next_leaf'] != 0x0):
                        g_line.append(f"Table_ref_{i}::next_leaf --> Table_ref_{i['next_leaf']}")
                    if (i['join_list'] != 0x0):
                        g_line.append(f"Table_ref_{i}::join_list --> mem_root_deque__Table_ref_{i['join_list']}")
                        if i['join_list'] not in g_mem_root_deque__Table_ref__list:
                            g_mem_root_deque__Table_ref__list.append(i['join_list'])
                            for j in mem_root_deque_to_list(i['join_list']):
                                g_line.append(f"mem_root_deque__Table_ref_{i['join_list']} --> Table_ref_{j} : {j}")
                    if (i['join_columns'] != 0x0):
                        if i['join_columns'] not in g_list__natural_join_column__list:
                            g_line.append(f"Table_ref_{i}::join_columns --> natural_join_column__list_{i['join_columns']}")
                            g_list__natural_join_column__list.append(i['join_columns'])
                            for j in List_to_list(i['join_columns']):
                                if j not in g_natural_join_column_list:
                                    g_natural_join_column_list.append(j.address)
                                    g_line.append(f"natural_join_column__list_{i['join_columns']} --> natural_join_column_{j.address}")
                                    if j.address not in g_Item_field_list:
                                        g_Item_field_list.append(j['table_field'])
                                        g_line.append(f"natural_join_column_{j.address}::table_field --> Item_field_{j['table_field']}")


        if (block['leaf_tables'] != 0x0):
            leaf_tables = table_ref_to_list(block['leaf_tables'], 'next_leaf')
            for i in leaf_tables:
                if i not in g_table_ref_list:
                    g_table_ref_list.append(i.dereference())

        if (block['m_table_nest'].address != 0x0):            
            m_table_nest = mem_root_deque_to_list(block['m_table_nest'])
            for i in m_table_nest:
                if i not in g_table_ref_list:
                    g_table_ref_list.append(i.dereference())

    # 探索 Query_expression
    # @expr query_expression 的指针
    # note 只有不在 g_query_expression_list 中的 @expr 才会进入这个函数
    def traverse_expressions(self, expr):
        g_query_expression_list.append(expr)

        if (expr.dereference()['master'] != 0x0):            
            g_line.append(f"Query_expression_{str(expr)} --> Query_block_{expr.dereference()['master']} : master")
            if (expr.dereference()['master'] not in g_query_block_list):
                self.traverse_blocks(expr.dereference()['master'])

        if (expr.dereference()['slave'] != 0x0):
            g_line.append(f"Query_expression_{str(expr)} --> Query_block_{expr.dereference()['slave']} : slave")
            if (expr.dereference()['slave'] not in g_query_block_list):
                self.traverse_blocks(expr.dereference()['slave'])

        if (expr.dereference()['next'] != 0x0):
            g_line.append(f"Query_expression_{str(expr)} --> Query_expression_{expr.dereference()['next']} : next")
            if (expr.dereference()['next'] not in g_query_expression_list):                
                self.traverse_expressions(expr.dereference()['next'])

        if (expr.dereference()['prev'] != 0x0):
            if (expr.dereference()['prev'].dereference() not in g_query_expression_list):
                g_line.append(f"Query_expression_{str(expr)} --> Query_expression_{expr.dereference()['prev']} : prev.dereference")
                self.traverse_expressions(expr.dereference()['prev'].dereference())
        
        if (expr.dereference()['m_query_term'] != 0x0):
            m_query_term_dynamic_type = expr.dereference()['m_query_term'].dynamic_type
            if str(m_query_term_dynamic_type) in ['Query_block *']:
                g_line.append(f"Query_expression_{str(expr)} --> Query_block_{expr.dereference()['m_query_term']} : m_query_term")
                if expr.dereference()['m_query_term'] not in g_query_block_list:                    
                    self.traverse_blocks(expr.dereference()['m_query_term'].cast(m_query_term_dynamic_type))
            elif str(m_query_term_dynamic_type) in ['Query_term_except *','Query_term_intersect *','Query_term_unary *','Query_term_union *']:
                g_line.append(f"Query_expression_{str(expr)} --> Query_term_{expr.dereference()['m_query_term']} : m_query_term")
                if expr.dereference()['m_query_term'] not in g_query_term_list:                    
                    self.traverse_terms(expr.dereference()['m_query_term'].cast(m_query_term_dynamic_type))
    
    # 探索 Query_term
    # term 实时类型为 ['Query_term_except *','Query_term_intersect *','Query_term_unary *','Query_term_union *'] 其中一种时才会进入该函数
    # @term query_term 的指针
    # note 只有不在 g_query_term_list 中的 @term 才会进入这个函数
    def traverse_terms(self, term):
        g_query_term_list.append(term)

        if (term['m_block'].address != 0x0):
            g_line.append(f"Query_term_{str(term)} --> Query_block_{term['m_block']} : m_block")
            if term['m_block'] not in g_query_block_list:
                self.traverse_blocks(term['m_block'])
            
        if (term['m_children'].address != 0x0):
            g_line.append(f"Query_term_{str(term)} --> mem_root_deque__Query_term_{term.dereference()['m_children'].address} : m_children")
            m_children_list = mem_root_deque_to_list(term['m_children'])
            for i in m_children_list:
                dynamic_type = i.dynamic_type
                if str(dynamic_type) in ['Query_block *']:
                    g_line.append(f"mem_root_deque__Query_term_{term.dereference()['m_children'].address}::{str(i)} --> Query_block_{str(i)} : {str(i)}")
                    if i not in g_query_block_list:                        
                        self.traverse_blocks(i.cast(dynamic_type))
                elif str(dynamic_type) in ['Query_term_except *','Query_term_intersect *','Query_term_unary *','Query_term_union *']:
                    g_line.append(f"mem_root_deque__Query_term_{term.dereference()['m_children'].address}::{str(i)} --> Query_term_{str(i)} : {str(i)}")
                    if i not in g_query_term_list:
                        self.traverse_terms(i.cast(dynamic_type))

MysqlCommand()
GDB_expr()
