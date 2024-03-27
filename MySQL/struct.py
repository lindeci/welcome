# -*- coding: utf-8 -*-

import gdb



class MysqlCommand(gdb.Command):
    def __init__(self):
        super(MysqlCommand, self).__init__(
            "mysql", gdb.COMMAND_USER, prefix=True)
			
class Table_ref:
    def __init__(self, table_ref):
        self.data={
                    'db':					{'_address':'', 'value':'', 'display':'true', 'type':'const char *',                   'comment':'库名'},
                    'table_name':			{'_address':'', 'value':'', 'display':'true', 'type':'const char *',                   'comment':'表名'},
                    'alias':				{'_address':'', 'value':'', 'display':'true', 'type':'const char *',                   'comment':'表的别名'},
                    'm_tableno':			{'_address':'', 'value':'', 'display':'true', 'type':'uint',                           'comment':'表编号'},
                    'm_join_cond':			{'_address':'', 'value':'', 'display':'true', 'type':'Item *',                         'comment':'表名'},
                    'm_is_sj_or_aj_nest':	{'_address':'', 'value':'', 'display':'true', 'type':'bool',                           'comment':'是否 semi join 或者 anti join'},
                    'sj_inner_tables':	    {'_address':'', 'value':'', 'display':'true', 'type':'table_map',                      'comment':'semi join 的内表'},
                    'natural_join':	        {'_address':'', 'value':'', 'display':'true', 'type':'Table_ref *',                    'comment':'自然连接的相关表'},
                    'is_natural_join':	    {'_address':'', 'value':'', 'display':'true', 'type':'bool',                           'comment':'是否为自然连接'},
                    'join_using_fields':	{'_address':'', 'value':'', 'display':'true', 'type':'List<String> *',                 'comment':'join 中 using 字段的列表'},
                    'join_columns':	        {'_address':'', 'value':'', 'display':'true', 'type':'List<Natural_join_column> *',    'comment':'连接列的列表'},
                    'table':	            {'_address':'', 'value':'', 'display':'true', 'type':'TABLE *',                        'comment':'对应的表'},
                    'table_id':	            {'_address':'', 'value':'', 'display':'false', 'type':'mysql::binlog::event::Table_id', 'comment':'binlog event 中的 Table_id'},
                    'derived':	            {'_address':'', 'value':'', 'display':'true', 'type':'Query_expression *',             'comment':'对应的 Query_expression *'},
                    'query_block':	        {'_address':'', 'value':'', 'display':'true', 'type':'Query_block *',                  'comment':'对应的 Query_block *'},
                    'outer_join':	        {'_address':'', 'value':'', 'display':'true', 'type':'bool',                           'comment':'是否是外表'},
                    'join_list':	        {'_address':'', 'value':'', 'display':'true', 'type':'mem_root_deque<Table_ref*> *',   'comment':'连接列表'},
                    'm_join_cond_optim':	{'_address':'', 'value':'', 'display':'true', 'type':'Item *',                         'comment':'优化后的连接条件'},
                    'next_leaf':            {'_address':'', 'value':'', 'display':'true', 'type':'Table_ref *',                    'comment':'Query_block 中的所有表'}
		}
        for i in self.data:
            self.data[i]['value'] = table_ref[i]

    def my_print(self, name, type, value, display, comment):
        if display == 'true':
            if type =='const char *' or type =='char *':
                if value == 0x0:
                    print(name, ':', '0x0', '--', type, '--', comment)
                else:
                    print(name, ':', value.string(), '--', type, '--', comment)
            if type =='uint' or type =='bool':
                print(name, ':', value, '--', type, '--', comment)
            if type == 'Query_expression *' or type == 'Query_block *' or type == 'Table_ref *':
                if value == 0x0:
                    print(name, ':', '0x0', '--', type, '--', comment)
                else:
                    print(name, ':', value, '--', type, '--', comment)
            if type == 'List<String> *':
                if value == 0x0:
                     print(name, ':', '0x0', '--', type, '--', comment)
                else:
                    print(name, ':', end='')
                    nodetype = value.dereference().type.template_argument(0)
                    first = value.dereference()['first']
                    last = value.dereference()['last'].dereference()
                    elements = value.dereference()['elements']
                    while first != last:
                        info = first['info']
                        info_dynamic_type = info.cast(nodetype.pointer()).dynamic_type
                        print(info.cast(info_dynamic_type),end='')
                        first = first['next']
                    print('--', type, '--', comment)

    def print(self):
        for i in self.data:
            #print(self.data[i],self.data[i]['value'], '     --', self.data[i]['comment'])
            self.my_print(i, self.data[i]['type'], self.data[i]['value'], self.data[i]['display'], self.data[i]['comment'])
			
class GDB_table_ref(gdb.Command):
    def __init__(self):
        super(GDB_table_ref, self).__init__("mysql table_ref", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        table_ref = Table_ref(gdb.parse_and_eval(arg))
        table_ref.print()

MysqlCommand()
GDB_table_ref()
