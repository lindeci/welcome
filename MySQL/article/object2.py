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
g_list_Mem_root_array__object = []  # 全局 Mem_root_array<xxx> 的 list, 里面的元素是指针
g_list_Item = []     # 全局 Item 的 list, 里面的元素是指针
g_list_SQL_I_List__object = []  # 全局 SQL_I_List<xxx> 的 list, 里面的元素是指针
g_list_List__object = []  # 全局 List<xxx> 的 list, 里面的元素是指针
g_list_std_vector__object = []  # 全局 std::vector<xxx> 的 list, 里面的元素是指针
g_list_JOIN = []  # 全局 JOIN 的 list, 里面的元素是指针
g_list_JOIN_TAB = []
g_list_QEP_TAB = []
g_list_QEP_shared = []
g_list_AccessPath = []
g_list_JoinHypergraph = []
g_list_hypergraph_Hypergraph = []
g_list_hypergraph_Node = []
g_list_hypergraph_Hyperedge = []
g_list_Predicate = []
g_list_JoinPredicate = []
g_list_RelationalExpression = []
g_list_line = []                             # 遍历对象时，如果两个对象之间有连线，则把连线信息插入这个列表。里面的元素时字符串
g_list_object_string = []
g_list_note = []

# 修饰函数，如果参数是指针则转换为对象。如果对象的地址合法，则调用原函数，否则什么都不做
# @func 原始函数名
def object_decorator(func):
    def wrapper(list, object):
        if object.type.code == gdb.TYPE_CODE_PTR:
            if object not in [0x0, 0x1, 0x8f8f8f8f8f8f8f8f] and object not in list:
                list.append(object)
                return func(list, object.dereference())
        else:
            if object.address not in [0x0, 0x1, 0x8f8f8f8f8f8f8f8f] and object.address not in list:
                list.append(object.address)
                return func(list, object)
    return wrapper

# 添加连线
# @list 连线列表，比如 g_line_COND_EQUAL、g_line_List__Item_equal 等
# @line_prefix 连线字符串的前缀，包含最后一个 _ 符号
# @item 连线末尾的对象或者指针
def add_line(list, line_prefix, item, label):
    if item.type.code == gdb.TYPE_CODE_PTR:
        if item not in [0x0, 0x1, 0x8f8f8f8f8f8f8f8f]:
            list.append(line_prefix + str(item) + ' : ' + label)
    else:
        if item.address not in [0x0, 0x1, 0x8f8f8f8f8f8f8f8f]:
            list.append(line_prefix + '_' + item.address + ' : ' + label)

# 调用 object 的 print(const THD *, String *str, enum_query_type) 函数，返回 String
# object 有 print(const THD *, String *str, enum_query_type) 函数成员的对象
# @object 对象或者指针
def get_object_print_result(object):
    if object.type.code == gdb.TYPE_CODE_PTR:
        if object not in [0x0, 0x1, 0x8f8f8f8f8f8f8f8f]:
            gdb.set_convenience_variable(g_gdb_conv,object.cast(object.dynamic_type))
    else:
        if object.address not in [0x0, 0x1, 0x8f8f8f8f8f8f8f8f]:
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
# @deque mem_root_deque 的指针或者值
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
# @list SQL_I_List 的值或指针
# 返回 list
def SQL_I_List_to_list(list, next_key = 'next_local'):    
    if list.type.code == gdb.TYPE_CODE_PTR:
        list = list.dereference()
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
# @array Mem_root_array 的值或指针
# 返回 list
def Mem_root_array_to_list(array):
    if array.type.code == gdb.TYPE_CODE_PTR:
        array = array.dereference()
    out_list = []
    m_size = array['m_size']
    for i in range(m_size):
        if array['m_array'][i].type.code == gdb.TYPE_CODE_PTR:
            out_list.append(array['m_array'][i])
        else:
             out_list.append(array['m_array'][i].address)
    return out_list

