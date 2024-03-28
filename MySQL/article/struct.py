# -*- coding: utf-8 -*-

import gdb

BLOCK_ELEMENTS = 128

g_space = 3          # 缩进空间大小
g_bin_len = 16       # 打印二级制的长度
g_gdb_conv = 'g_gdb_conv'    # gdb 时设置的临时变量

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

# 打印 key
# @space 缩进空间大小
# @key
def print_key(space, key):
    print(f"{' ' * space}\"{key}\":")

# 打印 list 中的内容
# @space 缩进空间大小
# @list
# @callback 回调函数
def print_list(space, list, callback):
    print(f"{' ' * space}[")
    length = len(list)
    for i in range(length):
        if (i < length - 1):
            callback(space + g_space, list[i])
            print(",")
        else:
            callback(space + g_space, list[i])
    print(f"\n{' ' * space}]", end='')

# 打印 key-value，其中 value 为 strint 类型
# @space 缩进空间大小
# @key
# @value
# @end print 的 end 值
def print_key_value_str(space, key, value, end=','):
    print(f"{' ' * space}\"{key}\":  \"{value}\"{end}")

# 打印 key-value，其中 value 为二进制类型
# @space 缩进空间大小
# @key
# @value
# @end print 的 end 值
def print_key_value_bin(space, key, value, end=','):
    print(f"{' ' * space}\"{key}\":  \"{bin(value)[2:].zfill(g_bin_len)}\"{end}")

# 打印 key-value，其中 value 为其他类型
# @space 缩进空间大小
# @key
# @value
# @end print 的 end 值
def print_key_value_oth(space, key, value, end=','):
    print(f"{' ' * space}\"{key}\":  {value}{end}")

# 打印 string
# @space 缩进空间大小
# @string
def print_string(space, string):
    print(f"{' ' * space}\"{string}\"", end = '')

# 打印条件中的 Item
# @space 缩进空间大小
# @item Item的指针
def print_cond_Item(space, item):
    # 递归遍历 item
    def walk(space, item):
        children = []
        item = item.cast(item.dynamic_type)
        gdb.set_convenience_variable(g_gdb_conv,item)
        if (gdb.parse_and_eval('dynamic_cast<Item_cond *>($g_gdb_conv)')):
            print_key(space, item.dynamic_type)
            children = List_to_list(item.dereference()['list'].address)
        elif (gdb.parse_and_eval('dynamic_cast<Item_equal *>($g_gdb_conv)')):
            print_key(space, item.dynamic_type)
            children = List_to_list(item['fields'].address)
        elif (gdb.parse_and_eval('dynamic_cast<Item_func *>($g_gdb_conv)')):
            print_key(space, item.dynamic_type)
            for i in range(item['arg_count']):
                it = item['args'][i]
                children.append(it.cast(it.dynamic_type))
        
        new_space = space + g_space
        print(f"{' ' * new_space}{{")

        for i in range(len(children)):
            my_end = ''
            if i < len(children) - 1:
                my_end = ','
            dynamic_type = str(children[i].dereference().dynamic_type)
            if dynamic_type == 'Item_field':
                print_key_value_str(new_space + g_space, dynamic_type, children[i]['table_name'].string() + '.' + children[i]['field_name'].string(), my_end)
            elif dynamic_type == 'Item_int':
                print_key_value_str(new_space + g_space, dynamic_type, str(children[i]['value']), my_end)
            elif dynamic_type == 'PTI_text_literal_text_string':
                print_key_value_str(new_space + g_space, dynamic_type, children[i]['str_value']['m_ptr'].string(), my_end)
            else:
                # 其他类型的 item 则需要递归遍历
                walk(new_space + g_space * 2, children[i])
                print(my_end)
        print(f"{' ' * (space + g_space)}}}",end='')

    print(f"{' ' * space}{{")
    print_key_value_str(space, '__address__',              item)
    walk(space + g_space, item)
    print()
    print(f"{' ' * space}}}", end='')

