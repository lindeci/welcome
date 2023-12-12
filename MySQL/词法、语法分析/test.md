```plantuml
participant Alice
participant Bob
@enduml
```

```plantuml
class Address
@enduml
```

#include <iostream>
#include <typeinfo>

class Base {
public:
    virtual ~Base() {}
};

class Derived : public Base {};

int main() {
    Base* b = new Derived();

    if(Derived* d = dynamic_cast<Derived*>(b)) {
        std::cout << "b is a Derived class object\n";
    } else {
        std::cout << "b is not a Derived class object\n";
    }

    std::cout << "typeid(b).name(): " << typeid(b).name() << '\n';
    std::cout << "typeid(*b).name(): " << typeid(*b).name() << '\n';

    delete b;
    return 0;
}

cat CMakeCache.txt |grep -i rtti  
ENABLE_RTTI:UNINITIALIZED=ON
protobuf_DISABLE_RTTI:BOOL=OFF


cat CMakeCache.txt | grep -i CMAKE_C_COMPILER
cat CMakeCache.txt | grep -i CMAKE_CXX_COMPILER

cmake3 --no-warn-unused-cli -DWITH_BOOST=/data/boost_1_77_0 -DWITH_DEBUG=1 -DBUILD_CONFIG=mysql_release -gdwarf-2 -DCMAKE_BUILD_TYPE:STRING=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE -S/data/mysql-server -B/data/mysql-server/build -G "Unix Makefiles" -DENABLE_RTTI=ON

cmake3 --no-warn-unused-cli -DWITH_BOOST=/data/boost_1_77_0 -DWITH_DEBUG=1 -DBUILD_CONFIG=mysql_release -gdwarf-2 -DCMAKE_BUILD_TYPE:STRING=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE -S/data/mysql-server -B/data/mysql-server/build -G "Unix Makefiles" -DWITH_RTTI=ON -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc

cmake3 --build /data/mysql-server/build --config Debug --target component_reference_cache -j 32

cmake3 --build /data/mysql-server/build --config Debug --target mysqld -j 32



  std::cout<<typeid(*this).name()<<std::endl;

"cmake.configureArgs": [
  "-DWITH_BOOST=/data/boost_1_77_0",
  "-DWITH_DEBUG=1",
  "-DBUILD_CONFIG=mysql_release",
  "-gdwarf-2",
  "-DWITH_RTTI=ON"
]

"cmake.configureArgs": [
  "-DWITH_BOOST=/data/boost_1_77_0",
  "-DWITH_DEBUG=1",
  "-DBUILD_CONFIG=mysql_release",
  "-gdwarf-2",
  "-DWITH_RTTI=ON",
  "-DCMAKE_CXX_COMPILER=g++",
  "-DCMAKE_C_COMPILER=gcc"
]


"version": "0.2.0",
    "configurations": [
        {
            "miDebuggerPath": "/opt/rh/devtoolset-11/root/usr/bin/gdb", /*GDB版本可能不支持typeid()*/
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/build/runtime_output_directory/mysqld-debug",
            "args": [
                "--user=mysql",
                "--datadir=${workspaceFolder}/build/runtime_output_directory/../data",
                "--socket=${workspaceFolder}/build/runtime_output_directory/../data/mysql.sock.lock"
            ],
            "stopAtEntry": false,
            "cwd": "${fileDirname}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                },
                {
                    "description": "Set Disassembly Flavor to Intel",
                    "text": "-gdb-set disassembly-flavor intel",
                    "ignoreFailures": true
                }/*,
                {
                    "description": "Enable RTTI for gdb",
                    "text": "-rtti",
                    "ignoreFailures": true
                }*/
            ]
    }
    ]

set debug = 'd,info:n:N:F:i:L:o,/tmp/mysqld.trace'
SET SESSION debug = '+d,ast,info:n:N:F:i:L:o,debug,error,enter,exit,exec_result,prep_stmt_exec';

SET SESSION debug = '+d,ast,info,debug,error,exit,exec_result,prep_stmt_exec';

select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3;




这个是gdb时打印的堆栈信息，格式不好看，帮我美化格式，要求不能删除内容，你主要根据逗号和花括号进行缩进和对齐，每次遇到花括号，要缩进，花括号里的内容左边都要对齐，风格类似json格式，但不严格要求满足json的语法