# 把 MySQL 源码中的 std::vector 转换为 python 中的 list
# @vector std::vector 的值或指针
# 返回 list  里面存的是指针
def std_vector_to_list(vector):
    if vector.type.code == gdb.TYPE_CODE_PTR:
        vector = vector.dereference()
    out_list = []
    value_reference = vector['_M_impl']['_M_start']
    while value_reference != vector['_M_impl']['_M_finish']:
        out_list.append(value_reference)
        value_reference += 1
    return out_list

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
                                       join => <JOIN*> {object['join']}
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
    
    traverse_JOIN(g_list_JOIN, object['join'])
    add_line(g_list_line, f'Query_block_{object.address}::join --> JOIN_', object['join'], 'join')
    
    traverse_mem_root_deque__object(g_list_mem_root_deque__object, object['m_table_nest'])
    add_line(g_list_line, f'Query_block_{object.address}::m_table_nest.address --> mem_root_deque__Table_ref_', object['m_table_nest'].address, 'm_table_nest')
    
    traverse_mem_root_deque__object(g_list_mem_root_deque__object, object['sj_nests'])
    add_line(g_list_line, f'Query_block_{object.address}::sj_nests.address --> mem_root_deque__Table_ref_', object['sj_nests'].address, 'sj_nests')
    
    
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
   
    traverse_Query_block(g_list_Query_block, object['m_block'])
    add_line(g_list_line, f'Query_term_{object.address}::m_block --> Query_block_', object['m_block'], 'm_block')
    
    traverse_mem_root_deque__object(g_list_mem_root_deque__object, object['m_children'])
    add_line(g_list_line, f'Query_term_{object.address}::m_children.address --> mem_root_deque__Query_term_', object['m_children'].address, 'm_children')
    
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
        elif str(i.dynamic_type.target()) in ['Item_field']:
            g_list_line.append(f'mem_root_deque__{target}_{object.address} --> Item_{address} : {address}')
            traverse_Item(g_list_Item, i.cast(i.dynamic_type))
        elif str(i.dynamic_type.target()) in ['Table_ref']:
            g_list_line.append(f'mem_root_deque__{target}_{object.address} --> Table_ref_{address} : {address}')
            traverse_Item(g_list_Table_ref, i.cast(i.dynamic_type))
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
    
@object_decorator
def traverse_List__object(list, object):
    if object.type.template_argument(0).code == gdb.TYPE_CODE_PTR:
        target = object.type.template_argument(0).target()
    else:
        target = object.type.template_argument(0)
    display = f'map List__{target}_{object.address} {{\n'

    for i in List_to_list(object):
        address = str(i)
        display += f'         {address} => {i.dynamic_type}\n'
        if str(target) == 'Item_equal':
            traverse_Item(g_list_List__Item_equal, i)
            g_list_line.append(f'List__{target}_{object.address}::{address} --> Item_{address} : {address}')
    display += '}\n'
    g_list_object_string.append(display)


@object_decorator
def traverse_Mem_root_array__object(list, object):
    if object.type.template_argument(0).code == gdb.TYPE_CODE_PTR:
        target = object.type.template_argument(0).target()
    else:
        target = object.type.template_argument(0)
    if str(target) in ['Item', 'Item_eq_base']:
        display = f'map Mem_root_array_Item_{object.address} {{\n'
    else:
        display = f'map Mem_root_array_{str(target).replace("::","_")}_{object.address} {{\n'
    out_list = Mem_root_array_to_list(object)
    for i in range(len(out_list)):
        address = str(out_list[i])
        if str(target) == 'hypergraph::Hyperedge':
            display += f'         edges[{i}] => {address}<{out_list[i].dynamic_type}>    left={bin(out_list[i]["left"])[2:].zfill(16)}    right={bin(out_list[i]["right"])[2:].zfill(16)}\n'
        elif str(target) == 'hypergraph::Node':
            simple_edges = set()
            complex_edges = set()
            for j in std_vector_to_list(out_list[i]['simple_edges']):
                simple_edges.add(int(j.dereference()))
            for j in std_vector_to_list(out_list[i]['complex_edges']):
                complex_edges.add(int(j.dereference()))
            if not simple_edges:
                simple_edges = '{}'
            if not complex_edges:
                complex_edges = '{}'
            display += f'         nodes[{i}] => {address}<{out_list[i].dynamic_type}>    simple_neighborhood={bin(out_list[i]["simple_neighborhood"])[2:].zfill(16)}    simple_edges={simple_edges}    complex_edges={complex_edges}\n'
        elif str(target) == 'Predicate':
            display += f'         {address} => {out_list[i].dynamic_type}\n'
            traverse_Predicate(g_list_Predicate, out_list[i])
            g_list_line.append(f'Mem_root_array_{str(target).replace("::","_")}_{object.address}::{address} --> Predicate_{address} : {address}')
        elif str(target) == 'JoinPredicate':
            display += f'         {address} => {out_list[i].dynamic_type}\n'
            traverse_JoinPredicate(g_list_JoinPredicate, out_list[i])
            g_list_line.append(f'Mem_root_array_{str(target).replace("::","_")}_{object.address}::{address} --> JoinPredicate_{address} : {address}')
        elif str(target) in ['Item', 'Item_eq_base']:
            display += f'         {address} => {out_list[i].dynamic_type}\n'
            traverse_Item(g_list_Item, out_list[i])
            g_list_line.append(f'Mem_root_array_Item_{object.address}::{address} --> Item_{address} : {address}')
        else:
            display += f'         {address} => {out_list[i].dynamic_type}\n'
        #if str(target) == 'hypergraph::Hyperedge':
        #    traverse_hypergraph_Hyperedge(g_list_hypergraph_Hyperedge, out_list[i])
        #    g_list_line.append(f'Mem_root_array_{str(target).replace("::","_")}_{object.address}::{address} --> hypergraph_Hyperedge_{address} : {address}')
        #elif str(target) == 'hypergraph::Node':
        #    traverse_hypergraph_Node(g_list_hypergraph_Node, out_list[i])
        #    g_list_line.append(f'Mem_root_array_{str(target).replace("::","_")}_{object.address}::{address} --> hypergraph_Node_{address} : {address}')
    display += '}\n'
    g_list_object_string.append(display)
    
