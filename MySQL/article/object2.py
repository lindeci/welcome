# -*- coding: utf-8 -*-

"""
整体流程: 
- 先遍历对象的指针，放在全局的LIST中，同时把连线放到 g_line 中，
- 然后先打印对象，再打印连线

注意: 每次调用 display_xxx(object) 之前，不做 object 的非法性判断，也不做 object 是否在 list 中做判断；
display_xxx(object) 的修饰函数 object_decorator 会对 object 的合法性做判断，如果是指针则转换成对象；
同时修饰函数 object_decorator 会对 object 是否在 list 中做判断，如果 object 在 list 中，则 pass
"""
import gdb
import sqlparse

BLOCK_ELEMENTS = 128

g_space = 3          # 缩进空间大小
g_bin_len = 16       # 打印二级制的长度
g_gdb_conv = 'g_gdb_conv'    # gdb 时设置的临时变量


g_list_Query_expression = [] # 全局 Query_expression 的 list，里面的元素是指针
g_list_Query_block = [] # 全局 Query_block 的 list，里面的元素是指针
g_list_Query_term = []  # 全局 _Query_term 的 list，里面的元素是指针, 只存放 ['Query_term_except','Query_term_intersect','Query_term_unary','Query_term_union'] 这4种类型
g_list_Table_ref = [] # 全局 Table_ref 的 list, 里面的元素是指针
g_list_Item_field = []
g_list_COND_EQUAL = []                  # 全局 COND_EQUAL 的 list，里面的元素是指针
g_list_Natural_join_column = [] #全局 Natural_join_column 的 list，里面的元素是指针
g_list_mem_root_deque__Table_ref = []  # 全局 mem_root_deque<Table_ref*> 的 list, 面的元素是指针
g_list_List__natural_join_colum = []  # 全局 List<Natural_join_column> 的 list，里面的元素是指针
g_list_List__Item_equal = []            # 全局 List<Item_equal> 的 list，里面的元素是指针
g_list_mem_root_deque__object = []  # 全局 mem_root_deque<xxx> 的 list, 里面的元素是指针
g_list_Item = []     # 全局 Item 的 list, 里面的元素是指针
g_list_SQL_I_List__object = []  # 全局 SQL_I_List<xxx> 的 list, 里面的元素是指针
g_list_JOIN = []  # 全局 JOIN 的 list, 里面的元素是指针

g_list_line = []                             # 遍历对象时，如果两个对象之间有连线，则把连线信息插入这个列表。里面的元素时字符串
g_list_object_string = []
g_list_note = []

# 修饰函数，如果参数是指针则转换为对象。如果对象的地址合法，则调用原函数，否则什么都不做
# @func 原始函数名
def object_decorator(func):
    def wrapper(list, object):
        if object.type.code == gdb.TYPE_CODE_PTR:
            if object not in [0x0, 0x1] and object not in list:
                list.append(object)
                return func(list, object.dereference())
        else:
            if object.address not in [0x0, 0x1] and object.address not in list:
                list.append(object.address)
                return func(list, object)
    return wrapper

# 添加连线
# @list 连线列表，比如 g_line_COND_EQUAL、g_line_List__Item_equal 等
# @line_prefix 连线字符串的前缀，包含最后一个 _ 符号
# @item 连线末尾的对象或者指针
def add_line(list, line_prefix, item, label):
    if item.type.code == gdb.TYPE_CODE_PTR:
        if item not in [0x0, 0x1]:
            list.append(line_prefix + str(item) + ' : ' + label)
    else:
        if item.address not in [0x0, 0x1]:
            list.append(line_prefix + '_' + item.address + ' : ' + label)

# 调用 object 的 print(const THD *, String *str, enum_query_type) 函数，返回 String
# object 有 print(const THD *, String *str, enum_query_type) 函数成员的对象
# @object 对象或者指针
def get_object_print_result(object):
    if object.type.code == gdb.TYPE_CODE_PTR:
        if object not in [0x0, 0x1]:
            gdb.set_convenience_variable(g_gdb_conv,object.cast(object.dynamic_type))
    else:
        if object.address not in [0x0, 0x1]:
            gdb.set_convenience_variable(g_gdb_conv,object.cast(object.dynamic_type).address)
    gdb.execute('call thd->gdb_str.set("", 0, system_charset_info)')
    gdb.execute('call $g_gdb_conv->print(thd, &(thd->gdb_str), QT_ORDINARY)')
    return gdb.parse_and_eval('thd->gdb_str.c_ptr_safe()').string()

# 把 object 添加到 list 中
# @list 比如 g_list_COND_EQUAL、g_list_List__Item_equal 等
# @object 指针或者对象
#ef add_object_to_list(list, object):
#   if object.type.code == gdb.TYPE_CODE_PTR:
#       if object not in list:
#           list.append(object)
#   else:
#       if object.address not in list:    
#           list.append(object.address)

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

