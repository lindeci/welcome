%{  // 开始定义部分
/*
Note: YYTHD is passed as an argument to yyparse(), and subsequently to yylex().
*/  // 注意：YYTHD作为参数传递给yyparse()，然后传递给yylex()。
#define YYP (YYTHD->m_parser_state)  // 定义YYP为YYTHD的m_parser_state成员
#define YYLIP (& YYTHD->m_parser_state->m_lip)  // 定义YYLIP为YYTHD的m_parser_state成员的m_lip成员的地址
#define YYPS (& YYTHD->m_parser_state->m_yacc)  // 定义YYPS为YYTHD的m_parser_state成员的m_yacc成员的地址
#define YYCSCL (YYLIP->query_charset)  // 定义YYCSCL为YYLIP指向的对象的query_charset成员
#define YYMEM_ROOT (YYTHD->mem_root)  // 定义YYMEM_ROOT为YYTHD的mem_root成员
#define YYCLIENT_NO_SCHEMA (YYTHD->get_protocol()->has_client_capability(CLIENT_NO_SCHEMA))  // 定义YYCLIENT_NO_SCHEMA为YYTHD的get_protocol()方法返回对象的has_client_capability方法的返回值

#define YYINITDEPTH 100  // 定义YYINITDEPTH为100
#define YYMAXDEPTH 3200                        /* Because of 64K stack */  // 定义YYMAXDEPTH为3200，因为栈大小是64K
#define Lex (YYTHD->lex)  // 定义Lex为YYTHD的lex成员
#define Select Lex->current_query_block()  // 定义Select为Lex指向对象的current_query_block()方法的返回值

…… 很多 include<xxx.h>

/* this is to get the bison compilation windows warnings out */  // 这是为了消除bison编译windows警告
#ifdef _MSC_VER  // 如果定义了_MSC_VER
/* warning C4065: switch statement contains 'default' but no 'case' labels */  // 警告C4065：switch语句包含'default'但没有'case'标签
#pragma warning (disable : 4065)  // 禁用警告4065
#endif  // 结束条件编译

using std::min;  // 使用std命名空间中的min函数
using std::max;  // 使用std命名空间中的max函数

/// The maximum number of histogram buckets.  // 直方图桶的最大数量。
static const int MAX_NUMBER_OF_HISTOGRAM_BUCKETS= 1024;  // 静态常量，直方图桶的最大数量为1024

/// The default number of histogram buckets when the user does not specify it
/// explicitly. A value of 100 is chosen because the gain in accuracy above this
/// point seems to be generally low.  // 当用户没有明确指定直方图桶的数量时，默认的数量。选择100是因为在这个点以上的精度提升似乎通常较低。
static const int DEFAULT_NUMBER_OF_HISTOGRAM_BUCKETS= 100;  // 静态常量，当用户没有明确指定时，直方图桶的默认数量为100

……

%start start_entry  // 定义语法分析的起始符号为start_entry

%parse-param { class THD *YYTHD }  // 定义解析参数为一个指向THD类的指针YYTHD
%parse-param { class Parse_tree_root **parse_tree }  // 定义解析参数为一个指向Parse_tree_root类的双重指针parse_tree

%lex-param { class THD *YYTHD }  // 定义词法分析参数为一个指向THD类的指针YYTHD
%define api.pure                                    /* We have threads */  // 定义api.pure，表示我们有线程
%define api.prefix {my_sql_parser_}  // 定义api.prefix为my_sql_parser_

/*
  1. We do not accept any reduce/reduce conflicts
  2. We should not introduce new shift/reduce conflicts any more.
*/  // 注释：我们不接受任何reduce/reduce冲突，我们不应再引入新的shift/reduce冲突。

%expect 63  // 预期有63个shift/reduce冲突