@object_decorator
def traverse_std_vector__object(list, object):
    if object.type.template_argument(0).code == gdb.TYPE_CODE_PTR:
        target = object.type.template_argument(0).target()
    else:
        target = object.type.template_argument(0)
    display = f'map std_vector_{str(target).replace("::","_").replace(" ","_")}_{object.address} {{\n'
    for i in std_vector_to_list(object):
        #address = str(i)
        display += f'         {bin(i.dereference())[2:].zfill(10)} => {i.dynamic_type}\n'
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
                                       ref_items => <Ref_item_array *> {object['ref_items']}
                                       m_root_access_path => <AccessPath *> {object['m_root_access_path']}
                                       m_root_access_path_no_in2exists => <AccessPath *> {object['m_root_access_path_no_in2exists']}
                              }}
                              ''')
    g_list_object_string.append(display)
    
    traverse_Item(g_list_Item, object['where_cond'])
    add_line(g_list_line, f'JOIN_{object.address}::where_cond --> Item_', object['where_cond'], 'where_cond')
    
    traverse_Item(g_list_Item, object['having_cond'])
    add_line(g_list_line, f'JOIN_{object.address}::having_cond --> Item_', object['having_cond'], 'having_cond')

    traverse_JOIN_TAB(g_list_JOIN_TAB, object['join_tab'])
    add_line(g_list_line, f'JOIN_{object.address}::join_tab --> JOIN_TAB_', object['join_tab'], 'join_tab')

    traverse_QEP_TAB(g_list_QEP_TAB, object['qep_tab'])
    add_line(g_list_line, f'JOIN_{object.address}::qep_tab --> QEP_TAB_', object['qep_tab'], 'qep_tab')

    traverse_COND_EQUAL(g_list_COND_EQUAL, object['cond_equal'])
    add_line(g_list_line, f'JOIN_{object.address}::cond_equal --> COND_EQUAL_', object['cond_equal'], 'cond_equal')
    
    traverse_Table_ref(g_list_Table_ref, object['tables_list'])
    add_line(g_list_line, f'JOIN_{object.address}::tables_list --> Table_ref_', object['tables_list'], 'tables_list')
        
    traverse_mem_root_deque__object(g_list_mem_root_deque__object, object['fields'])
    add_line(g_list_line, f'JOIN_{object.address}::fields --> mem_root_deque__Item_', object['fields'], 'fields')

    traverse_AccessPath(g_list_AccessPath, object['m_root_access_path'])
    add_line(g_list_line, f'JOIN_{object.address}::m_root_access_path --> AccessPath_', object['m_root_access_path'], 'm_root_access_path')

    traverse_AccessPath(g_list_AccessPath, object['m_root_access_path_no_in2exists'])
    add_line(g_list_line, f'JOIN_{object.address}::m_root_access_path_no_in2exists --> AccessPath_', object['m_root_access_path_no_in2exists'], 'm_root_access_path_no_in2exists')
    
# 探索 QEP_shared
# @list 存储 QEP_shared 指针的列表
# @object QEP_shared 的指针或者对象
@object_decorator
def traverse_QEP_shared(list, object):
    display = textwrap.dedent(f'''
                              map QEP_shared_{object.address} #header:pink;back:lightgreen{{
                                       m_join => <JOIN *> {object['m_join']}
                                       m_idx => <plan_idx> {object['m_idx']}
                                       m_table => <TABLE *> {object['m_table']}
                                       m_position => <POSITION *> {object['m_position']}
                                       m_sj_mat_exec => <Semijoin_mat_exec *> {object['m_sj_mat_exec']}
                                       m_first_sj_inner => <plan_idx> {object['m_first_sj_inner']}
                                       m_last_sj_inner => <plan_idx> {object['m_last_sj_inner']}
                                       m_first_inner => <plan_idx> {object['m_first_inner']}
                                       m_last_inner => <plan_idx> {object['m_last_inner']}
                                       m_first_upper => <plan_idx> {object['m_first_upper']}
                                       m_ref.address => <Index_lookup> {object['m_ref'].address}
                                       m_index => <uint> {object['m_index']}
                                       m_type => <join_type> {object['m_type']}
                                       m_condition => <Item *> {object['m_condition']}
                                       m_condition_is_pushed_to_sort => <bool> {object['m_condition_is_pushed_to_sort']}
                                       m_keys.address => <Key_map> {object['m_keys'].address}
                                       m_records => <ha_rows> {object['m_records']}
                                       m_range_scan => <AccessPath *> {object['m_range_scan']}
                                       prefix_tables_map => <table_map> {object['prefix_tables_map']}
                                       added_tables_map => <table_map> {object['added_tables_map']}
                                       m_ft_func => <Item_func_match *> {object['m_ft_func']}
                                       m_skip_records_in_range => <bool> {object['m_skip_records_in_range']}
                              }}
                              ''')
    g_list_object_string.append(display)
    
    traverse_Item(g_list_Item, object['m_condition'])
    add_line(g_list_line, f'QEP_shared_{object.address}::m_condition --> Item_', object['m_condition'], 'm_condition')
# List<Natural_join_column> *join_columns; // 连接列列表

# 探索 JOIN_TAB
# @list 存储 JOIN_TAB 指针的列表
# @object JOIN_TAB 的指针或者对象
@object_decorator
def traverse_JOIN_TAB(list, object):
    display = textwrap.dedent(f'''
                              map JOIN_TAB_{object.address} #header:pink;back:lightgreen{{
                                       m_qs => <QEP_shared *> {object['m_qs']}
                                       table_ref => <Table_ref *> {object['table_ref']}
                                       m_keyuse => <Key_use *> {object['m_keyuse']}
                                       m_join_cond_ref => <Item **> {object['m_join_cond_ref']}
                                       cond_equal => <COND_EQUAL *> {object['cond_equal']}
                                       worst_seeks => <double> {object['worst_seeks']}
                                       const_keys => <Key_map> {object['const_keys']}
                                       checked_keys => <Key_map> {object['checked_keys']}
                                       skip_scan_keys => <Key_map> {object['skip_scan_keys']}
                                       needed_reg => <Key_map> {object['needed_reg']}
                                       quick_order_tested => <Key_map> {object['quick_order_tested']}
                                       found_records => <ha_rows> {object['found_records']}
                                       read_time => <double> {object['read_time']}
                                       dependent => <table_map> {object['dependent']}
                                       key_dependent => <table_map> {object['key_dependent']}
                                       used_fieldlength => <uint> {object['used_fieldlength']}
                                       use_quick => <quick_type> {object['use_quick']}
                                       m_use_join_cache => <uint> {object['m_use_join_cache']}
                                       emb_sj_nest => <Table_ref *> {object['emb_sj_nest']}
                                       embedding_map => <nested_join_map> {object['embedding_map']}
                                       join_cache_flags => <uint> {object['join_cache_flags']}
                                       reversed_access => <bool> {object['reversed_access']}
                              }}
                              ''')
    g_list_object_string.append(display)

    traverse_QEP_shared(g_list_QEP_shared, object['m_qs'])
    add_line(g_list_line, f'JOIN_TAB_{object.address}::m_qs --> QEP_shared_', object['m_qs'], 'm_qs')

# 探索 QEP_TAB
# @list 存储 QEP_TAB 指针的列表
# @object QEP_TAB 的指针或者对象
@object_decorator
def traverse_QEP_TAB(list, object):
    display = textwrap.dedent(f'''
                              map QEP_TAB_{object.address} #header:pink;back:lightgreen{{
                                       m_qs => <QEP_shared *> {object['m_qs']}
                                       table_ref => <Table_ref *> {object['table_ref']}
                                       flush_weedout_table => <SJ_TMP_TABLE *> {object['flush_weedout_table']}
                                       check_weed_out_table => <SJ_TMP_TABLE *> {object['check_weed_out_table']}
                                       firstmatch_return => <plan_idx> {object['firstmatch_return']}
                                       loosescan_key_len => <uint> {object['loosescan_key_len']}
                                       match_tab => <plan_idx> {object['match_tab']}
                                       rematerialize => <bool> {object['rematerialize']}
                                       materialize_table => <QEP_TAB::Setup_func> {object['materialize_table']}
                                       using_dynamic_range => <bool> {object['using_dynamic_range']}
                                       needs_duplicate_removal => <bool> {object['needs_duplicate_removal']}
                                       not_used_in_distinct => <bool> {object['not_used_in_distinct']}
                                       having => <Item *> {object['having']}
                                       op_type => <QEP_TAB::enum_op_type> {object['op_type']}
                                       tmp_table_param => <Temp_table_param *> {object['tmp_table_param']}
                                       filesort => <Filesort *> {object['filesort']}
                                       filesort_pushed_order => <ORDER *> {object['filesort_pushed_order']}
                                       ref_item_slice => <uint> {object['ref_item_slice']}
                                       m_condition_optim => <Item *> {object['m_condition_optim']}
                                       m_keyread_optim => <bool> {object['m_keyread_optim']}
                                       m_reversed_access => <bool> {object['m_reversed_access']}
                                       lateral_derived_tables_depend_on_me => <qep_tab_map> {object['lateral_derived_tables_depend_on_me']}
                                       invalidators => <Mem_root_array<AccessPath const*> *> {object['invalidators']}
                              }}
                              ''')
    g_list_object_string.append(display)

    traverse_QEP_shared(g_list_QEP_shared, object['m_qs'])
    add_line(g_list_line, f'QEP_TAB_{object.address}::m_qs --> QEP_shared_', object['m_qs'], 'm_qs')
    
    traverse_Table_ref(g_list_Table_ref, object['table_ref'])
    add_line(g_list_line, f'QEP_TAB_{object.address}::table_ref --> Table_ref_', object['table_ref'], 'table_ref')

    traverse_Item(g_list_Item, object['m_condition_optim'])
    add_line(g_list_line, f'QEP_TAB_{object.address}::m_condition_optim --> Item_', object['m_condition_optim'], 'm_condition_optim')
    
# 探索 COND_EQUAL
# @list 存储 COND_EQUAL 指针的列表
# @object COND_EQUAL 的指针或者对象
@object_decorator
def traverse_COND_EQUAL(list, object):
    display = textwrap.dedent(f'''
                              map COND_EQUAL_{object.address} #header:pink;back:lightgreen{{
                                       max_members => <uint> {object['max_members']}
                                       upper_levels => <COND_EQUAL *> {object['upper_levels']}
                                       current_level.address => <List<Item_equal>> {object['current_level'].address}
                              }}
                              ''')
    g_list_object_string.append(display)

    traverse_List__object(g_list_List__object, object['current_level'])
    add_line(g_list_line, f'COND_EQUAL_{object.address}::current_level.address --> List__Item_equal_', object['current_level'].address, 'current_level')

# 探索 AccessPath
# @list 存储 AccessPath 指针的列表
# @object AccessPath 的指针或者对象
@object_decorator
def traverse_AccessPath(list, object):
    display = textwrap.dedent(f'''
                              map AccessPath_{object.address} #header:pink;back:lightgreen{{
                                       type => <AccessPath::Type> {object['type']}
                                       safe_for_rowid => <AccessPath::Safety> {object['safe_for_rowid']}
                                       count_examined_rows => <bool> {object['count_examined_rows']}
                                       has_group_skip_scan => <bool> {object['has_group_skip_scan']}
                                       forced_by_dbug => <bool> {object['forced_by_dbug']}
                                       ordering_state => <int> {object['ordering_state']}
                                       iterator => <RowIterator *> {object['iterator']}
                                       num_output_rows_before_filter => <double> {object['num_output_rows_before_filter']}
                                       filter_predicates.address => <OverflowBitset> {object['filter_predicates'].address}
                                       delayed_predicates.address => <OverflowBitset> {object['delayed_predicates'].address}
                                       parameter_tables => <hypergraph::NodeMap> {object['parameter_tables']}
                                       secondary_engine_data => <void *> {object['secondary_engine_data']}
                                       m_num_output_rows => <double> {object['m_num_output_rows']}
                                       m_cost => <double> {object['m_cost']}
                                       m_init_cost => <double> {object['m_init_cost']}
                                       m_init_once_cost => <double> {object['m_init_once_cost']}
                                       m_cost_before_filter => <double> {object['m_cost_before_filter']}
                                       u.address => <union {...}> {object['u'].address}
                              }}
                              ''')
    # immediate_update_delete_table => <int8_t> {object['immediate_update_delete_table']}
    g_list_object_string.append(display)

# 探索 JoinHypergraph
# @list 存储 JoinHypergraph 指针的列表
# @object JoinHypergraph 的指针或者对象
@object_decorator
def traverse_JoinHypergraph(list, object):
    display = textwrap.dedent(f'''
                              map JoinHypergraph_{object.address} #header:pink;back:lightgreen{{
                                       graph.address => <hypergraph::Hypergraph> {object['graph'].address}
                                       secondary_engine_costing_flags => <SecondaryEngineCostingFlags> {object['secondary_engine_costing_flags']}
                                       table_num_to_node_num.address => <std::array<int, 61>> {object['table_num_to_node_num'].address}
                                       nodes.address => <Mem_root_array<JoinHypergraph::Node>> {object['nodes'].address}
                                       edges.address => <Mem_root_array<JoinPredicate>> {object['edges'].address}
                                       predicates.address => <Mem_root_array<Predicate>> {object['predicates'].address}
                                       num_where_predicates => <unsigned int> {object['num_where_predicates']}
                                       materializable_predicates.address => <OverflowBitset> {object['materializable_predicates'].address}
                                       sargable_join_predicates.address => <mem_root_unordered_map<Item*, int, std::hash<Item*>, std::equal_to<Item*> >> {object['sargable_join_predicates'].address}
                                       has_reordered_left_joins => <bool> {object['has_reordered_left_joins']}
                                       tables_inner_to_outer_or_anti => <table_map> {object['tables_inner_to_outer_or_anti']}
                                       m_query_block => <const Query_block *> {object['m_query_block']}
                              }}
                              ''')
    g_list_object_string.append(display)

    traverse_Mem_root_array__object(g_list_Mem_root_array__object, object['nodes'])
    add_line(g_list_line, f'JoinHypergraph_{object.address}::nodes.address --> Mem_root_array_JoinHypergraph_Node_', object['nodes'].address, 'nodes.address')
    
    traverse_Mem_root_array__object(g_list_Mem_root_array__object, object['edges'])
    add_line(g_list_line, f'JoinHypergraph_{object.address}::edges.address --> Mem_root_array_JoinPredicate_', object['edges'].address, 'edges.address')
    
    traverse_Mem_root_array__object(g_list_Mem_root_array__object, object['predicates'])
    add_line(g_list_line, f'JoinHypergraph_{object.address}::predicates.address --> Mem_root_array_Predicate_', object['predicates'].address, 'predicates.address')

    traverse_hypergraph_Hypergraph(g_list_hypergraph_Hypergraph, object['graph'])
    add_line(g_list_line, f'JoinHypergraph_{object.address}::graph.address --> hypergraph_Hypergraph_', object['graph'].address, 'graph.address')

    #traverse_Query_block(g_list_Query_block, object['m_query_block'])
    #add_line(g_list_line, f'JoinHypergraph_{object.address}::m_query_block --> Query_block_', object['m_query_block'], 'm_query_block')
    
# 探索 hypergraph_Hypergraph
# @list 存储 hypergraph_Hypergraph 指针的列表
# @object hypergraph_Hypergraph 的指针或者对象
@object_decorator
def traverse_hypergraph_Hypergraph(list, object):
    display = textwrap.dedent(f'''
                              map hypergraph_Hypergraph_{object.address} #header:pink;back:lightgreen{{
                                       nodes.address => <Mem_root_array<hypergraph::Node>> {object['nodes'].address}
                                       edges.address => <Mem_root_array<hypergraph::Hyperedge>> {object['edges'].address}
                              }}
                              ''')
#    display = f'''map hypergraph_Hypergraph_{object.address} #header:pink;back:lightgreen{{ \n'''
#    edges_list = Mem_root_array_to_list(object['edges'])
#    nodes_list = Mem_root_array_to_list(object['nodes'])
#    display += f'''         edges.address => <Mem_root_array<hypergraph::Hyperedge>> {object['edges'].address} \\n'''
#    for i in range(len(edges_list)):
#        display += f'''edges[{i}] : <hypergraph::Hyperedge *> {edges_list[i]}     left={edges_list[i]["left"]}      right={edges_list[i]["right"]} \\n'''
#    print(display)
    g_list_object_string.append(display)

    traverse_Mem_root_array__object(g_list_Mem_root_array__object, object['nodes'])
    add_line(g_list_line, f'hypergraph_Hypergraph_{object.address}::nodes.address --> Mem_root_array_hypergraph_Node_', object['nodes'].address, 'nodes.address')
    
    traverse_Mem_root_array__object(g_list_Mem_root_array__object, object['edges'])
    add_line(g_list_line, f'hypergraph_Hypergraph_{object.address}::edges.address --> Mem_root_array_hypergraph_Hyperedge_', object['edges'].address, 'edges.address')