# 探索 Query_expression
# @list 存储 Query_expression 指针的列表
# @object Query_expression的指针或者对象
@object_decorator
def traverse_Query_expression(list, object):
    if object['prev'] not in [0x0, 0x1]:
        prev__dereference = object['prev'].dereference()
    else:
        prev__dereference = 0x0        
    display = textwrap.dedent(f'''
                              map Query_expression_{object.address} #header:pink;back:lightblue{{
                                       master => <Query_block*> {object['master']}
                                       slave => <Query_block*> {object['slave']}
                                       next => <Query_expression*> {object['next']}
                                       prev.dereference => <Query_expression**> {prev__dereference}
                                       m_query_term => <Query_term*> {object['m_query_term']}
                                       select_limit_cnt => <ha_rows> {object['select_limit_cnt']}
                                       offset_limit_cnt => <ha_rows> {object['offset_limit_cnt']}
                                       prepared => <bool> {object['prepared']}
                                       optimized => <bool> {object['optimized']}
                                       executed => <bool> {object['executed']}
                              }}
                              ''')
    g_list_object_string.append(display)
    note = f'note right of Query_expression_{object.address}\n' + \
           f'{sqlparse.format(get_object_print_result(object), reindent=True, keyword_case="upper")}\n' + \
           'end note'
    g_list_note.append(note)
    
    traverse_Query_block(g_list_Query_block, object['master'])    
    add_line(g_list_line, f'Query_expression_{object.address}::master -up-> Query_block_', object['master'], 'master')
    
    traverse_Query_block(g_list_Query_block, object['slave'])
    add_line(g_list_line, f'Query_expression_{object.address}::slave -down-> Query_block_', object['slave'], 'slave')
    
    traverse_Query_expression(g_list_Query_expression, object['next'])
    add_line(g_list_line, f'Query_expression_{object.address}::next --> Query_expression_', object['next'], 'next')
    
    if prev__dereference != 0x0:
        traverse_Query_expression(g_list_Query_expression, object['prev'].dereference())        
        g_list_line.append(f'Query_expression_{object.address}::prev.dereference --> Query_expression_{prev__dereference} : prev.dereference')

    if str(object['m_query_term'].dynamic_type) in ['Query_term_except *','Query_term_intersect *','Query_term_unary *','Query_term_union *']:
        traverse_Query_term(g_list_Query_term, object['m_query_term'].cast(object['m_query_term'].dynamic_type))
        add_line(g_list_line, f'Query_expression_{object.address}::m_query_term --> Query_term_', object['m_query_term'], 'm_query_term')
    elif str(object['m_query_term'].dynamic_type) in ['Query_block *']:
        traverse_Query_block(g_list_Query_block, object['m_query_term'].cast(object['m_query_term'].dynamic_type))
        add_line(g_list_line, f'Query_expression_{object.address}::m_query_term --> Query_block_', object['m_query_term'], 'm_query_term')

