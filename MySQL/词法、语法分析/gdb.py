import gdb

BLOCK_ELEMENTS = 128
num_blocks = gdb.parse_and_eval('thd->lex->query_block->m_table_nest.num_blocks()')
if (num_blocks):
    BLOCK_ELEMENTS = gdb.parse_and_eval(
        'thd->lex->query_block->m_table_nest->m_capacity/thd->lex->query_block->m_table_nest.num_blocks()')

g_conv = 'g_conv'
g_tab = ' ' * 5

def myprint(level, *args, **kwargs):
    __builtins__.print(g_tab*level, *args, **kwargs)

def mem_root_deque_to_list(deque):
    out_list = []
    m_begin_idx = deque['m_begin_idx']
    m_end_idx = deque['m_end_idx']
    while m_begin_idx != m_end_idx:
        element = deque['m_blocks'][m_begin_idx /
                                    BLOCK_ELEMENTS]['elements'][m_begin_idx % BLOCK_ELEMENTS]
        out_list.append(element)
        m_begin_idx += 1
    return out_list

def SQL_I_List_to_list(list, next_key):
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

def table_ref_to_list(table_ref, next_key):
    out_list = []
    while table_ref:
        out_list.append(table_ref)
        table_ref = table_ref.dereference()[next_key]
    return out_list

def List_to_list(list):
    out_list = []
    nodetype = list.dereference().type.template_argument(0)
    first = list.dereference()['first']
    last = list.dereference()['last'].dereference()
    elements = list.dereference()['elements']
    while first != last:
        info = first['info']
        info_dynamic_type = info.cast(nodetype.pointer()).dynamic_type
        out_list.append(info.cast(info_dynamic_type))
        first = first['next']
    return out_list

def Mem_root_array_to_list(array):
    out_list = []
    m_size = array.dereference()['m_size']
    for i in range(m_size):
        out_list.append(array.dereference()['m_array'][i])
    return out_list

def std_vector_to_list(vector):
    out_list = []
    value_reference = vector['_M_impl']['_M_start']
    while value_reference != vector['_M_impl']['_M_finish']:
        out_list.append(value_reference.dereference())
        value_reference += 1
    return out_list

def std_array_to_list(array):
    out_list = []
    array_size = array.type.template_argument(1)
    for i in range(array_size):
        out_list.append(array['_M_elems'][i])
    return out_list

def print_list(list, callback):
    length = len(list)
    for i in range(length):
        if (i < length - 1):
            callback(list[i])
            print(",", end='')
        else:
            callback(list[i])


def display_table_ref(table_ref):
    print(f"table_ref: {{",
          f"addr: {table_ref}, "
          f"table_name: {table_ref.dereference()['table_name'].string()}, "
          f"alias: {table_ref.dereference()['alias'].string()}, "
          f"derived: {table_ref.dereference()['derived']}, "
          f"query_block: {table_ref.dereference()['query_block']} }}", end='')


def display_block(block):
    print(f"{{"
          f"addr: {block}, "
          f"master: {block.dereference()['master']}, "
          f"slave: {block.dereference()['slave']}, "
          f"next: {block.dereference()['next']}, "
          f"link_prev: {block.dereference()['link_prev'].dereference()}, "
          f"link_nex: {block.dereference()['link_next']}, "
          f"m_table_list: {{", end='')
    m_table_list = SQL_I_List_to_list(block['m_table_list'], 'next_local')
    leaf_tables = table_ref_to_list(block['leaf_tables'], 'next_leaf')
    print_list(m_table_list, display_table_ref)
    m_table_nest = mem_root_deque_to_list(block['m_table_nest'])
    print(f"}}, m_table_nest: {{", end='')
    print_list(m_table_nest, display_table_ref)
    print(f"}}, leaf_tables: {{", end='')
    print_list(leaf_tables, display_table_ref)
    print(f"}} }}")
    print("")


def display_expression(expr):
    print(f"{{"
          f"addr: {expr}, "
          f"master: {expr.dereference()['master']}, "
          f"slave: {expr.dereference()['slave']}, "
          f"next: {expr.dereference()['next']}, "
          f"prev: {expr.dereference()['prev']}, "
          f"explain_marker: {expr.dereference()['explain_marker']}, "
          f"m_query_term: {{addr: {expr.dereference()['m_query_term']}, "
          f"dynamic_type: '{expr.dereference()['m_query_term'].dynamic_type}' }} }}")
    print("")