# 探索 Predicate
# @list 存储 Predicate 指针的列表
# @object Predicate 的指针或者对象
@object_decorator
def traverse_Predicate(list, object):
    display = textwrap.dedent(f'''
                              map Predicate_{object.address} #header:pink;back:lightgreen{{
                                       condition => <Item *> {object['condition']}
                                       used_nodes => <hypergraph::NodeMap> {bin(object['used_nodes'])[2:].zfill(16)}
                                       total_eligibility_set => <hypergraph::NodeMap> {bin(object['total_eligibility_set'])[2:].zfill(16)}
                                       selectivity => <double> {object['selectivity']}
                                       was_join_condition => <bool> {object['was_join_condition']}
                                       source_multiple_equality_idx => <int> {object['source_multiple_equality_idx']}
                                       functional_dependencies.address => <FunctionalDependencySet> {object['functional_dependencies'].address}
                                       functional_dependencies_idx.address => <Mem_root_array<int>> {object['functional_dependencies_idx'].address}
                                       contained_subqueries.address => <Mem_root_array<ContainedSubquery>> {object['contained_subqueries'].address}
                              }}
                              ''')
    g_list_object_string.append(display)

    traverse_Item(g_list_Item, object['condition'])
    add_line(g_list_line, f'Predicate_{object.address}::condition --> Item_', object['condition'], 'condition')