# 探索 Query_block
# @list 存储 Query_block 指针的列表
# @object Query_block的指针或者对象
@object_decorator
def traverse_Query_block(list, object):
    if object['link_prev'] not in [0x0, 0x1]:
        link_prev__dereference = object['link_prev'].dereference()
    else:
        link_prev__dereference = 0x0
    if (object['select_limit'] != 0x0):
        select_limit__value = object['select_limit'].cast(object['select_limit'].dynamic_type).dereference()['value']
    else:
        select_limit__value = 0
    if (object['offset_limit'] != 0x0):
        offset_limit__value = object['offset_limit'].cast(object['offset_limit'].dynamic_type).dereference()['value']
    else:
        offset_limit__value = 0
    
    display = textwrap.dedent(f'''
                              map Query_block_{object.address} #header:pink;back:lightgreen{{
                                       master => <Query_expression*> {object['master']}
                                       slave => <Query_expression*> {object['slave']}
                                       next => <Query_block*> {object['next']}
                                       link_prev.dereference => <Query_block**> {link_prev__dereference}
                                       select_limit.value => <Item*> {object['select_limit']}
                                       offset_limit.value => <Item*> {object['offset_limit']}
                                       m_table_list.address => <SQL_I_List<Table_ref>> {object['m_table_list'].address}
                                       leaf_tables => <Table_ref*> {object['leaf_tables']}
                                       m_table_nest.address => <mem_root_deque<Table_ref*>> {object['m_table_nest'].address}
                                       sj_nests.address => <mem_root_deque<Table_ref*>> {object['sj_nests'].address}
                                       order_list.address => <SQL_I_List<ORDER>> {object['order_list'].address}
                                       select_list_tables => <table_map> {object['select_list_tables']}
                                       outer_join => <table_map> {object['outer_join']}
                                       join.address => <JOIN*> {object['join'].address}
                                       m_current_table_nest => <mem_root_deque<Table_ref*>*> {object['m_current_table_nest']}
                                       cond_value => <Item::cond_result> {object['cond_value']}
                                       having_value => <Item::cond_result> {object['having_value']}
                                       m_where_cond => <Item*> {object['m_where_cond']}
                                       m_having_cond => <Item*> {object['m_having_cond']}
                                       has_sj_nests => <bool> {object['has_sj_nests']}
                                       has_aj_nests => <bool> {object['has_aj_nests']}
                                       m_right_joins => <bool> {object['m_right_joins']}
                              }}
                              ''')
    g_list_object_string.append(display)
    note = f'note right of Query_block_{object.address}\n' + \
           f'{sqlparse.format(get_object_print_result(object), reindent=True, keyword_case="upper")}\n' + \
           'end note'
    g_list_note.append(note)
        
    traverse_Query_expression(g_list_Query_expression, object['master'])
    add_line(g_list_line, f'Query_block_{object.address}::master -up-> Query_expression_', object['master'], 'master')
    
    traverse_Query_block(g_list_Query_block, object['next'])
    add_line(g_list_line, f'Query_block_{object.address}::next --> Query_block_', object['next'], 'next')
    
    traverse_Query_expression(g_list_Query_expression, object['slave'])
    add_line(g_list_line, f'Query_block_{object.address}::slave -down-> Query_expression_', object['slave'], 'slave')
    
    if link_prev__dereference != 0x0:
        traverse_Query_block(g_list_Query_block, object['link_prev'].dereference())
        g_list_line.append(f'Query_block_{object.address}::link_prev.dereference -right-> Query_block_{link_prev__dereference} : link_prev.dereference')
    
    traverse_Table_ref(g_list_Table_ref, object['leaf_tables'])
    add_line(g_list_line, f'Query_block_{object.address}::leaf_tables --> Table_ref_', object['leaf_tables'], 'leaf_tables')
    
    traverse_Item(g_list_Item, object['m_where_cond'])
    add_line(g_list_line, f'Query_block_{object.address}::m_where_cond --> Item_', object['m_where_cond'], 'm_where_cond')
    
    traverse_Item(g_list_Item, object['m_having_cond'])
    add_line(g_list_line, f'Query_block_{object.address}::m_having_cond --> Item_', object['m_having_cond'], 'm_having_cond')
    
    traverse_SQL_I_List__object(g_list_SQL_I_List__object, object['m_table_list'])
    if object["m_table_list"].type.template_argument(0).code == gdb.TYPE_CODE_PTR:
        add_line(g_list_line, f'Query_block_{object.address}::m_table_list --> SQL_I_List__{object["m_table_list"].type.template_argument(0).target()}_', object['m_table_list'].address, 'm_table_list')
    else:
        add_line(g_list_line, f'Query_block_{object.address}::m_table_list --> SQL_I_List__{object["m_table_list"].type.template_argument(0)}_', object['m_table_list'].address, 'm_table_list')


# 探索 Query_term，包含子类 Query_term_except、Query_term_intersect、Query_term_unary、Query_term_union，不包含 Query_block
# @list 存储 Query_term 指针的列表
# @object Query_term的指针或者对象
@object_decorator
def traverse_Query_term(list, object):
    if str(object.dynamic_type) not in ['Query_term_except','Query_term_intersect','Query_term_unary','Query_term_union']:
        return
    display = textwrap.dedent(f'''
                              map Query_term_{object.address} #header:pink;back:lightyellow{{
                                       __dynamic_type => {object.dynamic_type}
                                       m_block => <Query_block*> {object['m_block']}
                                       m_children.address => <mem_root_deque<Query_term*>> {object['m_children'].address}
                                       m_last_distinct => <int64_t> {object['m_last_distinct']}
                                       m_first_distinct => <int64_t> {object['m_first_distinct']}
                                       m_is_materialized => <bool> {object['m_is_materialized']}
                              }}
                              ''')
    g_list_object_string.append(display)
    add_line(g_list_line, f'Query_term_{object.address}::m_block --> Query_block_', object['m_block'], 'm_block')
    add_line(g_list_line, f'Query_term_{object.address}::m_children.address --> mem_root_deque__Query_term_', object['m_children'].address, 'm_children')
    traverse_Query_block(g_list_Query_block, object['m_block'])
    traverse_mem_root_deque__object(g_list_mem_root_deque__object, object['m_children'])
    