def display_term(term):
    dynamic_type = term.dynamic_type
    print(f"{{"
          f"addr: {term}, "
          f"dynamic_type: '{dynamic_type}'", end='')
    if (str(dynamic_type) == 'Query_term *' or term == 0x0 or str(dynamic_type) == 'Query_block *'):
        print(f"}}", end='')
        return
    m_children = mem_root_deque_to_list(
        term.cast(dynamic_type).dereference()['m_children'])
    m_generation = term.cast(dynamic_type).dereference()[
        'm_children']['m_generation']
    print(f", m_block: {term.cast(dynamic_type).dereference()['m_block']}"
          f", m_parent: {term.cast(dynamic_type).dereference()['m_parent']}"
          f", m_owning_operand: {term.cast(dynamic_type).dereference()['m_owning_operand']}", end = '')
    m_result_table = term.cast(dynamic_type).dereference()['m_result_table']
    print(f", m_result_table: {m_result_table}", end = '')
    m_fields = term.cast(dynamic_type).dereference()['m_fields']
    print(f", m_fields: {m_fields}", end = '')
    if (m_result_table != 0x0):
        print(f", m_result_table.table_ref: ", end = '')
        display_table_ref(m_result_table)
        #print("--------")
        #print(m_result_table.dereference())
        #print("--------")
    if (m_fields != 0x0):
        m_fields_list = mem_root_deque_to_list(m_fields)
        print(f", m_fields.len: {len(m_fields_list)}", end = '')
    print(f", m_curr_id: {term.cast(dynamic_type).dereference()['m_curr_id']}"
          f", m_generation: {m_generation}", end='')
    if (m_generation == 0):
        print(f"}}")
        return
    print(", m_children: [", end='')
    for i in range(m_generation):
        display_term(m_children[i])
        if (i < m_generation - 1):
            print(",", end='')
    print("]}", end='')

#def display_item(item):
#    dynamic_type = item.dynamic_type
#    print(dynamic_type)
#    print(item.cast(dynamic_type).dereference())
#    for i in range(item.cast(dynamic_type).dereference()['arg_count']):
#        print(i)
#        print(item.cast(dynamic_type).dereference()['args'].dereference()[i])


class MysqlCommand(gdb.Command):
    def __init__(self):
        super(MysqlCommand, self).__init__(
            "mysql", gdb.COMMAND_USER, prefix=True)