# 探索 JoinPredicate
# @list 存储 JoinPredicate 指针的列表
# @object JoinPredicate 的指针或者对象
@object_decorator
def traverse_JoinPredicate(list, object):
    display = textwrap.dedent(f'''
                              map JoinPredicate_{object.address} #header:pink;back:lightgreen{{
                                       expr => <RelationalExpression *> {object['expr']}
                                       selectivity => <double> {object['selectivity']}
                                       estimated_bytes_per_row => <size_t> {object['estimated_bytes_per_row']}
                                       functional_dependencies.address => <FunctionalDependencySet> {object['functional_dependencies'].address}
                                       functional_dependencies_idx.address => <Mem_root_array<int>> {object['functional_dependencies_idx'].address}
                                       ordering_idx_needed_for_semijoin_rewrite => <int> {object['ordering_idx_needed_for_semijoin_rewrite']}
                                       semijoin_group => <Item **> {object['semijoin_group']}
                                       semijoin_group_size => <int> {object['semijoin_group_size']}
                              }}
                              ''')
    g_list_object_string.append(display)
    
    traverse_RelationalExpression(g_list_RelationalExpression, object['expr'])
    add_line(g_list_line, f'JoinPredicate_{object.address}::expr --> RelationalExpression_', object['expr'], 'expr')