@object_decorator
def traverse_mem_root_deque__object(list, object):
    if object.type.template_argument(0).code == gdb.TYPE_CODE_PTR:
        target = object.type.template_argument(0).target()
    else:
        target = object.type.template_argument(0)
    display = f'map mem_root_deque__{target}_{object.address} {{\n'    
    for i in mem_root_deque_to_list(object):
        address = 0x0
        if object.type.template_argument(0).code == gdb.TYPE_CODE_PTR:
            address = str(i)
        else:
            address = str(i.address)
        display += f'         {address} => {i.dynamic_type}\n'
        if str(i.dynamic_type.target()) == 'Query_block':
            g_list_line.append(f'mem_root_deque__{target}_{object.address} --> Query_block_{address} : {address}')
            traverse_Query_block(g_list_Query_block, i.cast(i.dynamic_type))
        elif str(i.dynamic_type.target()) in ['Query_term_except','Query_term_intersect','Query_term_unary','Query_term_union']:
            g_list_line.append(f'mem_root_deque__{target}_{object.address} --> Query_term_{address} : {address}')
            traverse_Query_term(g_list_Query_term, i.cast(i.dynamic_type))
    display += '}\n'
    g_list_object_string.append(display)
    
@object_decorator
def traverse_SQL_I_List__object(list, object):
    if object.type.template_argument(0).code == gdb.TYPE_CODE_PTR:
        target = object.type.template_argument(0).target()
    else:
        target = object.type.template_argument(0)
    display = f'map SQL_I_List__{target}_{object.address} {{\n'

    for i in SQL_I_List_to_list(object):
        address = str(i)
        display += f'         {address} => {i.dynamic_type}\n'
        if str(target) == 'Table_ref':
            traverse_Table_ref(g_list_Table_ref, i)
            g_list_line.append(f'SQL_I_List__{target}_{object.address}::{address} --> Table_ref_{address} : {address}')
    display += '}\n'
    g_list_object_string.append(display)

# 探索 Table_ref
# @list 存储 Table_ref 指针的列表
# @object Table_ref 的指针或者对象
@object_decorator
def traverse_Table_ref(list, object):
    if object['db'] != 0x0:
        db = object['db'].string()
    else:
        db = 0x0
    if object['table_name'] != 0x0:
        table_name = object['table_name'].string()
    else:
        table_name = 0x0
    if object['alias'] != 0x0:
        alias = object['alias'].string()      
    else:
        alias = 0x0
    display = textwrap.dedent(f'''
                              map Table_ref_{object.address} #header:pink;back:lightblue{{
                                       db => <const char*> {db}
                                       table_name => <const char*> {table_name}
                                       alias => <const char*> {alias}
                                       m_tableno => <uint> {object['m_tableno']}
                                       next_local => <Table_ref*> {object['next_local']}
                                       next_leaf => <Table_ref*> {object['next_leaf']}
                                       partition_names => <List<String>*> {object['partition_names']}
                                       index_hints => <List<Index_hint>*> {object['index_hints']}
                                       view => <LEX*> {object['view']}
                                       derived => <Query_expression*> {object['derived']}
                                       schema_table => <ST_SCHEMA_TABLE*> {object['schema_table']}
                                       effective_algorithm => <enum_view_algorithm> {object['effective_algorithm']}
                                       field_translation => <Field_translator*> {object['field_translation']}
                                       natural_join => <Table_ref*> {object['natural_join']}
                                       join_using_fields => <List<String>*> {object['join_using_fields']}
                                       m_join_cond => <Item*> {object['m_join_cond']}
                                       m_is_sj_or_aj_nest => <bool> {object['m_is_sj_or_aj_nest']}
                                       sj_inner_tables => <table_map> {object['sj_inner_tables']}
                                       is_natural_join => <bool> {object['is_natural_join']}
                                       join_using_fields => <List<String>*> {object['join_using_fields']}
                                       join_columns => <List<Natural_join_column>*> {object['join_columns']}
                                       is_join_columns_complete => <bool> {object['is_join_columns_complete']}
                                       join_order_swapped => <bool> {object['join_order_swapped']}
                                       straight => <bool> {object['straight']}
                                       join_cond_dep_tables => <table_map> {object['join_cond_dep_tables']}
                                       nested_join => <NESTED_JOIN*> {object['nested_join']}
                                       embedding => <Table_ref*> {object['embedding']}
                                       join_list => <mem_root_deque<Table_ref*>*> {object['join_list']}
                                       m_join_cond_optim => <Item*> {object['m_join_cond_optim']}
                                       cond_equal => <COND_EQUAL*> {object['cond_equal']}
                              }}
                              ''')
    g_list_object_string.append(display)
    note = f'note right of Table_ref_{object.address}\n' + \
           f'{sqlparse.format(get_object_print_result(object), reindent=True, keyword_case="upper")}\n' + \
           'end note'
    g_list_note.append(note)
    
    traverse_Item(g_list_Item, object['m_join_cond'])
    add_line(g_list_line, f'Table_ref_{object.address}::m_join_cond --> Item_', object['m_join_cond'], 'm_join_cond')
    
    traverse_Item(g_list_Item, object['m_join_cond_optim'])
    add_line(g_list_line, f'Table_ref_{object.address}::m_join_cond_optim --> Item_', object['m_join_cond_optim'], 'm_join_cond_optim')

    traverse_Table_ref(g_list_Table_ref, object['next_local'])
    add_line(g_list_line, f'Table_ref_{object.address}::next_local --> Table_ref_', object['next_local'], 'next_local')
    
    traverse_Table_ref(g_list_Table_ref, object['next_leaf'])
    add_line(g_list_line, f'Table_ref_{object.address}::next_leaf --> Table_ref_', object['next_leaf'], 'next_leaf')
    