class GDB_expr(gdb.Command):
    def __init__(self):
        super(GDB_expr, self).__init__("mysql expr", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        self.printed_expression = {}
        self.printed_block = {}
        expr = gdb.parse_and_eval(arg)
        self.traverse_expressions(expr)
        print(f"m_query_term: ", end='')
        display_term(expr.dereference()['m_query_term'])
        print("")

    def traverse_blocks(self, expr):
        self.printed_block[str(expr)] = True
        print("query_block: ", end='')
        display_block(expr)
        if (expr.dereference()['master'] != 0x0):
            if (str(expr.dereference()['master']) not in self.printed_expression):
                self.traverse_expressions(expr.dereference()['master'])

        if (expr.dereference()['slave'] != 0x0):
            if (str(expr.dereference()['slave']) not in self.printed_expression):
                self.traverse_expressions(expr.dereference()['slave'])

        if (expr.dereference()['next'] != 0x0):
            if (str(expr.dereference()['next']) not in self.printed_block):
                self.traverse_blocks(expr.dereference()['next'])

        if (expr.dereference()['link_prev'] != 0x0 and expr.dereference()['link_prev'].dereference() != 0x0):
            if (str(expr.dereference()['link_prev'].dereference()) not in self.printed_block):
                self.traverse_blocks(expr.dereference()[
                                     'link_prev'].dereference())

    def traverse_expressions(self, expr):
        self.printed_expression[str(expr)] = True
        print("query_expression: ", end='')
        display_expression(expr)
        if (expr.dereference()['master'] != 0x0):
            if (str(expr.dereference()['master']) not in self.printed_block):
                self.traverse_blocks(expr.dereference()['master'])

        if (expr.dereference()['slave'] != 0x0):
            if (str(expr.dereference()['slave']) not in self.printed_block):
                self.traverse_blocks(expr.dereference()['slave'])

        if (expr.dereference()['next'] != 0x0):
            if (str(expr.dereference()['next']) not in self.printed_expression):
                self.traverse_expressions(expr.dereference()['next'])

        if (expr.dereference()['prev'] != 0x0):
            if (str(expr.dereference()['prev'].dereference()) not in self.printed_expression):
                self.traverse_expressions(expr.dereference()['prev'].dereference())

class GDB_item(gdb.Command):
    def __init__(self):
        super(GDB_item, self).__init__("mysql item", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        self.graph = []
        item = gdb.parse_and_eval(arg)
        casted_item = item.cast(item.dynamic_type)
        print('    ' * 0, '', casted_item, item.dereference().dynamic_type)
        self.walk(casted_item, 0, ' ')

    def walk(self, item, level, prefix):
        children = []
        gdb.set_convenience_variable('conv',item)
        if (gdb.parse_and_eval('dynamic_cast<Item_cond *>($conv)')):
            #print(1)
            children = self.walk_Item_cond(item)
        elif (gdb.parse_and_eval('dynamic_cast<Item_equal *>($conv)')):
            #print(3)
            children = self.walk_Item_equal(item)
        elif (gdb.parse_and_eval('dynamic_cast<Item_func *>($conv)')):
            #print(2)
            children = self.walk_Item_func(item)
            
        for i in range(len(children)):
            if len(children) == 1:
                print(prefix, '|-->', children[i], children[i].dereference().dynamic_type, self.display_item(children[i]))
                tmp_prefix = prefix + ' |   '
            elif i == len(children) - 1:
                print(prefix, '`-->', children[i], children[i].dereference().dynamic_type, self.display_item(children[i]))
                tmp_prefix = prefix + '     '
            else:
                print(prefix, '|-->', children[i], children[i].dereference().dynamic_type, self.display_item(children[i]))
                tmp_prefix = prefix + ' |   '
            self.walk(children[i], level + 1, tmp_prefix)

            if (str(item.dereference().type) == 'Item_equal'):
                if (item.dereference()['m_const_arg']):
                    m_const_arg = item.dereference()['m_const_arg']
                    print(prefix, '`-->', m_const_arg, m_const_arg.dereference().dynamic_type, self.display_item(m_const_arg))


    def walk_Item_func(self, item):
        children = []
        for i in range(item['arg_count']):
            it = item['args'][i]
            children.append(it.cast(it.dynamic_type))
        return children

    def walk_Item_cond(self, item):
        return List_to_list(item.dereference()['list'].address)

    def walk_Item_equal(self, item):
        return List_to_list(item.dereference()['fields'].address)

    def display_item(self, item):
        result = ''
        dynamic_type = str(item.dereference().dynamic_type)
        if dynamic_type == 'Item_field':
            result += ':   ' + item['field_name'].string()
        if dynamic_type == 'Item_int':
            result += ':   ' + str(item['value'])
        if dynamic_type == 'PTI_text_literal_text_string':
            result += ':   ' + '\'' + item['str_value']['m_ptr'].string() + '\''
        return result

class GDB_join(gdb.Command):
    def __init__(self):
        super(GDB_join, self).__init__("mysql join", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        self.graph = []
        item = gdb.parse_and_eval(arg)['cond_equal']['current_level']
        #children = List_to_list(item.address)
        #for i in range(len(children)):
        #    print(children[i].dereference().type)
        #casted_item = item.cast(item.dynamic_type)
        print('    ' * 0, '', item.address, item.dynamic_type)
        self.walk(item.address, 0, ' ')

    def walk(self, item, level, prefix):
        children = []
        children = self.walk_List(item)
        # if (str(item.dereference().type) == 'List<Item_field>'):
        for i in range(len(children)):
            if len(children) == 1:
                print(prefix, '|-->', children[i], children[i].dereference().dynamic_type, self.display_item(children[i]))
                tmp_prefix = prefix + ' |   '
            elif i == len(children) - 1:
                print(prefix, '`-->', children[i], children[i].dereference().dynamic_type, self.display_item(children[i]))
                tmp_prefix = prefix + '     '
            else:
                print(prefix, '|-->', children[i], children[i].dereference().dynamic_type, self.display_item(children[i]))
                tmp_prefix = prefix + ' |   '
            
            if (str(item.dereference().type) == 'List<Item_equal>'):
                #print(children[i].dereference()['fields'])
                self.walk(children[i].dereference()['fields'].address, level + 1, tmp_prefix)
                if (children[i].dereference()['m_const_arg']):
                    m_const_arg = children[i].dereference()['m_const_arg']
                    #print(tmp_prefix,1)
                    print(tmp_prefix, '`-->', m_const_arg, m_const_arg.dereference().dynamic_type, self.display_item(m_const_arg))

    def walk_List(self, item):
        return List_to_list(item)

    def display_item(self, item):
        result = ''
        dynamic_type = str(item.dereference().dynamic_type)
        if dynamic_type == 'Item_field':
            result += ':   ' + item['field_name'].string()
        if dynamic_type == 'Item_int':
            result += ':   ' + str(item['value'])
        if dynamic_type == 'PTI_text_literal_text_string':
            result += ':   ' + '\'' + item['str_value']['m_ptr'].string() + '\''
        return result

class GDB_comb(gdb.Command):
    def __init__(self):
        super(GDB_comb, self).__init__("mysql comb", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        print('------- mysql query expression -------')
        gdb.execute('mysql expr thd->lex->unit')
        print('')
        print('------- mysql where condition -------')
        gdb.execute('mysql item thd->lex->query_block->m_where_cond')
        print('')
        print('------- mysql join predicate -------')
        gdb.execute('mysql join thd->lex->unit->slave->join')

class GDB_JoinHypergraph(gdb.Command):
    def __init__(self):
        super(GDB_JoinHypergraph, self).__init__("mysql joinHyper", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        graph = gdb.parse_and_eval(arg)

        print('-----------JoinHypergraph::table_num_to_node_num-----------')
        self.display_table_num_to_node_num(graph['table_num_to_node_num'])

        print('')
        print('-----------JoinHypergraph::graph-----------')
        self.display_Hypergraph(graph['graph'])

        print('')
        print('-----------JoinHypergraph::nodes-----------')
        self.display_nodes(graph['nodes'])

        print('')
        print('-----------JoinHypergraph::edges<JoinPMem_root_array<JoinPredicate>>-----------')
        self.display_edges(graph['edges'].address)

        print('')
        print('-----------JoinHypergraph::predicates<Mem_root_array<Predicate>>-----------')
        self.display_predicates(graph['predicates'].address)

        print('')
        print('-----------JoinHypergraph::num_where_predicates-----------')
        print(f"num_where_predicates: {graph['num_where_predicates']}")

    def display_table_num_to_node_num(self, vector):
        table_num_to_node_num = std_array_to_list(vector)
        for i in range(len(table_num_to_node_num)):
            if (table_num_to_node_num[i] == -1):
                break
            print(f"table_num_to_node_num[{i}]={table_num_to_node_num[i]}")

    def display_Hypergraph(self, graph):
        edges = Mem_root_array_to_list(graph['edges'].address)
        for i in range(len(edges)):
            self.display_graph_edge(i, edges[i])
        nodes = Mem_root_array_to_list(graph['nodes'].address)
        print('')
        for i in range(len(nodes)):
            self.display_graph_node(i, nodes[i])

    def display_graph_edge(self, index, edge):
        print(f"edge[{index}]: {{"
            f"left: {bin(edge['left'])[2:].zfill(10)}   "
            f"right: {bin(edge['right'])[2:].zfill(10)}}}")

    def display_graph_node(self, index, node):
        simple_edges = std_vector_to_list(node['simple_edges'])
        complex_edges = std_vector_to_list(node['complex_edges'])

        print(f"node[{index}]: {{"
            f"simple_neighborhood: {bin(node['simple_neighborhood'])[2:].zfill(10)}   "
            f"simple_edges: {{", end = '')

        for i in range(len(simple_edges)):
            if (i == len(simple_edges) - 1):
                print(simple_edges[i], end = '}   ')
            else:
                print(simple_edges[i], end = ',')

        print(f"complex_edges: {{", end = '')
        for i in range(len(complex_edges)):
            if (i == len(complex_edges) - 1):
                print(complex_edges[i], end = '}')
            else:
                print(complex_edges[i], end = ',')
        if (len(complex_edges) == 0):
            print('}', end = '')
        print(' }')

    def display_nodes(self,nodes):
        nodes_list = Mem_root_array_to_list(nodes.address)
        for i in range(len(nodes_list)):
            print(f"nodes[{i}]:")
            print(f"table: {nodes_list[i]['table']['s']['table_name']['str'].string()}")
            join_conditions_pushable_to_this = Mem_root_array_to_list(nodes_list[i]['join_conditions_pushable_to_this'].address)
            sargable_predicates = Mem_root_array_to_list(nodes_list[i]['sargable_predicates'].address)
            companion_set = nodes_list[i]['companion_set']


            for j in range(len(join_conditions_pushable_to_this)):
                print(f"join_conditions_pushable_to_this[{j}]:")
                gdb.set_convenience_variable(g_conv,join_conditions_pushable_to_this[j])
                gdb.execute('mysql item $' + g_conv)

            for j in range(len(sargable_predicates)):
                print(f"sargable_predicates[{j}]: {{"
                    f"predicate_index: {sargable_predicates[j]['predicate_index']} "
                    f"field: {sargable_predicates[j]['field']} "
                    f"other_side: {sargable_predicates[j]['other_side']}"
                    f"can_evaluate: {sargable_predicates[j]['can_evaluate']}"
                    f"}}")
            
            print('')
            print('companion_set: ')
            m_equal_terms = Mem_root_array_to_list(companion_set['m_equal_terms'].address)
            for j in range(len(m_equal_terms)):
                print(f"m_equal_terms[{j}]: {{", end = '')
                fields = Mem_root_array_to_list(m_equal_terms[j]['fields'])
                print(f"fields: {[i['field_name'].string() for i in fields]}   ", end = '')
                #for k in range(len(fields)):
                #    print(fields[k]['field_name'].string(), end = '  ')
                #print('')
                print(f"tables: {bin(m_equal_terms[j]['tables'])[2:].zfill(10)} }}")
            print('----')

    def display_edges(self,edges):
        edges = Mem_root_array_to_list(edges)
        for i in range(len(edges)):
            expr = edges[i]['expr']
            print(f"edges[{i}]: {{ expr<RelationalExpression*>: {expr} }}")

    def display_predicates(self,predicates):
        predicates = Mem_root_array_to_list(predicates)
        for i in range(len(predicates)):
            condition = predicates[i]['condition']
            print(f"predicates[{i}]: {{ ")
            gdb.set_convenience_variable(g_conv,condition)
            gdb.execute('mysql item $' + g_conv)
            print(f" }}")

class GDB_RelationalExpression(gdb.Command):
    def __init__(self):
        super(GDB_RelationalExpression, self).__init__("mysql rel_expr", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        rel_expr = gdb.parse_and_eval(arg)
        self.display_RelationalExpression(rel_expr)
    
    def display_RelationalExpression(self, rel_expr):
        print(f"RelationalExpression: {rel_expr}")
        print(f"type: {rel_expr.dereference()['type']}")
        table = ''
        if (str(rel_expr.dereference()['type']) == 'RelationalExpression::TABLE'):
            table = rel_expr.dereference()['table']['alias'].string()
        print(f"table: {table}")
        print(f"left: {rel_expr.dereference()['left']}")
        print(f"right: {rel_expr.dereference()['right']}")
        print(f"tables_in_subtree: {rel_expr.dereference()['tables_in_subtree']}")
        print(f"nodes_in_subtree: {bin(rel_expr.dereference()['nodes_in_subtree'])[2:].zfill(10)}")
        multi_children = Mem_root_array_to_list(rel_expr.dereference()['multi_children'].address)
        print((f"multi_children<RelationalExpression>: {multi_children}"))
        join_conditions_pushable_to_this = Mem_root_array_to_list(rel_expr.dereference()['join_conditions_pushable_to_this'].address)
        print((f"join_conditions_pushable_to_this<Item*>: {[str(i.address) for i in join_conditions_pushable_to_this]}"))
        print('')

        if (rel_expr.dereference()['left'] and str(rel_expr.dereference()['left']) != '0x8f8f8f8f8f8f8f8f'):
            self.display_RelationalExpression(rel_expr.dereference()['left'])
        if (rel_expr.dereference()['right'] and str(rel_expr.dereference()['right']) != '0x8f8f8f8f8f8f8f8f'):
            self.display_RelationalExpression(rel_expr.dereference()['right'])


MysqlCommand()
GDB_item()
GDB_expr()
GDB_join()
GDB_comb()
GDB_JoinHypergraph()
GDB_RelationalExpression()


"""
-exec mysql expr thd->lex->unit
-exec mysql item thd->lex->unit->slave->m_where_cond
-exec mysql item thd->lex->m_current_query_block->m_where_cond

-exec p thd->lex->m_current_query_block->m_where_cond

-exec mysql item ((Item_equal*)thd->lex->unit->slave->join->cond_equal->current_level->first->info)
-exec mysql join thd->lex->unit->slave->join

-exec p ((Item_equal*)thd->lex->unit->slave->join->cond_equal->current_level->first->next->next->next->next->next->info)->m_const_arg->str_value->m_ptr

-exec p ((Item_field*)thd->lex->m_current_query_block->m_where_cond->list[2]->fields->first->info)->item_name->m_str

ItemToString(join->where_cond).c_str())

-exec p ItemToString((Item*)((Item_equal*)thd->lex->unit->slave->join->cond_equal->current_level->first->info)).c_str()
$9 = 0xffff30b3bc90 "multiple equal(customer.C_CUSTKEY, orders.O_CUSTKEY)"

-exec p PrintRelationalExpression(root, 0)

-exec mysql joinHyper graph

-exec mysql rel_expr graph->edges->m_array[0]->expr
"""