# 探索 RelationalExpression
# @list 存储 RelationalExpression 指针的列表
# @object RelationalExpression 的指针或者对象
@object_decorator
def traverse_RelationalExpression(list, object):
    display = textwrap.dedent(f'''
                              map RelationalExpression_{object.address} #header:pink;back:lightgreen{{
                                       type => <RelationalExpression::Type> {object['type']}
                                       tables_in_subtree => <table_map> {object['tables_in_subtree']}
                                       nodes_in_subtree => <hypergraph::NodeMap> {object['nodes_in_subtree']}
                                       table => <const Table_ref *> {object['table']}
                                       join_conditions_pushable_to_this.address => <Mem_root_array<Item*>> {object['join_conditions_pushable_to_this'].address}
                                       companion_set => <CompanionSet *> {object['companion_set']}
                                       left => <RelationalExpression *> {object['left']}
                                       right => <RelationalExpression *> {object['right']}
                                       multi_children.address => <Mem_root_array<RelationalExpression*>> {object['multi_children'].address}
                                       join_conditions.address => <Mem_root_array<Item*>> {object['join_conditions'].address}
                                       equijoin_conditions.address => <Mem_root_array<Item_eq_base*>> {object['equijoin_conditions'].address}
                                       properties_for_join_conditions.address => <Mem_root_array<CachedPropertiesForPredicate>> {object['properties_for_join_conditions'].address}
                                       properties_for_equijoin_conditions.address => <Mem_root_array<CachedPropertiesForPredicate>> {object['properties_for_equijoin_conditions'].address}
                                       join_conditions_reject_all_rows => <bool> {object['join_conditions_reject_all_rows']}
                                       conditions_used_tables => <table_map> {object['conditions_used_tables']}
                                       join_predicate_first => <int> {object['join_predicate_first']}
                                       join_predicate_last => <int> {object['join_predicate_last']}
                                       conflict_rules.address => <Mem_root_array<ConflictRule>> {object['conflict_rules'].address}
                              }}
                              ''')
    g_list_object_string.append(display)
    
    traverse_RelationalExpression(g_list_RelationalExpression, object['left'])
    add_line(g_list_line, f'RelationalExpression_{object.address}::left --> RelationalExpression_', object['left'], 'left')
    
    traverse_RelationalExpression(g_list_RelationalExpression, object['right'])
    add_line(g_list_line, f'RelationalExpression_{object.address}::right --> RelationalExpression_', object['right'], 'right')
    
    #traverse_Mem_root_array__object(g_list_Mem_root_array__object, object['join_conditions_pushable_to_this'])
    #add_line(g_list_line, f'RelationalExpression_{object.address}::join_conditions_pushable_to_this.address --> Mem_root_array_Item_', object['join_conditions_pushable_to_this'].address, 'join_conditions_pushable_to_this.address')

    traverse_Mem_root_array__object(g_list_Mem_root_array__object, object['join_conditions'])
    add_line(g_list_line, f'RelationalExpression_{object.address}::join_conditions.address --> Mem_root_array_Item_', object['join_conditions'].address, 'join_conditions.address')

    #traverse_Mem_root_array__object(g_list_Mem_root_array__object, object['equijoin_conditions'])
    #add_line(g_list_line, f'RelationalExpression_{object.address}::equijoin_conditions.address --> Mem_root_array_Item_', object['equijoin_conditions'].address, 'equijoin_conditions.address')

    #traverse_Mem_root_array__object(g_list_Mem_root_array__object, object['multi_children'])
    #add_line(g_list_line, f'RelationalExpression_{object.address}::multi_children.address --> Mem_root_array_Item_', object['multi_children'].address, 'multi_children.address')
    