# 探索 Item
# @list 存储 Item 指针的列表
# @object Item 的指针或者对象
@object_decorator
def traverse_Item(list, object):
    gdb_str = sqlparse.format(get_object_print_result(object), reindent=True, keyword_case="upper").replace("\n","\\\\n")
    display = textwrap.dedent(f'''
                              map Item_{object.address} #header:pink;back:orange{{
                                       __dynamic_type => {object.dynamic_type}
                                       __print => {get_object_print_result(object)}
                              }}
                              ''')
    g_list_object_string.append(display)
    
# 探索 JOIN
# @list 存储 JOIN 指针的列表
# @object JOIN 的指针或者对象
@object_decorator
def traverse_JOIN(list, object):
    if object['best_ref'] != 0X0:
        best_ref__dereference = object['best_ref'].dereference()
    else:
        best_ref__dereference = 0x0
    if object['map2table'] != 0X0:
        map2table__dereference = object['map2table'].dereference()
    else:
        map2table__dereference = 0x0
    display = textwrap.dedent(f'''
                              map JOIN_{object.address} #header:pink;back:lightblue{{
                                       query_block => <Query_block* const> {object['query_block']}
                                       thd => <THD* const> {object['thd']}
                                       join_tab => <JOIN_TAB*> {object['join_tab']}
                                       qep_tab => <QEP_TAB*> {object['qep_tab']}                                       
                                       sort_by_table => <TABLE*> {object['sort_by_table']}
                                       grouped => <bool> {object['grouped']}
                                       const_table_map => <table_map> {object['const_table_map']}
                                       found_const_table_map => <table_map> {object['found_const_table_map']}
                                       fields => <mem_root_deque<Item*>> {object['fields']}
                                       tmp_table_param => <Temp_table_param> {object['tmp_table_param'].address}
                                       lock => <MYSQL_LOCK*> {object['lock']}
                                       implicit_grouping => <bool> {object['implicit_grouping']}
                                       select_distinct => <bool> {object['select_distinct']}
                                       keyuse_array => <Key_use_array> {object['keyuse_array'].address}
                                       order => <ORDER_with_src> {object['order'].address}
                                       group_list => <ORDER_with_src> {object['group_list'].address}
                                       m_windows => <List<Window>> {object['m_windows'].address}
                                       where_cond => <Item*> {object['where_cond']}
                                       having_cond => <Item*> {object['having_cond']}
                                       having_for_explain => <Item*> {object['having_for_explain']}
                                       tables_list => <Table_ref*> {object['tables_list']}
                                       current_ref_item_slice => <uint> {object['current_ref_item_slice']}
                                       with_json_agg => <bool> {object['with_json_agg']}
                                       rollup_state => <JOIN::RollupState> {object['rollup_state']}
                                       explain_flags => <Explain_format_flags> {object['explain_flags'].address}
                                       send_group_parts => <uint> {object['send_group_parts']}
                                       cond_equal => <COND_EQUAL*> {object['cond_equal']}
                              }}
                              ''')
    g_list_object_string.append(display)
    
    traverse_Item(g_list_Item, object['where_cond'])
    add_line(g_list_line, f'JOIN_{object.address}::where_cond --> Item_', object['where_cond'], 'where_cond')
    
    traverse_Item(g_list_Item, object['having_cond'])
    add_line(g_list_line, f'JOIN_{object.address}::having_cond --> Item_', object['having_cond'], 'having_cond')