# 打印 Table_ref
# @space 缩进空间大小
# @table_ref Table_ref的指针或者值
def print_Table_ref(space, table_ref):
    if table_ref.type.code == gdb.TYPE_CODE_PTR:
        table_ref = table_ref.dereference()
    print(f"{' ' * space}{{")
    new_space = g_space + space
    print_key_value_str(new_space, '__address__',              table_ref.address)
    print_key_value_str(new_space, '__type__',                 'Table_ref')
    print_key_value_str(new_space, 'db',                       table_ref['db'].string())
    print_key_value_str(new_space, 'table_name',               table_ref['table_name'].string())
    print_key_value_oth(new_space, 'm_tableno',                table_ref['m_tableno'])

    if table_ref['m_join_cond'] == 0x0:         
        print_key_value_str(new_space, 'm_join_cond',              table_ref['m_join_cond'])
    else:
        print_key(new_space, 'm_join_cond')
        print_cond_Item(new_space + len('m_join_cond') + g_space, table_ref['m_join_cond'])
        print(',')
    
    print_key_value_str(new_space, 'm_is_sj_or_aj_nest',       table_ref['m_is_sj_or_aj_nest'])
    print_key_value_bin(new_space, 'sj_inner_tables',          table_ref['sj_inner_tables'])

    if table_ref['natural_join'] == 0x0:         
        print_key_value_str(new_space, 'natural_join',              table_ref['natural_join'])
    else:
        print_key(space, 'natural_join')
        print_Table_ref(new_space + len('natural_join') + 2)
    
    print_key_value_str(new_space, 'is_natural_join',                table_ref['is_natural_join'])

    if table_ref['join_using_fields'] == 0x0:
        print_key_value_str(new_space, 'join_using_fields',              table_ref['join_using_fields'])
    else:        
        print_key(new_space, 'join_using_fields')
        join_using_fields_list = List_to_list(table_ref['join_using_fields'])
        print_list(new_space + g_space, join_using_fields_list, print_string)
        print(',')
    
    if table_ref['join_list'] == 0x0:
        print_key_value_str(new_space, 'join_list',              table_ref['join_list'])
    else:        
        print_key(new_space, 'join_list')
        join_list_list = mem_root_deque_to_list(table_ref['join_list'])
        print_list(new_space + len('join_list') + g_space, join_list_list, print_string)
        print(',')

    if table_ref['next_leaf'] == 0x0:
        print_key_value_str(new_space, 'next_leaf',              table_ref['next_leaf'])
    else:        
        print_key(new_space, 'next_leaf')
        print_Table_ref(new_space + len('next_leaf') + g_space, table_ref['next_leaf'])
        print(',')
    
    print_key_value_str(new_space, 'table',                    table_ref['table']['s']['table_name']['str'].string())
    print_key_value_str(new_space, 'outer_join',               table_ref['outer_join'])

    if table_ref['m_join_cond_optim'] == 0x0:         
        print_key_value_str(new_space, 'm_join_cond_optim',              table_ref['m_join_cond_optim'])
    else:
        print_key(new_space, 'm_join_cond_optim')
        print_cond_Item(new_space + len('m_join_cond_optim') + g_space, table_ref['m_join_cond_optim'])
        print(',')

    # natrue join 的列，比如 t1 join t2 using(id,name)。数据类型：List<Natural_join_column> *
    print_key_value_str(new_space, 'join_columns',               table_ref['join_columns'])

    if table_ref['cond_equal'] == 0x0:         
        print_key_value_str(new_space, 'cond_equal',              table_ref['cond_equal'])
    else:
        print_key(new_space, 'cond_equal->current_level')
        cond_equal_list = List_to_list(table_ref['cond_equal']['current_level'])
        print_list(new_space + g_space, cond_equal_list, print_cond_Item)
        print(',')
    
    print_key_value_str(new_space, 'optimized_away',               table_ref['optimized_away'])
    print_key_value_str(new_space, 'query_block',               table_ref['query_block'], end='')

    print(f"{' ' * space}}}",end='')

# 打印 Query_block
# @space 缩进空间大小
# @Query_block Query_block的指针或者值
def print_Query_block(space, query_block):
    if query_block.type.code == gdb.TYPE_CODE_PTR:
        query_block = query_block.dereference()
    print(f"{' ' * space}{{")
    new_space = g_space + space
    print_key_value_str(new_space, '__address__',              query_block.address)
    print_key_value_str(new_space, '__type__',                 'Query_block')

    if query_block['db'] == 0x0:         
        print_key_value_str(new_space, 'db',              query_block['db'])
    else:
        print_key_value_str(new_space, 'db',              query_block['db'].string())
    
    
    print(f"{' ' * space}}}",end='')


class MysqlCommand(gdb.Command):
    def __init__(self):
        super(MysqlCommand, self).__init__(
            "mysql", gdb.COMMAND_USER, prefix=True)
			
class GDB_table_ref(gdb.Command):
    def __init__(self):
        super(GDB_table_ref, self).__init__("mysql table_ref", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        print_Table_ref(0, gdb.parse_and_eval(arg))
        print()

class GDB_query_block(gdb.Command):
    def __init__(self):
        super(GDB_query_block, self).__init__("mysql query_block", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        print_Query_block(0, gdb.parse_and_eval(arg))
        print()

MysqlCommand()
GDB_table_ref()
GDB_query_block()