## 探索 hypergraph_Node
## @list 存储 hypergraph_Node 指针的列表
## @object hypergraph_Node 的指针或者对象
#@object_decorator
#def traverse_hypergraph_Node(list, object):
#    display = textwrap.dedent(f'''
#                              map hypergraph_Node_{object.address} #header:pink;back:lightgreen{{
#                                       complex_edges.address => <std::vector<unsigned int, std::allocator<unsigned int> >> {object['complex_edges'].address}
#                                       simple_edges.address => <std::vector<unsigned int, std::allocator<unsigned int> >> {object['simple_edges'].address}
#                                       simple_neighborhood => <hypergraph::NodeMap> {bin(object['simple_neighborhood'])[2:].zfill(16)}
#                                       Size => <const int> {object['Size']}
#                                       padding => <char [8]> {object['padding']}
#                              }}
#                              ''')
#    g_list_object_string.append(display)
#    
#    traverse_std_vector__object(g_list_std_vector__object, object['simple_edges'])
#    add_line(g_list_line, f'hypergraph_Node_{object.address}::simple_edges.address --> std_vector_unsigned_int_', object['simple_edges'].address, 'simple_edges.address')
#    
#
## 探索 hypergraph_Hyperedge
## @list 存储 hypergraph_Hyperedge 指针的列表
## @object hypergraph_Hyperedge 的指针或者对象
#@object_decorator
#def traverse_hypergraph_Hyperedge(list, object):
#    display = textwrap.dedent(f'''
#                              map hypergraph_Hyperedge_{object.address} #header:pink;back:lightgreen{{
#                                       left => <hypergraph::NodeMap> {bin(object['left'])[2:].zfill(16)}
#                                       right => <hypergraph::NodeMap> {bin(object['right'])[2:].zfill(16)}
#                              }}
#                              ''')
#    g_list_object_string.append(display)

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