# 探索 QEP_shared
# @list 存储 QEP_shared 指针的列表
# @object QEP_shared 的指针或者对象
@object_decorator
def traverse_QEP_shared(list, object):
    display = textwrap.dedent(f'''
                              map JOIN_{object.address} #header:pink;back:lightblue{{
                                       query_block => <Query_block* const> {object['query_block']}
                                       thd => <THD* const> {object['thd']}
                                       join_tab => <JOIN_TAB*> {object['join_tab']}
                                       qep_tab => <QEP_TAB*> {object['qep_tab']}                                       
                                       sort_by_table => <TABLE*> {object['sort_by_table']}
                                       grouped => <bool> {object['grouped']}
                                       const_table_map => <table_map> {object['const_table_map']}
                                       found_const_table_map => <table_map> {object['found_const_table_map']}
                                       fields => <mem_root_deque<Item*>> {object['fields']}
                                       tmp_table_param => <Temp_table_param> {object['tmp_table_param'].address}
                                       lock => <MYSQL_LOCK*> {object['lock']}
                                       implicit_grouping => <bool> {object['implicit_grouping']}
                                       select_distinct => <bool> {object['select_distinct']}
                                       keyuse_array => <Key_use_array> {object['keyuse_array'].address}
                                       order => <ORDER_with_src> {object['order'].address}
                                       group_list => <ORDER_with_src> {object['group_list'].address}
                                       m_windows => <List<Window>> {object['m_windows'].address}
                                       where_cond => <Item*> {object['where_cond']}
                                       having_cond => <Item*> {object['having_cond']}
                                       having_for_explain => <Item*> {object['having_for_explain']}
                                       tables_list => <Table_ref*> {object['tables_list']}
                                       current_ref_item_slice => <uint> {object['current_ref_item_slice']}
                                       with_json_agg => <bool> {object['with_json_agg']}
                                       rollup_state => <JOIN::RollupState> {object['rollup_state']}
                                       explain_flags => <Explain_format_flags> {object['explain_flags'].address}
                                       send_group_parts => <uint> {object['send_group_parts']}
                                       cond_equal => <COND_EQUAL*> {object['cond_equal']}
                              }}
                              ''')
    g_list_object_string.append(display)
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
    print(f"    thd => {join['thd']}")
    print(f"    join_tab => {join['join_tab']}")
    print(f"    qep_tab => {join['qep_tab']}")
    if join['best_ref'] != 0X0:
        print(f"    best_ref.dereference => {join['best_ref'].dereference()}")
    else:
        print(f"    best_ref.dereference => {join['best_ref']}")
    if join['map2table'] != 0X0:
        print(f"    map2table.dereference => {join['map2table'].dereference()}")
    else:
        print(f"    map2table.dereference => {join['map2table']}")
    print(f"    sort_by_table => {join['sort_by_table']}")
    print(f"    grouped => {join['grouped']}")
    print(f"    const_table_map => {join['const_table_map']}")
    print(f"    found_const_table_map => {join['found_const_table_map']}")
    print(f"    fields => {join['fields']}")
    print(f"    tmp_table_param => {join['tmp_table_param'].address}")
    print(f"    lock => {join['lock']}")
    print(f"    implicit_grouping => {join['implicit_grouping']}")
    print(f"    select_distinct => {join['select_distinct']}")
    print(f"    keyuse_array => {join['keyuse_array'].address}")
    print(f"    order => {join['order'].address}")
    print(f"    group_list => {join['group_list'].address}")
    print(f"    m_windows => {join['m_windows'].address}")
    print(f"    where_cond => {join['where_cond']}")
    print(f"    having_cond => {join['having_cond']}")
    print(f"    having_for_explain => {join['having_for_explain']}")
    print(f"    tables_list => {join['tables_list']}")
    print(f"    current_ref_item_slice => {join['current_ref_item_slice']}")
    print(f"    with_json_agg => {join['with_json_agg']}")
    print(f"    rollup_state => {join['rollup_state']}")
    print(f"    explain_flags => {join['explain_flags'].address}")
    print(f"    send_group_parts => {join['send_group_parts']}")
    print(f"    cond_equal => {join['cond_equal']}")
    print(f"}}")

    if join['join_tab'] != 0X0:
        display_JOIN_TAB(join['join_tab'])

    if join['qep_tab'] != 0X0:
        display_QEP_TAB(join['qep_tab'])

    if join['where_cond'] not in [0x0, 0x1]:
        print(f"note right of JOIN_{join.address}")
        gdb.set_convenience_variable(g_gdb_conv,join['where_cond'].cast(join['where_cond'].dynamic_type))
        gdb.execute('call thd->gdb_str.set("", 0, system_charset_info)')
        gdb.execute('call $g_gdb_conv->print(thd, &(thd->gdb_str), QT_ORDINARY)')
        gdb_str = gdb.parse_and_eval('thd->gdb_str.c_ptr_safe()').string()
        formatted_sql = sqlparse.format(gdb_str, reindent=True, keyword_case='upper')
        print(f"where_cond:   {formatted_sql}")
        print(f"end note")

    if join['cond_equal'] != 0X0:
        display_COND_EQUAL(join['cond_equal'])