define print_queue
set $head = fifo_queue_head
while $head != 0
print *$head
set $head = $head->next
end

for (Item *&item : value)
p item

-exec p *((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_lhs

$81 = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x860d890 <vtable for PT_query_specification+16>, contextualized = false, m_pos = {cpp = {start = 0x7fff34afa440 "select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_I"..., end = 0x7fff34afa4d8 " union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3"}, raw = {start = 0x7fff34afa2f0 "select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_I"..., end = 0x7fff34afa388 " union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3"}}}, <No data fields>}


-exec p *((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_rhs

$82 = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x860d890 <vtable for PT_query_specification+16>, contextualized = false, m_pos = {cpp = {start = 0x7fff34afa4e3 "select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3", end = 0x7fff34afa574 " order by id desc limit 3"}, raw = {start = 0x7fff34afa393 "select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3", end = 0x7fff34afa424 " order by id desc limit 3"}}}, <No data fields>}


-exec p typeid(*((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_lhs).name()


-exec p  *(PT_query_specification*)((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_rhs



-exec p  *(PT_query_specification*)((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_rhs
$85 = {<PT_query_primary> = {<PT_query_expression_body> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x860d890 <vtable for PT_query_specification+16>, contextualized = false, m_pos = {cpp = {start = 0x7fff34afa4e3 "select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3", end = 0x7fff34afa574 " order by id desc limit 3"}, raw = {start = 0x7fff34afa393 "select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3", end = 0x7fff34afa424 " order by id desc limit 3"}}}, <No data fields>}, <No data fields>}, opt_hints = 0x0, options = {query_spec_options = 0}, item_list = 0x7fff34b179d0, opt_into1 = 0x0, m_is_from_clause_implicit = false, from_clause = {static has_trivial_destructor = <optimized out>, m_root = 0x7fff340146f0, m_array = 0x7fff34b19348, m_size = 1, m_capacity = 20}, opt_where_clause = 0x7fff34b19668, opt_group_clause = 0x0, opt_having_clause = 0x0, opt_window_clause = 0x0}


-exec p  *(PT_query_specification*)((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_lhs
$86 = {<PT_query_primary> = {<PT_query_expression_body> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x860d890 <vtable for PT_query_specification+16>, contextualized = false, m_pos = {cpp = {start = 0x7fff34afa440 "select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_I"..., end = 0x7fff34afa4d8 " union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3"}, raw = {start = 0x7fff34afa2f0 "select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_I"..., end = 0x7fff34afa388 " union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3"}}}, <No data fields>}, <No data fields>}, opt_hints = 0x0, options = {query_spec_options = 0}, item_list = 0x7fff34afabd0, opt_into1 = 0x0, m_is_from_clause_implicit = false, from_clause = {static has_trivial_destructor = <optimized out>, m_root = 0x7fff340146f0, m_array = 0x7fff34b17390, m_size = 1, m_capacity = 20}, opt_where_clause = 0x7fff34b176b0, opt_group_clause = 0x0, opt_having_clause = 0x0, opt_window_clause = 0x0}


-exec p  *(PT_select_item_list*)(((PT_query_specification*)((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_rhs)->item_list)


-exec p  *(PT_select_item_list*)(((PT_query_specification*)((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_rhs)->item_list)
$89 = {<PT_item_list> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x860c4e8 <vtable for PT_select_item_list+16>, contextualized = false, m_pos = {cpp = {start = 0x7fff34afa4ea "p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3", end = 0x7fff34afa528 " from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3"}, raw = {start = 0x7fff34afa39a "p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3", end = 0x7fff34afa3d8 " from processlist p left join threads t on p.id=t.PROCESSLIST_ID  where id=8 order by id desc limit 3"}}}, value = {static block_elements = <optimized out>, m_blocks = 0x7fff34b17a30, m_begin_idx = 64, m_end_idx = 70, m_capacity = 128, m_root = 0x7fff340146f0, m_generation = 6}}, <No data fields>}

-exec p  *(PT_select_item_list*)(((PT_query_specification*)((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_lhs)->item_list)
$90 = {<PT_item_list> = {<Parse_tree_node_tmpl<Parse_context>> = {_vptr.Parse_tree_node_tmpl = 0x860c4e8 <vtable for PT_select_item_list+16>, contextualized = false, m_pos = {cpp = {start = 0x7fff34afa447 "p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THR"..., end = 0x7fff34afa48d " from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p."...}, raw = {start = 0x7fff34afa2f7 "p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('1','1') as func from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THR"..., end = 0x7fff34afa33d " from processlist p left join threads t on p.id=t.PROCESSLIST_ID where id=5 union all select p.id,p.user,p.state,t.THREAD_ID,t.THREAD_OS_ID,concat('2','1') from processlist p left join threads t on p."...}}}, value = {static block_elements = <optimized out>, m_blocks = 0x7fff34afac30, m_begin_idx = 64, m_end_idx = 70, m_capacity = 128, m_root = 0x7fff340146f0, m_generation = 6}}, <No data fields>}



-exec set $l_item_list = (PT_select_item_list*)(((PT_query_specification*)((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_lhs)->item_list)

-exec p *($l_item_list->value)[0]
-exec p *($l_item_list->value)[1]
-exec p *($l_item_list->value)[2]
-exec p *($l_item_list->value)[3]
-exec p *($l_item_list->value)[4]
-exec p *($l_item_list->value)[5]

-exec p typeid(*(*(PTI_expr_with_alias*)(($l_item_list->value)[0]))->expr).name()
$75 = 0x6551230 <typeinfo name for PTI_simple_ident_q_2d> "21PTI_simple_ident_q_2d"
-exec p typeid(*(*(PTI_expr_with_alias*)(($l_item_list->value)[1]))->expr).name()
$76 = 0x6551230 <typeinfo name for PTI_simple_ident_q_2d> "21PTI_simple_ident_q_2d"
-exec p typeid(*(*(PTI_expr_with_alias*)(($l_item_list->value)[2]))->expr).name()
$77 = 0x6551230 <typeinfo name for PTI_simple_ident_q_2d> "21PTI_simple_ident_q_2d"
-exec p typeid(*(*(PTI_expr_with_alias*)(($l_item_list->value)[3]))->expr).name()
$78 = 0x6551230 <typeinfo name for PTI_simple_ident_q_2d> "21PTI_simple_ident_q_2d"
-exec p typeid(*(*(PTI_expr_with_alias*)(($l_item_list->value)[4]))->expr).name()
$79 = 0x6551230 <typeinfo name for PTI_simple_ident_q_2d> "21PTI_simple_ident_q_2d"
-exec p typeid(*(*(PTI_expr_with_alias*)(($l_item_list->value)[5]))->expr).name()
$80 = 0x6551140 <typeinfo name for PTI_function_call_generic_ident_sys> "35PTI_function_call_generic_ident_sys"



-exec p (*(PTI_simple_ident_q_2d*)(*(PTI_expr_with_alias*)(($l_item_list->value)[0]))->expr)->field
$29 = 0x7fff348d65a8 "id"
-exec p (*(PTI_simple_ident_q_2d*)(*(PTI_expr_with_alias*)(($l_item_list->value)[1]))->expr)->field
$30 = 0x7fff348d6bd0 "user"
-exec p (*(PTI_simple_ident_q_2d*)(*(PTI_expr_with_alias*)(($l_item_list->value)[2]))->expr)->field
$31 = 0x7fff348d6d90 "state"
-exec p (*(PTI_simple_ident_q_2d*)(*(PTI_expr_with_alias*)(($l_item_list->value)[3]))->expr)->field
$32 = 0x7fff348d6f50 "THREAD_ID"
-exec p (*(PTI_simple_ident_q_2d*)(*(PTI_expr_with_alias*)(($l_item_list->value)[4]))->expr)->field
$35 = 0x7fff348d7118 "THREAD_OS_ID"
-exec p (*(PTI_function_call_generic_ident_sys*)(*(PTI_expr_with_alias*)(($l_item_list->value)[5]))->expr)->ident
$34 = {str = 0x7fff348d72d8 "concat", length = 6}


-exec p (*(PTI_function_call_generic_ident_sys*)(*(PTI_expr_with_alias*)((((PT_select_item_list*)(((PT_query_specification*)((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_lhs)->item_list))->value)[5]))->expr)->ident

-exec p (*(PTI_function_call_generic_ident_sys*)(*(PTI_expr_with_alias*)((((PT_select_item_list*)(((PT_query_specification*)((PT_union *)((PT_query_expression*)(*(PT_select_stmt*)parse_tree)->m_qe)->m_body)->m_rhs)->item_list))->value)[5]))->expr)->ident

-exec set print pretty on