import textwrap
 
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

class MysqlCommand(gdb.Command):
    def __init__(self):
        super(MysqlCommand, self).__init__(
            "mysql", gdb.COMMAND_USER, prefix=True)

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
        del g_list_List__natural_join_colum[:]   
        del g_list_List__Item_equal[:]           
        del g_list_mem_root_deque__object[:]     
        del g_list_Mem_root_array__object[:]     
        del g_list_Item[:]                       
        del g_list_SQL_I_List__object[:]         
        del g_list_List__object[:]               
        del g_list_JOIN[:]                       
        del g_list_JOIN_TAB[:]
        del g_list_QEP_TAB[:]
        del g_list_QEP_shared[:]
        del g_list_AccessPath[:]
        del g_list_JoinHypergraph[:]
        del g_list_hypergraph_Hypergraph[:]
        del g_list_line[:]                       
        del g_list_object_string[:]
        del g_list_note[:]
        del g_list_hypergraph_Node[:]
        del g_list_hypergraph_Hyperedge[:]
        del g_list_std_vector__object[:]
        del g_list_Predicate[:]
        del g_list_JoinPredicate[:]
        del g_list_RelationalExpression[:]
        
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


class GDB_object(gdb.Command):
    def __init__(self):
        super(GDB_object, self).__init__("mysql object", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):        
        class_type = gdb.lookup_type(arg)
        fields = class_type.fields()
        print(f'                              map {arg}_{{object.address}} #header:pink;back:lightgreen{{{{')
        for field in fields:
            print(f'                                       {field.name} => <{field.type}> {{object[\'{field.name}\']}}')
        print('                              }}')
GDB_object()

class GDB_JoinHypergraph(gdb.Command):
    def __init__(self):
        super(GDB_JoinHypergraph, self).__init__("mysql join_graph", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        del g_list_Query_expression[:]           
        del g_list_Query_block[:]                
        del g_list_Query_term[:]                 
        del g_list_Table_ref[:]                  
        del g_list_Item_field[:]
        del g_list_COND_EQUAL[:]                 
        del g_list_Natural_join_column[:]        
        del g_list_mem_root_deque__Table_ref[:]  
        del g_list_List__natural_join_colum[:]   
        del g_list_List__Item_equal[:]           
        del g_list_mem_root_deque__object[:]     
        del g_list_Mem_root_array__object[:]     
        del g_list_Item[:]                       
        del g_list_SQL_I_List__object[:]         
        del g_list_List__object[:]               
        del g_list_JOIN[:]                       
        del g_list_JOIN_TAB[:]
        del g_list_QEP_TAB[:]
        del g_list_QEP_shared[:]
        del g_list_AccessPath[:]
        del g_list_JoinHypergraph[:]
        del g_list_hypergraph_Hypergraph[:]
        del g_list_line[:]                       
        del g_list_object_string[:]
        del g_list_note[:]
        del g_list_hypergraph_Node[:]
        del g_list_hypergraph_Hyperedge[:]
        del g_list_std_vector__object[:]
        del g_list_Predicate[:]
        del g_list_JoinPredicate[:]
        del g_list_RelationalExpression[:]
        
        expr = gdb.parse_and_eval(arg)
        traverse_JoinHypergraph(g_list_JoinHypergraph, expr)

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
GDB_JoinHypergraph()