def display_QEP_shared(share):
    if share.type.code == gdb.TYPE_CODE_PTR:
        share = share.dereference()
    print(f"map QEP_shared_{share.address} {{")
    print(f"    m_join => {share['m_join']}")
    print(f"    m_idx => {share['m_idx']}")
    print(f"    m_table => {share['m_table']}")
    print(f"    m_position => {share['m_position']}")
    print(f"    m_sj_mat_exec => {share['m_sj_mat_exec']}")
    print(f"    m_first_sj_inner => {share['m_first_sj_inner']}")
    print(f"    m_last_sj_inner => {share['m_last_sj_inner']}")
    print(f"    m_first_inner => {share['m_first_inner']}")
    print(f"    m_last_inner => {share['m_last_inner']}")
    print(f"    m_first_upper => {share['m_first_upper']}")
    print(f"    m_ref => {share['m_ref']}")
    print(f"    m_index => {share['m_index']}")
    print(f"    m_condition => {share['m_condition']}")
    print(f"    m_condition_is_pushed_to_sort => {share['m_condition_is_pushed_to_sort']}")
    print(f"    m_records => {share['m_records']}")
    print(f"    m_range_scan => {share['m_range_scan']}")
    print(f"    prefix_tables_map => {share['prefix_tables_map']}")
    print(f"    added_tables_map => {share['added_tables_map']}")
    print(f"    m_ft_func => {share['m_ft_func']}")
    print(f"    m_skip_records_in_range => {share['m_skip_records_in_range']}")
    print(f"}}")
    

def display_JOIN_TAB(JOIN_TAB):
    if JOIN_TAB.type.code == gdb.TYPE_CODE_PTR:
        JOIN_TAB = JOIN_TAB.dereference()
    print(f"map JOIN_TAB_{JOIN_TAB.address} {{")
    print(f"    table_ref => {JOIN_TAB['table_ref']}")
    print(f"    m_keyuse => {JOIN_TAB['m_keyuse']}")
    print(f"    m_join_cond_ref => {JOIN_TAB['m_join_cond_ref']}")
    print(f"    cond_equal => {JOIN_TAB['cond_equal']}")
    print(f"    worst_seeks => {JOIN_TAB['worst_seeks']}")
    print(f"    const_keys => {JOIN_TAB['const_keys']}")
    print(f"    checked_keys => {JOIN_TAB['checked_keys']}")
    print(f"    skip_scan_keys => {JOIN_TAB['skip_scan_keys']}")
    print(f"    needed_reg => {JOIN_TAB['needed_reg']}")
    print(f"    quick_order_tested => {JOIN_TAB['quick_order_tested']}")
    print(f"    found_records => {JOIN_TAB['found_records']}")
    print(f"    read_time => {JOIN_TAB['read_time']}")
    print(f"    dependent => {JOIN_TAB['dependent']}")
    print(f"    key_dependent => {JOIN_TAB['key_dependent']}")
    print(f"    used_fieldlength => {JOIN_TAB['used_fieldlength']}")
    print(f"    use_quick => {JOIN_TAB['use_quick']}")
    print(f"    m_use_join_cache => {JOIN_TAB['m_use_join_cache']}")
    print(f"    emb_sj_nest => {JOIN_TAB['emb_sj_nest']}")
    print(f"    embedding_map => {JOIN_TAB['embedding_map']}")
    print(f"    join_cache_flags => {JOIN_TAB['join_cache_flags']}")
    print(f"    reversed_access => {JOIN_TAB['reversed_access']}")
    print(f"}}")

    #display_QEP_shared(JOIN_TAB)

