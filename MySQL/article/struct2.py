import gdb

BLOCK_ELEMENTS = 128

g_space = 3          # 缩进空间大小
g_bin_len = 16       # 打印二级制的长度
g_gdb_conv = 'g_gdb_conv'    # gdb 时设置的临时变量

g_query_expression_list = []      # 全局 query_expression 的 list，里面的元素是指针
g_query_block_list = []           # 全局 query_block 的 list，里面的元素是指针
g_query_term_list = []            # 全局 query_term 的 list，里面的元素是指针, 只存放 ['Query_term_except','Query_term_intersect','Query_term_unary','Query_term_union'] 这4种类型
g_table_ref = []                  # 全局 Table_ref 的 list, 里面的元素是指针

g_line = []
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

#def display_block(block):
#    print(f"{{"
#          f"addr: {block}, "
#          f"master: {block.dereference()['master']}, "
#          f"slave: {block.dereference()['slave']}, "
#          f"next: {block.dereference()['next']}, "
#          f"link_prev: {block.dereference()['link_prev'].dereference()}, "
#          f"link_nex: {block.dereference()['link_next']}, "
#          f"m_table_list: {{", end='')
#    m_table_list = SQL_I_List_to_list(block['m_table_list'], 'next_local')
#    leaf_tables = table_ref_to_list(block['leaf_tables'], 'next_leaf')
#    print_list(m_table_list, display_table_ref)
#    m_table_nest = mem_root_deque_to_list(block['m_table_nest'])
#    print(f"}}, m_table_nest: {{", end='')
#    print_list(m_table_nest, display_table_ref)
#    print(f"}}, leaf_tables: {{", end='')
#    print_list(leaf_tables, display_table_ref)
#    print(f"}} }}")
#    print("")
#
#
#def display_expression(expr):
#    print(f"{{"
#          f"addr: {expr}, "
#          f"master: {expr.dereference()['master']}, "
#          f"slave: {expr.dereference()['slave']}, "
#          f"next: {expr.dereference()['next']}, "
#          f"prev: {expr.dereference()['prev']}, "
#          f"explain_marker: {expr.dereference()['explain_marker']}, "
#          f"m_query_term: {{addr: {expr.dereference()['m_query_term']}, "
#          f"dynamic_type: '{expr.dereference()['m_query_term'].dynamic_type}' }} }}")
#    print("")
#
#
#def display_term(term):
#    dynamic_type = term.dynamic_type
#    print(f"{{"
#          f"addr: {term}, "
#          f"dynamic_type: '{dynamic_type}'", end='')
#    if (str(dynamic_type) == 'Query_term *' or term == 0x0 or str(dynamic_type) == 'Query_block *'):
#        print(f"}}", end='')
#        return
#    m_children = mem_root_deque_to_list(
#        term.cast(dynamic_type).dereference()['m_children'])
#    m_generation = term.cast(dynamic_type).dereference()[
#        'm_children']['m_generation']
#    print(f", m_block: {term.cast(dynamic_type).dereference()['m_block']}"
#          f", m_parent: {term.cast(dynamic_type).dereference()['m_parent']}"
#          f", m_owning_operand: {term.cast(dynamic_type).dereference()['m_owning_operand']}", end = '')
#    m_result_table = term.cast(dynamic_type).dereference()['m_result_table']
#    print(f", m_result_table: {m_result_table}", end = '')
#    m_fields = term.cast(dynamic_type).dereference()['m_fields']
#    print(f", m_fields: {m_fields}", end = '')
#    if (m_result_table != 0x0):
#        print(f", m_result_table.table_ref: ", end = '')
#        display_table_ref(m_result_table)
#        #print("--------")
#        #print(m_result_table.dereference())
#        #print("--------")
#    if (m_fields != 0x0):
#        m_fields_list = mem_root_deque_to_list(m_fields)
#        print(f", m_fields.len: {len(m_fields_list)}", end = '')
#    print(f", m_curr_id: {term.cast(dynamic_type).dereference()['m_curr_id']}"
#          f", m_generation: {m_generation}", end='')
#    if (m_generation == 0):
#        print(f"}}")
#        return
#    print(", m_children: [", end='')
#    for i in range(m_generation):
#        display_term(m_children[i])
#        if (i < m_generation - 1):
#            print(",", end='')
#    print("]}", end='')

class MysqlCommand(gdb.Command):
    def __init__(self):
        super(MysqlCommand, self).__init__(
            "mysql", gdb.COMMAND_USER, prefix=True)

# 打印 Query_expression
# @expr Query_expression的指针或者对象
def display_Query_expression(expr):
    if expr.type.code == gdb.TYPE_CODE_PTR:
        expr = expr.dereference()
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
            "end note \n")

    print("class Query_term_set_op { \n"
            "    - Query_block *m_block \n"
            "    + mem_root_deque<Query_term*> m_children \n"
            "    + int64_t m_last_distinct \n"
            "    + int64_t m_first_distinct \n"
            "    + bool m_is_materialized \n"
            "} \n"
            "note right of Query_term_set_op::m_block \n"
            "    所属的 Query_block\n"
            "end note \n")

    print("class Query_block { \n"
            "} \n")

    print("class Query_term_except { \n"
            "} \n")

    print("class Query_term_intersect { \n"
            "} \n")

    print("class Query_term_unary { \n"
            "} \n")

    print("class Query_term_union { \n"
            "} \n")

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
        
        for i in g_line:
            print(str(i))

        print_class()
        
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

        m_table_list = SQL_I_List_to_list(block['m_table_list'], 'next_local')

        
        leaf_tables = table_ref_to_list(block['leaf_tables'], 'next_leaf')
        print_list(m_table_list, display_table_ref)
        m_table_nest = mem_root_deque_to_list(block['m_table_nest'])

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