def display_QEP_TAB(QEP_TAB):
    if QEP_TAB.type.code == gdb.TYPE_CODE_PTR:
        QEP_TAB = QEP_TAB.dereference()
    print(f"map QEP_TAB_{QEP_TAB.address} {{")
    print(f"    table_ref => {QEP_TAB['table_ref']}")
    print(f"    flush_weedout_table => {QEP_TAB['flush_weedout_table']}")
    print(f"    check_weed_out_table => {QEP_TAB['check_weed_out_table']}")
    print(f"    firstmatch_return => {QEP_TAB['firstmatch_return']}")
    print(f"    loosescan_key_len => {QEP_TAB['loosescan_key_len']}")
    print(f"    rematerialize => {QEP_TAB['rematerialize']}")
    print(f"    materialize_table => {QEP_TAB['materialize_table']}")
    print(f"    using_dynamic_range => {QEP_TAB['using_dynamic_range']}")
    print(f"    needs_duplicate_removal => {QEP_TAB['needs_duplicate_removal']}")
    print(f"    not_used_in_distinct => {QEP_TAB['not_used_in_distinct']}")
    print(f"    having => {QEP_TAB['having']}")
    print(f"    op_type => {QEP_TAB['op_type']}")
    print(f"    tmp_table_param => {QEP_TAB['tmp_table_param']}")
    print(f"    filesort => {QEP_TAB['filesort']}")
    print(f"    filesort_pushed_order => {QEP_TAB['filesort_pushed_order']}")
    print(f"    ref_item_slice => {QEP_TAB['ref_item_slice']}")
    print(f"    m_condition_optim => {QEP_TAB['m_condition_optim']}")
    print(f"    m_keyread_optim => {QEP_TAB['m_keyread_optim']}")
    print(f"    m_reversed_access => {QEP_TAB['m_reversed_access']}")
    print(f"    lateral_derived_tables_depend_on_me => {QEP_TAB['lateral_derived_tables_depend_on_me']}")
    print(f"    invalidators => {QEP_TAB['invalidators']}")
    print(f"}}")

    if QEP_TAB['m_condition_optim'] not in [0x0, 0x1]:
        print(f"note right of QEP_TAB_{QEP_TAB.address}")
        gdb.set_convenience_variable(g_gdb_conv,QEP_TAB['m_condition_optim'].cast(QEP_TAB['m_condition_optim'].dynamic_type))
        gdb.execute('call thd->gdb_str.set("", 0, system_charset_info)')
        gdb.execute('call $g_gdb_conv->print(thd, &(thd->gdb_str), QT_ORDINARY)')
        gdb_str = gdb.parse_and_eval('thd->gdb_str.c_ptr_safe()').string()
        formatted_sql = sqlparse.format(gdb_str, reindent=True, keyword_case='upper')
        print(f"m_condition_optim:   {formatted_sql}")
        print(f"end note")

    #display_QEP_shared(QEP_TAB)
import textwrap

@object_decorator
def display_COND_EQUAL(COND_EQUAL):
    add_object_to_list(g_list_display_COND_EQUA, COND_EQUAL)
    display = textwrap.dedent(f'''
        map COND_EQUAL_{COND_EQUAL.address} {{
            max_members => {COND_EQUAL['max_members']}
            upper_levels => {COND_EQUAL['upper_levels']}
            current_level => {COND_EQUAL['current_level'].address}
        }}
        ''')
    g_list_line_COND_EQUAL
    
    add_line(g_line_COND_EQUAL, f'COND_EQUAL_{COND_EQUAL.address}::current_level -->List__Item_equal_', COND_EQUAL)
    if COND_EQUAL['current_level'].address not in [0x0, 0x1]:
        current_level_list = List_to_list(COND_EQUAL['current_level'])
        for i in current_level_list:
            gdb.set_convenience_variable(g_gdb_conv, get_object(i).address)
            gdb.execute('call thd->gdb_str.set("", 0, system_charset_info)')
            gdb.execute('call $g_gdb_conv->print(thd, &(thd->gdb_str), QT_ORDINARY)')
            gdb_str = gdb.parse_and_eval('thd->gdb_str.c_ptr_safe()').string()
            #formatted_sql = sqlparse.format(gdb_str, reindent=True, keyword_case='upper')
            print(gdb_str)

@object_decorator
def display_List__Item_equal(list):
    display = f'map List__Item_equal_{list.address} {{\n'
    for i in List_to_list(list):
        display += f'    {i.address} => {get_object_print_result(i)}\n'
    display += f'}}'
    g_list_List__Item_equal
    
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
        del g_list_Query_expression[:]
        del g_list_Query_block[:]
        del g_list_Query_term[:]
        del g_list_Table_ref[:]
        del g_list_Item_field[:]
        del g_list_COND_EQUAL[:]
        del g_list_Natural_join_column[:]
        del g_list_mem_root_deque__Table_ref[:]
        del g_list_mem_root_deque__object[:]
        del g_list_List__natural_join_colum[:]
        del g_list_List__Item_equal[:]
        del g_list_Item[:]
        del g_list_SQL_I_List__object[:]
        del g_list_JOIN[:]
        del g_list_line[:]
        del g_list_object_string[:]
        del g_list_note[:]
        
        expr = gdb.parse_and_eval(arg)
        traverse_Query_expression(g_list_Query_expression, expr)

        print("@startuml")
        for i in g_list_object_string:
            print(i)

        for i in g_list_line:
            print(i)
        print()
        
        #for i in g_list_note:
        #    print(i)
        #    print()

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













import gdb

class MysqlCommand(gdb.Command):
    def __init__(self):
        super(MysqlCommand, self).__init__(
            "mysql", gdb.COMMAND_USER, prefix=True)

class GDB_expr(gdb.Command):
    def __init__(self):
        super(GDB_expr, self).__init__("mysql my_object", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):        
        class_type = gdb.lookup_type(arg)
        fields = class_type.fields()
        for field in fields:
            print(field.name, field.type)
        
MysqlCommand()
GDB_expr()
