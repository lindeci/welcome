- [Innovation and LTS 的规划](#innovation-and-lts-的规划)
- [环境准备](#环境准备)
- [检查是否支持向量语法](#检查是否支持向量语法)
- [详细目标](#详细目标)
- [mysql 客户端对向量关键字的支持](#mysql-客户端对向量关键字的支持)
- [在 libmysql 库中添加对向量的支持](#在-libmysql-库中添加对向量的支持)
- [词法分析调整](#词法分析调整)
- [语法分析调整](#语法分析调整)
- [对向量函数支持的调整](#对向量函数支持的调整)
  - [新增向量函数](#新增向量函数)
- [在 Item 中的调整](#在-item-中的调整)
- [日志事件打印](#日志事件打印)
- [数据包](#数据包)
- [解析树数据类型的支持](#解析树数据类型的支持)
- [协议](#协议)
- [主从复制](#主从复制)
- [插入](#插入)
- [优化器](#优化器)
- [分区表](#分区表)
- [sql\_prepare](#sql_prepare)
- [show](#show)
- [建表](#建表)
- [字典表](#字典表)
- [字典、视图](#字典视图)
- [分区](#分区)
- [查询组件接口](#查询组件接口)
- [存储过程接口](#存储过程接口)
- [bind](#bind)
- [客户端 SQL](#客户端-sql)
- [存储引擎层](#存储引擎层)
  - [全文检索接口](#全文检索接口)
  - [数据结构、函数和宏](#数据结构函数和宏)
  - [记录比较](#记录比较)
  - [myisam](#myisam)
  - [handler](#handler)
  - [NDB](#ndb)
- [MySQL 字段类型新增向量字段类型](#mysql-字段类型新增向量字段类型)
- [添加向量字段类型对应的类](#添加向量字段类型对应的类)
- [在系统表的数据字典中添加向量字段的支持](#在系统表的数据字典中添加向量字段的支持)
- [字段之间复制的函数](#字段之间复制的函数)
- [在物理字段上的支持](#在物理字段上的支持)
- [备份工具对向量字段的支持](#备份工具对向量字段的支持)
- [调整 binlog 的事件对向量的支持](#调整-binlog-的事件对向量的支持)
- [pluginx 对向量的支持](#pluginx-对向量的支持)
- [向量转换函数](#向量转换函数)
- [跟踪分析](#跟踪分析)
  - [简单跟踪 vector\_dim](#简单跟踪-vector_dim)

# Innovation and LTS 的规划
https://dev.mysql.com/doc/refman/9.0/en/mysql-releases.html

MySQL Release Schedule

![MySQL Release Schedule](https://dev.mysql.com/doc/refman/9.0/en/images/mysql-lts-innovation-versioning-graph.png)

# 环境准备
查看 OS 版本
```
cat /etc/os-release 
NAME="CentOS Linux"
VERSION="7 (Core)"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="7"
PRETTY_NAME="CentOS Linux 7 (Core)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:centos:centos:7"
HOME_URL="https://www.centos.org/"
BUG_REPORT_URL="https://bugs.centos.org/"

CENTOS_MANTISBT_PROJECT="CentOS-7"
CENTOS_MANTISBT_PROJECT_VERSION="7"
REDHAT_SUPPORT_PRODUCT="centos"
REDHAT_SUPPORT_PRODUCT_VERSION="7"
```

编译安装启动 MySQL
```sh
cmake3 --no-warn-unused-cli -DWITH_BOOST=/data/ldc_docker/boost_1_77_0 -DWITH_DEBUG=1 -DBUILD_CONFIG=mysql_release -DWITH_RTTI=ON -DWITH_SHOW_PARSE_TREE=ON -DCMAKE_BUILD_TYPE:STRING=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE -S/data/ldc_docker/mysql-server_9.0.0 -B/data/ldc_docker/mysql-server_9.0.0/build -G "Unix Makefiles"

cmake3 --build /data/ldc_docker/mysql-server_9.0.0/build --config Debug --target mysqld -j 32
cmake3 --build /data/ldc_docker/mysql-server_9.0.0/build --config Debug --target mysql -j 32
cmake3 --build /data/ldc_docker/mysql-server_9.0.0/build --config Debug --target component_reference_cache -j 32

chown -R mysql.mysql /data/ldc_docker/mysql-server_9.0.0/data
/data/ldc_docker/mysql-server_9.0.0/build/runtime_output_directory/mysqld-debug --initialize --user=mysql --basedir=/data/ldc_docker/mysql-server_9.0.0/build --datadir=/data/ldc_docker/mysql-server_9.0.0/data

/data/ldc_docker/mysql-server_9.0.0/build/runtime_output_directory/mysqld-debug --user=mysql --datadir=/data/ldc_docker/mysql-server_9.0.0/data --socket=/data/ldc_docker/mysql-server_9.0.0/data/mysql.sock.lock --mysqlx-port=33061 --mysqlx_socket=/data/ldc_docker/mysql-server_9.0.0/data/mysqlx.sock &

/data/ldc_docker/mysql-server_9.0.0/build/runtime_output_directory/mysql -uroot -p'root' --socket=/data/ldc_docker/mysql-server_9.0.0/data/mysql.sock.lock
```

```
启动时报错：
2024-07-08T03:11:08.288642Z 0 [ERROR] [MY-011300] [Server] Plugin mysqlx reported: 'Setup of bind-address: '*' port: 33060 failed, `bind()` failed with error: Address already in use (98). Do you already have another mysqld server running with Mysqlx ?'
2024-07-08T03:11:08.288659Z 0 [ERROR] [MY-013597] [Server] Plugin mysqlx reported: 'Value '*' set to `Mysqlx_bind_address`, X Plugin can't bind to it. Skipping this value.'
2024-07-08T03:11:08.288682Z 0 [ERROR] [MY-011300] [Server] Plugin mysqlx reported: 'Setup of socket: '/tmp/mysqlx.sock' failed, another process with PID 17564 is using UNIX socket file'

需要添加启动参数 
--mysqlx-port=33061 --mysqlx_socket=/data/ldc_docker/mysql-server_9.0.0/data/mysqlx.sock

原因：
show plugins;
+----------------------------------+----------+--------------------+---------+---------+
| Name                             | Status   | Type               | Library | License |
+----------------------------------+----------+--------------------+---------+---------+
| binlog                           | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| sha256_password                  | ACTIVE   | AUTHENTICATION     | NULL    | GPL     |
| caching_sha2_password            | ACTIVE   | AUTHENTICATION     | NULL    | GPL     |
| sha2_cache_cleaner               | ACTIVE   | AUDIT              | NULL    | GPL     |
| daemon_keyring_proxy_plugin      | ACTIVE   | DAEMON             | NULL    | GPL     |
| CSV                              | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| MEMORY                           | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| InnoDB                           | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| INNODB_TRX                       | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMP                       | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMP_RESET                 | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMPMEM                    | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMPMEM_RESET              | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMP_PER_INDEX             | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMP_PER_INDEX_RESET       | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_BUFFER_PAGE               | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_BUFFER_PAGE_LRU           | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_BUFFER_POOL_STATS         | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_TEMP_TABLE_INFO           | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_METRICS                   | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_DEFAULT_STOPWORD       | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_DELETED                | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_BEING_DELETED          | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_CONFIG                 | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_INDEX_CACHE            | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_FT_INDEX_TABLE            | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_TABLES                    | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_TABLESTATS                | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_INDEXES                   | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_TABLESPACES               | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_COLUMNS                   | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_VIRTUAL                   | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CACHED_INDEXES            | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_SESSION_TEMP_TABLESPACES  | ACTIVE   | INFORMATION SCHEMA | NULL    | GPL     |
| MyISAM                           | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| MRG_MYISAM                       | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| PERFORMANCE_SCHEMA               | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| TempTable                        | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| ARCHIVE                          | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| BLACKHOLE                        | ACTIVE   | STORAGE ENGINE     | NULL    | GPL     |
| FEDERATED                        | DISABLED | STORAGE ENGINE     | NULL    | GPL     |
| ndbcluster                       | DISABLED | STORAGE ENGINE     | NULL    | GPL     |
| ndbinfo                          | DISABLED | STORAGE ENGINE     | NULL    | GPL     |
| ndb_transid_mysql_connection_map | DISABLED | INFORMATION SCHEMA | NULL    | GPL     |
| ngram                            | ACTIVE   | FTPARSER           | NULL    | GPL     |
| mysqlx_cache_cleaner             | ACTIVE   | AUDIT              | NULL    | GPL     |
| mysqlx                           | ACTIVE   | DAEMON             | NULL    | GPL     |
+----------------------------------+----------+--------------------+---------+---------+
47 rows in set (0.01 sec)

可以看到 mysqlx

mysqlx 介绍：
https://dev.mysql.com/doc/refman/9.0/en/document-store.html

```

# 检查是否支持向量语法
```sql
SELECT VERSION();
+-------------+
| VERSION()   |
+-------------+
| 9.0.0-debug |
+-------------+
1 row in set (0.00 sec)

create database test_vector;

use test_vector;

-- 创建支持 vector 字段类型的表
create table t_vector(id int,c_v vector);

-- 插入向量
insert into t_vector values(1,to_vector('[1,1]')),(2,to_vector('[2,2,2]'));

-- 查看表数据
select * from t_vector;                 
+------+----------------------------+
| id   | c_v                        |
+------+----------------------------+
|    1 | 0x0000803F0000803F         |
|    2 | 0x000000400000004000000040 |
+------+----------------------------+
2 rows in set (0.00 sec)

-- 查看向量维度
select id,vector_dim(c_v) from t_vector;
+------+-----------------+
| id   | vector_dim(c_v) |
+------+-----------------+
|    1 |               2 |
|    2 |               3 |
+------+-----------------+
2 rows in set (0.00 sec)

-- 查看向量数据
select id,from_vector(c_v) from t_vector;
+------+---------------------------------------+
| id   | from_vector(c_v)                      |
+------+---------------------------------------+
|    1 | [1.00000e+00,1.00000e+00]             |
|    2 | [2.00000e+00,2.00000e+00,2.00000e+00] |
+------+---------------------------------------+
2 rows in set (0.00 sec)
```

# 详细目标
```
vector
to_vector(...)
from_vector(...)
vector_dim(...)
```
# mysql 客户端对向量关键字的支持
client/mysql.cc 文件调整
```cpp
……
static COMMANDS commands[] = {
        ……
        {"TO_VECTOR", 0, nullptr, false, ""},
        {"STRING_TO_VECTOR", 0, nullptr, false, ""},
        {"FROM_VECTOR", 0, nullptr, false, ""},
        {"VECTOR_TO_STRING", 0, nullptr, false, ""},
        {"VECTOR_DIM", 0, nullptr, false, ""},
        ……
……

static bool is_binary_field(MYSQL_FIELD *field) {
  return (
      (field->charsetnr == 63) &&
      (field->type == MYSQL_TYPE_BIT || field->type == MYSQL_TYPE_BLOB ||
       field->type == MYSQL_TYPE_LONG_BLOB ||
       field->type == MYSQL_TYPE_MEDIUM_BLOB ||
       field->type == MYSQL_TYPE_TINY_BLOB ||
       field->type == MYSQL_TYPE_VAR_STRING ||
       field->type == MYSQL_TYPE_STRING || field->type == MYSQL_TYPE_VARCHAR ||
       field->type == MYSQL_TYPE_VECTOR || field->type == MYSQL_TYPE_GEOMETRY));
}
……
```
sql-common/client.cc 文件调整
```cpp
const char *fieldtype2str(enum enum_field_types type) {
  switch (type) {
    case MYSQL_TYPE_BIT:
      return "BIT";
    case MYSQL_TYPE_BLOB:
      return "BLOB";
    case MYSQL_TYPE_VECTOR:
      return "VECTOR";
    ……
```

# 在 libmysql 库中添加对向量的支持
对 `libmysql/libmysql.cc` 进行调整，把字符串转换成对应的数据类型
```cpp
static void fetch_string_with_conversion(MYSQL_BIND *param, char *value,
                                         size_t length) {
  ……
  switch (param->buffer_type) {
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_DECIMAL:
    case MYSQL_TYPE_NEWDECIMAL:
    default: {
      /*
        Copy column data to the buffer taking into account offset,
        data length and buffer length.
      */
      char *start = value + param->offset;
      char *end = value + length;
      size_t copy_length;
      if (start < end) {
        copy_length = end - start;
        /* We've got some data beyond offset: copy up to buffer_length bytes */
        if (param->buffer_length)
          memcpy(buffer, start,
                 std::min<size_t>(copy_length, param->buffer_length));
      } else
        copy_length = 0;
      if (copy_length < param->buffer_length) buffer[copy_length] = '\0';
      *param->error = copy_length > param->buffer_length;
      /*
        param->length will always contain length of entire column;
        number of copied bytes may be way different:
      */
      *param->length = (unsigned long)length;
      break;
    }
    ……
  ……
```
继续调整，检查两个字段类型是否在二进制协议中兼容，即它们是否具有相同的二进制表示并需要客户端缓冲区的相同类型
```cpp
static bool is_binary_compatible(enum enum_field_types type1,
                                 enum enum_field_types type2) {
  static const enum enum_field_types
      range1[] = {MYSQL_TYPE_SHORT, MYSQL_TYPE_YEAR, MYSQL_TYPE_NULL},
      range2[] = {MYSQL_TYPE_INT24, MYSQL_TYPE_LONG, MYSQL_TYPE_NULL},
      range3[] = {MYSQL_TYPE_DATETIME, MYSQL_TYPE_TIMESTAMP, MYSQL_TYPE_NULL},
      range4[] = {
          MYSQL_TYPE_ENUM,        MYSQL_TYPE_SET,        MYSQL_TYPE_TINY_BLOB,
          MYSQL_TYPE_MEDIUM_BLOB, MYSQL_TYPE_LONG_BLOB,  MYSQL_TYPE_BLOB,
          MYSQL_TYPE_VECTOR,      MYSQL_TYPE_VAR_STRING, MYSQL_TYPE_STRING,
          MYSQL_TYPE_GEOMETRY,    MYSQL_TYPE_DECIMAL,    MYSQL_TYPE_NULL};
  static const enum enum_field_types *range_list[] = {range1, range2, range3,
                                                      range4},
                                     **range_list_end =
                                         range_list + sizeof(range_list) /
                                                          sizeof(*range_list);
  const enum enum_field_types **range, *type;

  if (type1 == type2) return true;
  for (range = range_list; range != range_list_end; ++range) {
    /* check that both type1 and type2 are in the same range */
    bool type1_found = false, type2_found = false;
    for (type = *range; *type != MYSQL_TYPE_NULL; type++) {
      type1_found |= type1 == *type;
      type2_found |= type2 == *type;
    }
    if (type1_found || type2_found) return type1_found && type2_found;
  }
  return false;
}
```
继续调整，设置用于结果集中某一列的提取函数
```cpp
static bool setup_one_fetch_function(MYSQL_BIND *param, MYSQL_FIELD *field) {
  DBUG_TRACE;

  /* Setup data copy functions for the different supported types */
  switch (param->buffer_type) {
    ……
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_BIT:
      assert(param->buffer_length != 0);
      param->fetch_result = fetch_result_bin;
      break;
    ……
  ……
  /* Setup skip_result functions (to calculate max_length) */
  param->skip_result = skip_result_fixed;
  switch (field->type) {
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    ……
    case MYSQL_TYPE_JSON:
      param->skip_result = skip_result_string;
      break;
    ……
  }
```

# 词法分析调整
在 `sql/lex.h` 中添加关键字
```cpp
……
static const SYMBOL symbols[] = {
    ……
    {SYM("VECTOR", VECTOR_SYM)},
    ……
```

# 语法分析调整
在 `sql/sql_yacc.yy` 中添加对 VECTOR_SYM 的语法分析支持

```cpp
...
/* 定义新的 token VECTOR_SYM */
%token<lexer.keyword> VECTOR_SYM 1215
...
/* 字段类型的语法 */
type:
          ……
            | VECTOR_SYM opt_field_length
          {
            $$= NEW_PTN PT_vector_type(@$, $2);
          }
          ……

/*添加关键字 VECTOR*/
ident_keywords_unambiguous:
        ……
        | VECTOR_SYM
```

# 对向量函数支持的调整
对于 `to_vector`、`from_vector`、`vector_dim` 这3个向量相关函数，跟其它大部分函数一样，通过 `PTI_function_call_generic_ident_sys` 生成

函数分析的语法规则配置在 `sql/sql_yacc.yy`
```cpp
……
function_call_generic:
          IDENT_sys '(' opt_udf_expr_list ')'
          {
            $$= NEW_PTN PTI_function_call_generic_ident_sys(@$, $1, $3);
          }
        | ident '.' ident '(' opt_expr_list ')'
          {
            $$= NEW_PTN PTI_function_call_generic_2d(@$, $1, $3, $5);
          }
        ;
……
```

## 新增向量函数
在 `plugin/x/src/mysql_function_names.cc` 中添加新的函数名字
```cpp
……
const char *const native_mysql_functions[] = {
    ……
    "FROM_VECTOR",
    ……
    "STRING_TO_VECTOR",
    ……
    "TO_VECTOR",
    ……
    "VECTOR_DIM",
    "VECTOR_TO_STRING",
    ……
```

在 `sql/item_create.cc` 中添加上面函数名字对应的构造方法
```cpp
static const std::pair<const char *, Create_func *> func_array[] = {
    ……
    {"TO_VECTOR", SQL_FN(Item_func_to_vector, 1)},
    {"STRING_TO_VECTOR", SQL_FN(Item_func_to_vector, 1)},
    {"FROM_VECTOR", SQL_FN(Item_func_from_vector, 1)},
    {"VECTOR_TO_STRING", SQL_FN(Item_func_from_vector, 1)},
    {"VECTOR_DIM", SQL_FN(Item_func_vector_dim, 1)},
    ……
```

在 `sql/item_strfunc.h` 中添加上面构造方法 `Item_func_to_vector` 和 `Item_func_from_vector` 对应的类
```cpp
……
class Item_func_to_vector final : public Item_str_func {
  String buffer;

 public:
  Item_func_to_vector(const POS &pos, Item *a) : Item_str_func(pos, a) {}
  bool resolve_type(THD *thd) override;
  const char *func_name() const override { return "to_vector"; }
  String *val_str(String *str) override;
};

class Item_func_from_vector final : public Item_str_func {
  static const uint32 per_value_chars = 16;
  static const uint32 max_output_bytes =
      (Field_vector::max_dimensions * Item_func_from_vector::per_value_chars);
  String buffer;

 public:
  Item_func_from_vector(const POS &pos, Item *a) : Item_str_func(pos, a) {
    collation.set(&my_charset_utf8mb4_0900_bin);
  }
  bool resolve_type(THD *thd) override;
  const char *func_name() const override { return "from_vector"; }
  String *val_str(String *str) override;
};
……
```

在 `sql/item_func.h` 中添加 上面构造方法 `Item_func_vector_dim` 对应的类
```cpp
……
class Item_func_vector_dim : public Item_int_func {
  String value;

 public:
  Item_func_vector_dim(const POS &pos, Item *a) : Item_int_func(pos, a) {}
  longlong val_int() override;
  const char *func_name() const override { return "vector_dim"; }
  bool resolve_type(THD *thd) override {
    if (param_type_is_default(thd, 0, 1, MYSQL_TYPE_VECTOR)) {
      return true;
    }
    bool valid_type = (args[0]->data_type() == MYSQL_TYPE_VECTOR) ||
                      (args[0]->result_type() == STRING_RESULT &&
                       args[0]->collation.collation == &my_charset_bin);
    if (!valid_type) {
      my_error(ER_WRONG_ARGUMENTS, MYF(0), func_name());
      return true;
    }
    max_length = 10;
    return false;
  }
};
……
```

在 sql/item_func.cc 中调整
```cpp
uint Item_func::num_vector_args() {
  uint num_vectors = 0;
  for (uint i = 0; i < arg_count; i++) {
    /* VECTOR type fields should not participate as function arguments. */
    if (args[i]->data_type() == MYSQL_TYPE_VECTOR) {
      num_vectors++;
    }
  }
  return num_vectors;
}

……

bool Item_func_get_user_var::propagate_type(THD *,
                                            const Type_properties &type) {
  /*
    If the type is temporal: user variables don't support that type; so, we
    use a VARCHAR instead. Same for JSON and GEOMETRY.
    BIT and YEAR types are represented with LONGLONG.
  */
  switch (type.m_type) {
    ……
    case MYSQL_TYPE_VECTOR:
      set_data_type_vector(
          Field_vector::dimension_bytes(Field_vector::max_dimensions));
      break;
    default:
      assert(false);
  }
  ……
}


……


/*
    Syntax:
      string get_dd_char_length()
*/
longlong Item_func_internal_dd_char_length::val_int() {
  ……
  if (field_type == MYSQL_TYPE_VECTOR) {
    /* For vector types, we can return the field_length as is. */
    return field_length;
  }

  ……

  return 0;
}
```

# 在 Item 中的调整
在 `sql/item.h` 中的调整
```cpp
class Item : public Parse_tree_node {
  ……
// Return the default result type for a given data type
  static Item_result type_to_result(enum_field_types type) {
    switch (type) {
      ……
      case MYSQL_TYPE_BLOB:
      case MYSQL_TYPE_VECTOR:
      case MYSQL_TYPE_GEOMETRY:
      case MYSQL_TYPE_JSON:
      case MYSQL_TYPE_ENUM:
      case MYSQL_TYPE_SET:
        return STRING_RESULT;
      ……
    }
    assert(false);
    return INVALID_RESULT;
  }

  ……

  static enum_field_types type_for_variable(enum_field_types src_type) {
    switch (src_type) {
      ……
      case MYSQL_TYPE_BLOB:
      case MYSQL_TYPE_VECTOR:
      case MYSQL_TYPE_MEDIUM_BLOB:
      case MYSQL_TYPE_LONG_BLOB:
        return MYSQL_TYPE_VARCHAR;
      ……
    }
    assert(false);
    return MYSQL_TYPE_NULL;
  }

  ……

  /**
    Set the data type of the Item to be VECTOR.
  */
  void set_data_type_vector(uint32 max_l) {
    set_data_type(MYSQL_TYPE_VECTOR);
    collation.set(&my_charset_bin, DERIVATION_IMPLICIT);
    decimals = DECIMAL_NOT_SPECIFIED;
    max_length = max_l;
  }
```

调整 sql/item.cc  
聚合函数
```cpp
bool Item::aggregate_type(const char *name, Item **items, uint count) {
  ……

  // Operate on "new" types only
  new_type = real_type_to_type(new_type);

  // Calculate remaining type properties and set complete data type
  switch (new_type) {
    ……
    case MYSQL_TYPE_JSON:
      set_data_type_json();
      break;

    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_STRING:
    case MYSQL_TYPE_VARCHAR:
    case MYSQL_TYPE_TINY_BLOB:
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_SET:
    case MYSQL_TYPE_ENUM:
      if (aggregate_string_properties(new_type, name, items, count))
        return true;
      break;

    ……
  }

  ……
}
```

```cpp
bool Item_field::check_function_as_value_generator(uchar *checker_args) {
  ……

  if (field->real_type() == MYSQL_TYPE_VECTOR) {
    /* Vector typed column cannot be used in generated column expression */
    if (func_args->source == VGS_DEFAULT_EXPRESSION) {
      my_error(ER_INCORRECT_TYPE, MYF(0), field->field_name,
               "DEFAULT EXPRESSION"); /* LCOV_EXCL_LINE */
    } else if (func_args->source == VGS_CHECK_CONSTRAINT) {
      my_error(ER_INCORRECT_TYPE, MYF(0), field->field_name,
               "CHECK CONSTRAINT");
    } else {
      my_error(ER_INCORRECT_TYPE, MYF(0), field->field_name,
               "GENERATED COLUMN");
    }
    return true;
  }

  ……
}
```
```cpp
bool Item::is_blob_field() const {
  assert(fixed);

  const enum_field_types type = data_type();
  return (type == MYSQL_TYPE_BLOB || type == MYSQL_TYPE_VECTOR ||
          type == MYSQL_TYPE_GEOMETRY ||
          // Char length, not the byte one, should be taken into account
          max_length / collation.collation->mbmaxlen >
              CONVERT_IF_BIGGER_TO_BLOB);
}
```

```cpp
bool Item_param::propagate_type(THD *, const Type_properties &type) {
  assert(type.m_type != MYSQL_TYPE_INVALID);
  switch (type.m_type) {
    ……
    case MYSQL_TYPE_VECTOR:
      set_data_type_vector(
          Field_vector::dimension_bytes(Field_vector::max_dimensions));
      break;
    ……
  }

  m_result_type = type_to_result(data_type());

  return false;
}
```

```cpp
Field *Item::tmp_table_field_from_field_type(TABLE *table,
                                             bool fixed_length) const {
  /*
    The field functions defines a field to be not null if null_ptr is not 0
  */
  Field *field;

  switch (data_type()) {
    ……
    case MYSQL_TYPE_VECTOR:
      field = new (*THR_MALLOC) Field_vector(
          max_length, m_nullable, item_name.ptr(), collation.collation);
      break;
    ……
  }
  if (field) field->init(table);
  return field;
}
```

```cpp
bool Item::send(Protocol *protocol, String *buffer) {
  switch (data_type()) {
    default:
    case MYSQL_TYPE_NULL:
    case MYSQL_TYPE_BOOL:
    case MYSQL_TYPE_INVALID:
    case MYSQL_TYPE_DECIMAL:
    case MYSQL_TYPE_ENUM:
    case MYSQL_TYPE_SET:
    case MYSQL_TYPE_TINY_BLOB:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_GEOMETRY:
    case MYSQL_TYPE_STRING:
    case MYSQL_TYPE_VAR_STRING:
    case MYSQL_TYPE_VARCHAR:
    case MYSQL_TYPE_BIT:
    case MYSQL_TYPE_NEWDECIMAL:
    case MYSQL_TYPE_JSON: {
      const String *res = val_str(buffer);
      assert(null_value == (res == nullptr));
      if (res != nullptr)
        return protocol->store_string(res->ptr(), res->length(),
                                      res->charset());
      break;
    }
    ……
  }

  assert(null_value);
  if (current_thd->is_error()) return true;
  return protocol->store_null();
}
```

```cpp
bool Item::evaluate(THD *thd, String *buffer) {
  assert(result_type() != ROW_RESULT);

  switch (data_type()) {
    ……
    case MYSQL_TYPE_NULL:
    case MYSQL_TYPE_DECIMAL:
    case MYSQL_TYPE_ENUM:
    case MYSQL_TYPE_SET:
    case MYSQL_TYPE_TINY_BLOB:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_GEOMETRY:
    case MYSQL_TYPE_STRING:
    case MYSQL_TYPE_VAR_STRING:
    case MYSQL_TYPE_VARCHAR:
    case MYSQL_TYPE_BIT: {
      (void)val_str(buffer);
      break;
    }
    ……
  }
  const bool result = thd->is_error();
  // Convention: set NULL value indicator on error
  if (result) null_value = true;
  return result;
}
```
```cpp
bool Item::aggregate_string_properties(enum_field_types type, const char *name,
                                       Item **items, uint nitems) {
  ……

  switch (type) {
    ……
    case MYSQL_TYPE_VECTOR:
      set_data_type_vector(char_width);
      break;

    ……
  }
  return false;
}
```

```cpp
bool Item_insert_value::fix_fields(THD *thd, Item **reference) {
  ……

  if (thd->lex->in_update_value_clause &&
      field_arg->field->table->insert_values) {
    Field *def_field = field_arg->field->clone(thd->mem_root);
    if (def_field == nullptr) return true;

    def_field->move_field_offset((ptrdiff_t)(def_field->table->insert_values -
                                             def_field->table->record[0]));
    m_rowbuffer_saved = def_field->table->insert_values;
    /*
      Put the original and cloned Field_blob objects in
      'insert_update_values_map' map. This will be used to make a
      separate copy of blob value, in case 'UPDATE' clause is executed in
      'INSERT...UPDATE' statement. See mysql_prepare_blob_values()
      for more info. We are only checking for MYSQL_TYPE_BLOB and
      MYSQL_TYPE_GEOMETRY. Sub types of blob like TINY BLOB, LONG BLOB, JSON,
      are internally stored are BLOB only. Same applies to geometry type.
    */
    if ((def_field->type() == MYSQL_TYPE_BLOB ||
         def_field->type() == MYSQL_TYPE_VECTOR ||
         def_field->type() == MYSQL_TYPE_GEOMETRY)) {
      try {
        thd->lex->insert_values_map(field_arg, def_field);
      } catch (std::bad_alloc const &) {
        my_error(ER_STD_BAD_ALLOC_ERROR, MYF(0), "", "fix_fields");
        return true;
      }
    }

    set_field(def_field);

    // Use same field name as the underlying field:
    assert(field_name == nullptr);
    field_name = arg->item_name.ptr();

    // The VALUES function is deprecated.
    if (m_is_values_function)
      push_deprecated_warn(
          thd, "VALUES function",
          "an alias (INSERT INTO ... VALUES (...) AS alias) and replace "
          "VALUES(col) in the ON DUPLICATE KEY UPDATE clause with alias.col");
  } else {
    // VALUES() is used out-of-scope - its value is always NULL
    ……
  }
  return false;
}
```

```cpp
void Item_insert_value::bind_fields() {
  if (arg == nullptr) return;
  if (!fixed) return;

  assert(m_table_ref->table->insert_values);

  // Bind field to the current TABLE object
  field->table = m_table_ref->table;

  field->move_field_offset(
      (ptrdiff_t)(field->table->insert_values - m_rowbuffer_saved));
  m_rowbuffer_saved = field->table->insert_values;

  Item_field *field_arg = down_cast<Item_field *>(arg->real_item());
  if ((field->type() == MYSQL_TYPE_BLOB || field->type() == MYSQL_TYPE_VECTOR ||
       field->type() == MYSQL_TYPE_GEOMETRY)) {
    current_thd->lex->insert_values_map(field_arg, field);
  }

  set_result_field(field);
}
```

```cpp
uint32 Item_aggregate_type::display_length(Item *item) {
  if (item->type() == Item::FIELD_ITEM)
    return ((Item_field *)item)->max_disp_length();

  switch (item->data_type()) {
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_VAR_STRING:
    case MYSQL_TYPE_STRING:
    case MYSQL_TYPE_GEOMETRY:
    case MYSQL_TYPE_JSON:
      return item->max_length;
    ……
  }
}
```

# 日志事件打印
sql/log_event.cc
```cpp
static size_t log_event_print_value(IO_CACHE *file, const uchar *ptr, uint type,
                                    uint meta, char *typestr,
                                    size_t typestr_length, char *col_name,
                                    bool is_partial,
                                    unsigned int vector_dimensionality) {
  uint32 length = 0;

  ……

  switch (type) {
    ……

    case MYSQL_TYPE_VECTOR: {
      snprintf(typestr, typestr_length, "VECTOR(%u)", vector_dimensionality);
      if (ptr == nullptr) {
        return my_b_printf(file, "NULL");
      }
      length = uint4korr(ptr);
      ptr += 4;
      uint dims = get_dimensions(length, sizeof(float));
      my_b_printf(file, "[");
      const uint tmp_length = 40;
      char tmp[tmp_length];
      for (uint i = 0; i < dims; i++) {
        char delimiter = (i == dims - 1) ? ']' : ',';
        snprintf(tmp, tmp_length, "%.5e", float4get(ptr + i * sizeof(float)));
        my_b_printf(file, "%s%c", tmp, delimiter);
      }
      return length + 4;
    }

    ……
  }
  ……
}
```
```cpp
size_t Rows_log_event::print_verbose_one_row(
    IO_CACHE *file, table_def *td, PRINT_EVENT_INFO *print_event_info,
    MY_BITMAP *cols_bitmap, const uchar *value, const uchar *prefix,
    enum_row_image_type row_image_type) {
  ……

  auto vector_dimensionality_it = td->get_vector_dimensionality_begin();

  for (size_t i = 0; i < td->size(); i++) {
    ……

    unsigned int vector_dimensionality = 0;
    if (td->type(i) == MYSQL_TYPE_VECTOR &&
        vector_dimensionality_it != td->get_vector_dimensionality_end()) {
      vector_dimensionality = *vector_dimensionality_it++;
    }

    char col_name[256];
    sprintf(col_name, "@%lu", (unsigned long)i + 1);
    const size_t size = log_event_print_value(
        file, is_null ? nullptr : value, td->type(i), td->field_metadata(i),
        typestr, sizeof(typestr), col_name, is_partial, vector_dimensionality);
    ……
  }
  return value - value0;
}
```

```cpp
static inline bool is_character_type(uint type) {
  switch (type) {
    case MYSQL_TYPE_STRING:
    case MYSQL_TYPE_VAR_STRING:
    case MYSQL_TYPE_VARCHAR:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_BLOB:
      return true;
    default:
      return false;
  }
}
```

```cpp
bool Table_map_log_event::init_vector_dimensionality_field() {
  StringBuffer<256> buf;
  for (auto *field : *m_column_view) {
    if (field->real_type() == MYSQL_TYPE_VECTOR) {
      store_compressed_length(
          buf, down_cast<Field_vector *>(field)->get_max_dimensions());
    }
  }

  if (buf.length() > 0)
    return write_tlv_field(m_metadata_buf, VECTOR_DIMENSIONALITY, buf);
  return false;
}
```

```cpp
static void get_type_name(uint type, unsigned char **meta_ptr,
                          const CHARSET_INFO *cs, char *typestr,
                          uint typestr_length, unsigned int geometry_type,
                          unsigned int vector_dimensionality) {
  switch (type) {
    ……
    case MYSQL_TYPE_VECTOR: {
      snprintf(typestr, typestr_length, "VECTOR(%u)", vector_dimensionality);
      (*meta_ptr)++;
      break;
    }
    ……
  }
}
```

```cpp
void Table_map_log_event::print_columns(
    IO_CACHE *file, const Optional_metadata_fields &fields) const {
  ……
  auto vector_dimensionality_it = fields.m_vector_dimensionality.begin();

  ……

    unsigned int vector_dimensionality = 0;
    if (real_type == MYSQL_TYPE_VECTOR &&
        vector_dimensionality_it != fields.m_vector_dimensionality.end()) {
      vector_dimensionality = *vector_dimensionality_it++;
    }

    ……
  }
  ……
}
```

# 数据包
sql/pack_rows.cc
```cpp
static size_t CalculateColumnStorageSize(const Column &column) {
  bool is_blob_column = false;
  switch (column.field_type) {
    ……
    case MYSQL_TYPE_JSON:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_TINY_BLOB:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_BLOB: {
      is_blob_column = true;
      break;
    }
    ……
  }

  ……

  return column.field->max_data_length();
}
```
# 解析树数据类型的支持
sql/parse_tree_column_attrs.h
```cpp
class PT_vector_type : public PT_type {
  char vector_length_buffer[33]{};

 public:
  PT_vector_type(const POS &pos, const char *length)
      : PT_type(pos, MYSQL_TYPE_VECTOR) {
    const char *length_arg = length == nullptr ? "2048" : length;
    uint vector_length = atoi(length_arg) * sizeof(float);
    sprintf(vector_length_buffer, "%u", vector_length);
  }

  const char *get_length() const override { return vector_length_buffer; }
  const CHARSET_INFO *get_charset() const override { return &my_charset_bin; }
};
```

# 协议
sql/protocol_classic.cc
```cpp
bool Protocol_classic::store_string(const char *from, size_t length,
                                    const CHARSET_INFO *fromcs) {
  // field_types check is needed because of the embedded protocol
  assert(send_metadata || field_types == nullptr ||
         field_types[field_pos] == MYSQL_TYPE_DECIMAL ||
         field_types[field_pos] == MYSQL_TYPE_BIT ||
         field_types[field_pos] == MYSQL_TYPE_NEWDECIMAL ||
         field_types[field_pos] == MYSQL_TYPE_NEWDATE ||
         field_types[field_pos] == MYSQL_TYPE_JSON ||
         field_types[field_pos] == MYSQL_TYPE_VECTOR ||
         (field_types[field_pos] >= MYSQL_TYPE_ENUM &&
          field_types[field_pos] <= MYSQL_TYPE_GEOMETRY));
  field_pos++;
  // result_cs is nullptr when client issues SET character_set_results=NULL
  if (result_cs != nullptr && !my_charset_same(fromcs, result_cs) &&
      fromcs != &my_charset_bin && result_cs != &my_charset_bin) {
    // Store with conversion.
    return net_store_data_with_conversion(pointer_cast<const uchar *>(from),
                                          length, fromcs, result_cs);
  }
  // Store without conversion.
  return net_store_data(pointer_cast<const uchar *>(from), length, packet);
}
```

# 主从复制
sql/rpl_utility.h
```cpp
class table_def {
  ……
  static uint vector_column_count(const unsigned char *types, ulong size) {
    uint count = 0;
    for (ulong i = 0; i < size; i++) {
      if (static_cast<enum_field_types>(types[i]) == MYSQL_TYPE_VECTOR) {
        count++;
      }
    }
    return count;
  }
  ……
  std::vector<unsigned int>::const_iterator get_vector_dimensionality_begin()
      const {
    return m_vector_dimensionality.begin();
  }

  std::vector<unsigned int>::const_iterator get_vector_dimensionality_end()
      const {
    return m_vector_dimensionality.end();
  }

  ……
  std::vector<unsigned int> m_vector_dimensionality;
```

sql/rpl_utility.cc
```cpp
static bool can_convert_field_to(Field *field, enum_field_types source_type,
                                 uint metadata, bool is_array,
                                 Relay_log_info *rli, uint16 mflags,
                                 unsigned int vector_dimensionality,
                                 int *order_var) {
  ……
  if (field->real_type() == source_type) {
    ……

    if (field->real_type() == MYSQL_TYPE_VECTOR &&
        down_cast<Field_vector *>(field)->get_max_dimensions() !=
            vector_dimensionality) {
      return false;
    }
    ……
  } else if (is_array) {
    // Can't convert between typed array of different types
    return false;
  } else if (metadata == 0 &&
             (timestamp_cross_check(field->real_type(), source_type) ||
              datetime_cross_check(field->real_type(), source_type) ||
              time_cross_check(field->real_type(), source_type))) {
    ……
  } else if (!replica_type_conversions_options)
    return false;

  /*
    Here, from and to will always be different. Since the types are
    different, we cannot use the compatible_field_size() function, but
    have to rely on hard-coded max-sizes for fields.
  */

  DBUG_PRINT("debug", ("Base types are different, checking conversion"));
  switch (source_type)  // Source type (on master)
  {
    ……

    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_GEOMETRY:
    case MYSQL_TYPE_JSON:
    ……
      return false;
  }
  return false;  // To keep GCC happy
}
```

```cpp
bool table_def::compatible_with(THD *thd, Relay_log_info *rli, TABLE *table,
                                TABLE **conv_table_var) {
  ……

  auto vector_dimensionality_it = m_vector_dimensionality.begin();

  for (auto it = fields->begin(); it.filtered_pos() < cols_to_check; ++it) {
    ……

    unsigned int vector_dimensionality = 0;
    if (type(col) == MYSQL_TYPE_VECTOR &&
        vector_dimensionality_it != m_vector_dimensionality.end()) {
      vector_dimensionality = *vector_dimensionality_it++;
    }

    if (can_convert_field_to(field, type(col), field_metadata(col),
                             is_array(col), rli, m_flags, vector_dimensionality,
                             &order)) {
      ……
    } else {
      ……
}
```

```cpp
std::pair<my_off_t, std::pair<uint, bool>> read_field_metadata(
    const uchar *buffer, enum_field_types binlog_type) {
  ……
  switch (binlog_type) {
    case MYSQL_TYPE_TINY_BLOB:
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_DOUBLE:
    case MYSQL_TYPE_FLOAT:
    case MYSQL_TYPE_GEOMETRY:
    case MYSQL_TYPE_TIME2:
    case MYSQL_TYPE_DATETIME2:
    case MYSQL_TYPE_TIMESTAMP2:
    case MYSQL_TYPE_JSON: {
      /*
        These types store a single byte.
      */
      metadata = buffer[index++];
      break;
    }
    ……
  }
  return std::make_pair(index, std::make_pair(metadata, is_array));
}
```

```cpp
uint Hash_slave_rows::make_hash_key(TABLE *table, MY_BITMAP *cols) {
  ……

  ……

  for (Field **ptr = table->field;
       *ptr && ((*ptr)->field_index() < cols->n_bits); ptr++) {
    ……
    if (bitmap_is_set(cols, f->field_index()) &&
        ……
      switch (f->type()) {
        case MYSQL_TYPE_BLOB:
        case MYSQL_TYPE_VECTOR:
        case MYSQL_TYPE_VARCHAR:
        case MYSQL_TYPE_GEOMETRY:
        case MYSQL_TYPE_JSON:
        case MYSQL_TYPE_BIT: {
          String tmp;
          f->val_str(&tmp);
          crc = checksum_crc32(crc, pointer_cast<const uchar *>(tmp.ptr()),
                               tmp.length());
          break;
        }
        ……
      }
……
    }
  }

  ……
}
```

# 插入
sql/sql_insert.cc
```cpp
static bool mysql_prepare_blob_values(THD *thd,
                                      const mem_root_deque<Item *> &fields,
                                      MEM_ROOT *mem_root) {
  ……
  for (Item *fld : fields) {
    Item_field *field = fld->field_for_view_update();
    Field *lhs_field = field->field;

    if (lhs_field->type() == MYSQL_TYPE_BLOB ||
        lhs_field->type() == MYSQL_TYPE_VECTOR ||
        lhs_field->type() == MYSQL_TYPE_GEOMETRY)
      blob_update_field_set.insert_unique(down_cast<Field_blob *>(lhs_field));
  }

  ……
}
```

# 优化器
sql/sql_optimizer.cc
```cpp
bool uses_index_fields_only(Item *item, TABLE *tbl, uint keyno,
                            bool other_tbls_ok) {
  ……

  switch (item_type) {
    ……
    case Item::FIELD_ITEM: {
      const Item_field *item_field = down_cast<const Item_field *>(item);
      if (item_field->field->table != tbl) return other_tbls_ok;
      /*
        The below is probably a repetition - the first part checks the
        other two, but let's play it safe:
      */
      return item_field->field->part_of_key.is_set(keyno) &&
             item_field->field->type() != MYSQL_TYPE_GEOMETRY &&
             item_field->field->type() != MYSQL_TYPE_VECTOR &&
             item_field->field->type() != MYSQL_TYPE_BLOB;
    }
    ……
  }
}
```

```cpp
static uint32 get_key_length_tmp_table(Item *item) {
  ……
  const enum_field_types type = item->data_type();
  if (type == MYSQL_TYPE_BLOB || type == MYSQL_TYPE_VECTOR ||
      type == MYSQL_TYPE_VARCHAR || type == MYSQL_TYPE_GEOMETRY)
    len += HA_KEY_BLOB_LENGTH;

  return len;
}
```

# 分区表
sql/sql_partition.cc
```cpp
static bool set_up_field_array(TABLE *table, bool is_sub_part) {
  ……
  while ((field = *(ptr++))) {
    if (field->is_flag_set(GET_FIXED_FIELDS_FLAG)) {
      field->clear_flag(GET_FIXED_FIELDS_FLAG);
      field->set_flag(FIELD_IN_PART_FUNC_FLAG);
      if (likely(!result)) {
        ……

        if (field->real_type() == MYSQL_TYPE_VECTOR) {
          /* vector column as partition key is not supported */
          my_error(ER_FIELD_TYPE_NOT_ALLOWED_AS_PARTITION_FIELD, MYF(0),
                   field->field_name);
          result = true;
        }

        ……
      }
    }
  }
  ……
}
```

```cpp
static int check_part_field(enum_field_types sql_type, const char *field_name,
                            Item_result *result_type, bool *need_cs_check) {
  ……
  if (sql_type == MYSQL_TYPE_VECTOR) {
    /* vector column as partition key is not supported */
    /* LCOV_EXCL_START */
    my_error(ER_FIELD_TYPE_NOT_ALLOWED_AS_PARTITION_FIELD, MYF(0), field_name);
    return true;
    /* LCOV_EXCL_STOP */
  }
  ……
……
}
```

# sql_prepare
sql/sql_prepare.cc
```cpp
static void set_parameter_type(Item_param *param, enum enum_field_types type,
                               bool unsigned_type,
                               const CHARSET_INFO *cs_source) {
  param->set_data_type_source(type, unsigned_type);

  switch (param->data_type_source()) {
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR: {
      param->set_collation_source(&my_charset_bin);
      break;
    }
    ……
  }
}
```
```cpp
static bool set_parameter_value(
    Item_param *param, const uchar **pos, ulong len,
    enum Prepared_statement::enum_param_pack_type pack_type) {
  switch (param->data_type_source()) {
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR: {
      param->set_str((const char *)*pos, len);

      break;
    }
    ……
  }
  return false;
}
```

```cpp
bool Prepared_statement::check_parameter_types() {
  ……

  for (Item_param **it = m_param_array; it < end; ++it) {
    ……

    switch (item->data_type()) {
      ……
      case MYSQL_TYPE_BLOB:
      case MYSQL_TYPE_VECTOR:
      case MYSQL_TYPE_LONG_BLOB:
        if (item->data_type_actual() == MYSQL_TYPE_LONGLONG ||
            item->data_type_actual() == MYSQL_TYPE_NEWDECIMAL ||
            item->data_type_actual() == MYSQL_TYPE_DOUBLE ||
            item->data_type_actual() == MYSQL_TYPE_DATETIME ||
            item->data_type_actual() == MYSQL_TYPE_TIMESTAMP ||
            item->data_type_actual() == MYSQL_TYPE_DATE ||
            item->data_type_actual() == MYSQL_TYPE_TIME)
          return false;
        break;
      ……
    }
  }

  return true;
}
```

# show 
sql/sql_show.cc
```cpp
static TABLE *create_schema_table(THD *thd, Table_ref *table_list) {
  ……

  for (; fields_info->field_name; fields_info++) {
    switch (fields_info->field_type) {
      ……
      case MYSQL_TYPE_BLOB:
      case MYSQL_TYPE_VECTOR:
        if (!(item = new Item_blob(fields_info->field_name,
                                   fields_info->field_length))) {
          return nullptr;
        }
        break;
      ……
    }
    ……
  }
  ……
}
```

```cpp
void show_sql_type(enum_field_types type, bool is_array, uint metadata,
                   String *str, const CHARSET_INFO *field_cs,
                   unsigned int vector_dimensionality) {
  DBUG_TRACE;
  DBUG_PRINT("enter", ("type: %d, metadata: 0x%x", type, metadata));

  switch (type) {
    ……

    case MYSQL_TYPE_VECTOR: {
      const CHARSET_INFO *cs = str->charset();
      size_t length = cs->cset->snprintf(cs, str->ptr(), str->alloced_length(),
                                         "vector(%u)", vector_dimensionality);
      str->length(length);
      break;
    }

    ……
  }
  if (is_array) str->append(STRING_WITH_LEN(" array"));
}
```

# 建表
sql/sql_table.cc
```cpp
bool prepare_pack_create_field(THD *thd, Create_field *sql_field,
                               longlong table_flags) {
  ……

  switch (sql_field->sql_type) {
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_TINY_BLOB:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_JSON:
      assert(sql_field->auto_flags == Field::NONE ||
             sql_field->auto_flags == Field::GENERATED_FROM_EXPRESSION);
      break;
    ……
  }

  ……
}
```

```cpp
static bool prepare_key_column(THD *thd, HA_CREATE_INFO *create_info,
                               List<Create_field> *create_list,
                               const Key_spec *key, const Key_part_spec *column,
                               const size_t column_nr, KEY *key_info,
                               KEY_PART_INFO *key_part_info,
                               const handler *file, int *auto_increment,
                               const CHARSET_INFO **ft_key_charset) {
  ……

  // VECTOR columns cannot be used as keys
  if (sql_field->sql_type == MYSQL_TYPE_VECTOR) {
    my_error(ER_NON_SCALAR_USED_AS_KEY, MYF(0), column->get_field_name());
    return true;
  }

  ……

}
```

```cpp
bool Item_field::replace_field_processor(uchar *arg) {
  ……

  if (create_field) {
    field = new (targ->thd()->mem_root) Create_field_wrapper(create_field);
    switch (create_field->sql_type) {
      case MYSQL_TYPE_VECTOR:
        my_error(ER_INCORRECT_TYPE, MYF(0), create_field->field_name,
                 "GENERATED COLUMN");
        return true;
      ……
    }

    fixed = true;
  } else {
    ……
  }

  ……
}
```

```cpp
bool mysql_prepare_create_table(
    THD *thd, const char *error_schema_name, const char *error_table_name,
    HA_CREATE_INFO *create_info, Alter_info *alter_info, handler *file,
    bool is_partitioned, KEY **key_info_buffer, uint *key_count,
    FOREIGN_KEY **fk_key_info_buffer, uint *fk_key_count,
    FOREIGN_KEY *existing_fks, uint existing_fks_count,
    const dd::Table *existing_fks_table, uint fk_max_generated_name_number,
    int select_field_count, bool find_parent_keys) {
  ……
  while ((sql_field = it++)) {
    if (sql_field->auto_flags & Field::NEXT_NUMBER) auto_increment++;
    switch (sql_field->sql_type) {
      case MYSQL_TYPE_GEOMETRY:
      case MYSQL_TYPE_BLOB:
      case MYSQL_TYPE_VECTOR:
      case MYSQL_TYPE_MEDIUM_BLOB:
      case MYSQL_TYPE_TINY_BLOB:
      case MYSQL_TYPE_LONG_BLOB:
      case MYSQL_TYPE_JSON:
        blob_columns++;
        break;
      default:
        if (sql_field->is_array) blob_columns++;
        break;
    }
  }
  ……
}
```

```cpp
bool mysql_checksum_table(THD *thd, Table_ref *tables,
                          HA_CHECK_OPT *check_opt) {
  ……

  /* Open one table after the other to keep lock time as short as possible. */
  for (table = tables; table; table = table->next_local) {
    ……

    if (!t) {
      /* Table didn't exist */
      protocol->store_null();
    } else {
      if (t->file->ha_table_flags() & HA_HAS_CHECKSUM &&
          !(check_opt->flags & T_EXTEND))
        protocol->store((ulonglong)t->file->checksum());
      else if (!(t->file->ha_table_flags() & HA_HAS_CHECKSUM) &&
               (check_opt->flags & T_QUICK))
        protocol->store_null();
      else {
        ……

        if (t->file->ha_rnd_init(true))
          protocol->store_null();
        else {
          for (;;) {
            ……

            for (uint i = 0; i < t->s->fields; i++) {
              Field *f = t->field[i];

              /*
                BLOB and VARCHAR have pointers in their field, we must convert
                to string; GEOMETRY and JSON are implemented on top of BLOB.
                BIT may store its data among NULL bits, convert as well.
              */
              switch (f->type()) {
                case MYSQL_TYPE_BLOB:
                case MYSQL_TYPE_VECTOR:
                case MYSQL_TYPE_VARCHAR:
                case MYSQL_TYPE_GEOMETRY:
                case MYSQL_TYPE_JSON:
                case MYSQL_TYPE_BIT: {
                  String tmp;
                  f->val_str(&tmp);
                  row_crc =
                      checksum_crc32(row_crc, (uchar *)tmp.ptr(), tmp.length());
                  break;
                }
                ……
              }
            }

            crc += row_crc;
          }
          ……
        }
      }
      trans_rollback_stmt(thd);
      close_thread_tables(thd);
    }

    ……
  }

  ……
}
```
# 字典表
sql/dd/dd_table.cc
```cpp
dd::enum_column_types get_new_field_type(enum_field_types type) {
  switch (type) {
    ……

    case MYSQL_TYPE_VECTOR:
      return dd::enum_column_types::VECTOR;

    ……
  }

  ……
}
```

# 字典、视图
sql/dd/impl/system_views/columns.cc

sql/dd/impl/system_views/parameters.cc

sql/dd/impl/system_views/routines.cc

sql/dd/impl/tables/columns.cc

sql/dd/impl/tables/parameters.cc

sql/dd/impl/tables/routines.cc

sql/histograms/histogram.cc

# 分区
sql/partitioning/partition_handler.cc
```cpp
uint32 Partition_helper::ph_calculate_key_hash_value(Field **field_array) {
  ……

  do {
    Field *field = *field_array;
    if (use_51_hash) {
      switch (field->real_type()) {
        ……
        case MYSQL_TYPE_BLOB:
        case MYSQL_TYPE_VECTOR:
        case MYSQL_TYPE_VAR_STRING:
        case MYSQL_TYPE_GEOMETRY:
        case MYSQL_TYPE_INVALID:
          /* fall through. */
        default:
          assert(0);  // New type?
                      /* Fall through for default hashing (5.5). */
      }
      /* fall through, use collation based hashing. */
    }
    field->hash(&nr1, &nr2);
  } while (*(++field_array));
  return (uint32)nr1;
}
```

# 查询组件接口
sql/server_component/mysql_query_attributes_imp.cc
```cpp
/** keep in sync with setup_one_conversion_function() */
static String *query_parameter_val_str(const PS_PARAM *param,
                                       const CHARSET_INFO *cs) {
  String *str = nullptr;
  switch (param->type) {
    // the expected data types listed in the manual
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR: {
      str = new String[1];
      uint dummy_errors;
      if (str->copy(reinterpret_cast<const char *>(param->value), param->length,
                    &my_charset_bin, &my_charset_bin, &dummy_errors)) {
        delete[] str;
        str = nullptr;
      }
      break;
    }
    ……
  }
  return str;
}
```

# 存储过程接口
```cpp
/*
 * Argument-related services:
 */

/**
  Get stored program argument metadata

  "argument_name" -> const char *
  "sql_type"      -> uint64_t
  "in_variable"   -> boolean
  "out_variable"  -> boolean
  "is_signed"     -> boolean (Applicable to numeric data types)
  "is_nullable"   -> boolean
  "byte_length"   -> uint64_t
  "char_length"   -> uint64_t (Applicable to string data types)
  "charset"       -> char const *
  @note Have the key at least 7 characters long, with unique first 8 characters.

  @returns status of get operation
  @retval MYSQL_SUCCESS Success
  @retval MYSQL_FAILURE Failure
*/
static int get_field_metadata_internal(Create_field &field, bool input,
                                       bool output, const char *key,
                                       void *value) {
  if (strcmp("argument_name", key) == 0)
    ……
  else if (strcmp("sql_type", key) == 0)
    switch (field.sql_type) {
      ……
      case MYSQL_TYPE_BLOB:
        *reinterpret_cast<uint64_t *>(value) = MYSQL_SP_ARG_TYPE_BLOB;
        break;
      case MYSQL_TYPE_VAR_STRING:
        *reinterpret_cast<uint64_t *>(value) = MYSQL_SP_ARG_TYPE_VAR_STRING;
        break;
      case MYSQL_TYPE_STRING:
        *reinterpret_cast<uint64_t *>(value) = MYSQL_SP_ARG_TYPE_STRING;
        break;
      case MYSQL_TYPE_GEOMETRY:
        *reinterpret_cast<uint64_t *>(value) = MYSQL_SP_ARG_TYPE_GEOMETRY;
        break;
      case MYSQL_TYPE_VECTOR:
        *reinterpret_cast<uint64_t *>(value) = MYSQL_SP_ARG_TYPE_VECTOR;
        break;
      default:
        return MYSQL_FAILURE;
    }
  ……
}
```

# bind 
sql-common/bind_params.cc
```cpp
bool fix_param_bind(MYSQL_BIND *param, uint idx) {
  param->long_data_used = false;
  param->param_number = idx;

  /* If param->is_null is not set, then the value can never be NULL */
  if (!param->is_null) param->is_null = &int_is_null_false;

  /* Setup data copy functions for the different supported types */
  switch (param->buffer_type) {
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_VARCHAR:
    case MYSQL_TYPE_VAR_STRING:
    case MYSQL_TYPE_STRING:
    case MYSQL_TYPE_DECIMAL:
    case MYSQL_TYPE_NEWDECIMAL:
    case MYSQL_TYPE_JSON:
      param->store_param_func = store_param_str;
      /*
        For variable length types user must set either length or
        buffer_length.
      */
      break;
    default:
      return true;
  }
  ……
}
```

# 客户端 SQL
sql-common/client.cc
```cpp
const char *fieldtype2str(enum enum_field_types type) {
  switch (type) {
    ……
    case MYSQL_TYPE_VECTOR:
      return "VECTOR";
    case MYSQL_TYPE_BOOL:
      return "BOOLEAN";
    ……
    default:
      return "?-unknown-?";
  }
}
```

# 存储引擎层
## 全文检索接口
storage/innobase/fts/fts0fts.cc
```cpp
static inline CHARSET_INFO *fts_get_charset(ulint prtype) {
#ifdef UNIV_DEBUG
  switch (prtype & DATA_MYSQL_TYPE_MASK) {
    case MYSQL_TYPE_BIT:
    case MYSQL_TYPE_STRING:
    case MYSQL_TYPE_VAR_STRING:
    case MYSQL_TYPE_TINY_BLOB:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_VARCHAR:
      break;
    default:
      ut_error;
  }
#endif /* UNIV_DEBUG */

  uint cs_num = (uint)dtype_get_charset_coll(prtype);

  if (CHARSET_INFO *cs = get_charset(cs_num, MYF(MY_WME))) {
    return (cs);
  }

  ib::fatal(UT_LOCATION_HERE, ER_IB_MSG_461)
      << "Unable to find charset-collation " << cs_num;
  return (nullptr);
}
```

## 数据结构、函数和宏
storage/innobase/handler/ha_innodb.cc
```cpp
/** Converts a MySQL type to an InnoDB type. Note that this function returns
the 'mtype' of InnoDB. InnoDB differentiates between MySQL's old <= 4.1
VARCHAR and the new true VARCHAR in >= 5.0.3 by the 'prtype'.
@param[out]     unsigned_flag   DATA_UNSIGNED if an 'unsigned type'; at least
ENUM and SET, and unsigned integer types are 'unsigned types'
@param[in]      f               MySQL Field
@return DATA_BINARY, DATA_VARCHAR, ... */
ulint get_innobase_type_from_mysql_type(ulint *unsigned_flag, const void *f) {
  const class Field *field = reinterpret_cast<const class Field *>(f);

  ……

  switch (field->type()) {
      /* NOTE that we only allow string types in DATA_MYSQL and
      DATA_VARMYSQL */
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_JSON:  // JSON fields are stored as BLOBs
      return (DATA_BLOB);
    case MYSQL_TYPE_NULL:
      /* MySQL currently accepts "NULL" datatype, but will
      reject such datatype in the next release. We will cope
      with it and not trigger assertion failure in 5.1 */
      break;
    default:
      ut_error;
  }

  return (0);
}
```

## 记录比较
storage/innobase/include/rem0cmp.ic
```cpp
#ifndef UNIV_HOTBACKUP
/** Compare two data fields.
@param[in] dfield1 data field
@param[in] dfield2 data field
@return the comparison result of dfield1 and dfield2
@retval true if dfield1 is equal to dfield2, or a prefix of dfield1
@retval false otherwise */
static inline bool cmp_dfield_dfield_eq_prefix(const dfield_t *dfield1,
                                               const dfield_t *dfield2) {
  const dtype_t *type;

  ut_ad(dfield_check_typed(dfield1));
  ut_ad(dfield_check_typed(dfield2));

  type = dfield_get_type(dfield1);

#ifdef UNIV_DEBUG
  switch (type->prtype & DATA_MYSQL_TYPE_MASK) {
    case MYSQL_TYPE_BIT:
    case MYSQL_TYPE_STRING:
    case MYSQL_TYPE_VAR_STRING:
    case MYSQL_TYPE_TINY_BLOB:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_VARCHAR:
      break;
    default:
      ut_error;
  }
#endif /* UNIV_DEBUG */

  uint cs_num = (uint)dtype_get_charset_coll(type->prtype);

  if (CHARSET_INFO *cs = get_charset(cs_num, MYF(MY_WME))) {
    return (!cs->coll->strnncoll(
        cs, static_cast<uchar *>(dfield_get_data(dfield1)),
        dfield_get_len(dfield1), static_cast<uchar *>(dfield_get_data(dfield2)),
        dfield_get_len(dfield2), true));
  }

#ifdef UNIV_NO_ERR_MSGS
  ib::fatal(UT_LOCATION_HERE)
#else
  ib::fatal(UT_LOCATION_HERE, ER_IB_MSG_627)
#endif /* !UNIV_NO_ERR_MSGS */
      << "Unable to find charset-collation " << cs_num;

  return (false);
}
#endif /* UNIV_HOTBACKUP */
```

storage/innobase/rem/rem0cmp.cc
```cpp
static inline int innobase_mysql_cmp(ulint prtype, const byte *a,
                                     size_t a_length, const byte *b,
                                     size_t b_length) {
#ifdef UNIV_DEBUG
  switch (prtype & DATA_MYSQL_TYPE_MASK) {
    case MYSQL_TYPE_BIT:
    case MYSQL_TYPE_STRING:
    case MYSQL_TYPE_VAR_STRING:
    case MYSQL_TYPE_TINY_BLOB:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_VARCHAR:
      break;
    default:
      ut_error;
  }
#endif /* UNIV_DEBUG */

  ……
}
````
## myisam
storage/myisam/ha_myisam.cc
```cpp
int table2myisam(TABLE *table_arg, MI_KEYDEF **keydef_out,
                 MI_COLUMNDEF **recinfo_out, uint *records_out) {
  ……
    for (j = 0; j < pos->user_defined_key_parts; j++) {
      ……
      if (field->type() == MYSQL_TYPE_BLOB ||
          field->type() == MYSQL_TYPE_VECTOR ||
          field->type() == MYSQL_TYPE_GEOMETRY) {
        keydef[i].seg[j].flag |= HA_BLOB_PART;
        /* save number of bytes used to pack length */
        keydef[i].seg[j].bit_start =
            (uint)(field->pack_length() - portable_sizeof_char_ptr);
      } else if (field->type() == MYSQL_TYPE_BIT) {
        ……
      }
    }
    keyseg += pos->user_defined_key_parts;
  }
  ……
}
```

## handler
storage/temptable/include/temptable/handler.h
```cpp
inline bool Handler::is_field_type_fixed_size(const Field &mysql_field) const {
  switch (mysql_field.type()) {
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_GEOMETRY:
    case MYSQL_TYPE_JSON:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_TINY_BLOB:
    case MYSQL_TYPE_VARCHAR:
      return false;
    default:
      return true;
  }
}
```

## NDB
storage/ndb/plugin/ha_ndbcluster_cond.cc
```cpp
在所有 MYSQL_TYPE_BLOB 的地方，类似地加上 MYSQL_TYPE_VECTOR
```


# MySQL 字段类型新增向量字段类型
对 include/field_types.h 进行调整
```cpp
……
enum enum_field_types {
  ……
  MYSQL_TYPE_VECTOR = 242,
  ……
……
```

# 添加向量字段类型对应的类
在 `sql/field.h` 中添加
```cpp
……
#include "sql/vector_conversion.h"  // get_dimensions
……
/*

Field class hierarchy


Field (abstract)
|
+--Field_bit
|  +--Field_bit_as_char
|
+--Field_num (abstract)
|  |  +--Field_real (abstract)
|  |     +--Field_decimal
|  |     +--Field_float
|  |     +--Field_double
|  |
|  +--Field_new_decimal
|  +--Field_short
|  +--Field_medium
|  +--Field_long
|  +--Field_longlong
|  +--Field_tiny
|     +--Field_year
|
+--Field_str (abstract)
|  +--Field_longstr
|  |  +--Field_string
|  |  +--Field_varstring
|  |  +--Field_blob
|  |     +--Field_geom
|  |     +--Field_json
|  |        +--Field_typed_array
|  |     +--Field_vector
|  |
|  +--Field_null
|  +--Field_enum
|     +--Field_set
|
+--Field_temporal (abstract)
   +--Field_time_common (abstract)
   |  +--Field_time
   |  +--Field_timef
   |
   +--Field_temporal_with_date (abstract)
      +--Field_newdate
      +--Field_temporal_with_date_and_time (abstract)
         +--Field_timestamp
         +--Field_datetime
         +--Field_temporal_with_date_and_timef (abstract)
            +--Field_timestampf
            +--Field_datetimef
*/
……
class Field_vector : public Field_blob {
 public:
  static const uint32 max_dimensions = 16383;
  static const uint32 precision = sizeof(float);
  static uint32 dimension_bytes(uint32 dimensions) {
    return precision * dimensions;
  }
  uint32 get_max_dimensions() const {
    return get_dimensions(field_length, precision);
  }

  Field_vector(uchar *ptr_arg, uint32 len_arg, uchar *null_ptr_arg,
               uchar null_bit_arg, uchar auto_flags_arg,
               const char *field_name_arg, TABLE_SHARE *share,
               uint blob_pack_length, const CHARSET_INFO *cs)
      : Field_blob(ptr_arg, null_ptr_arg, null_bit_arg, auto_flags_arg,
                   field_name_arg, share, blob_pack_length, cs) {
    set_field_length(len_arg);
    assert(packlength == 4);
  }

  Field_vector(uint32 len_arg, bool is_nullable_arg, const char *field_name_arg,
               const CHARSET_INFO *cs)
      : Field_blob(len_arg, is_nullable_arg, field_name_arg, cs, false) {
    set_field_length(len_arg);
    assert(packlength == 4);
  }

  Field_vector(const Field_vector &field) : Field_blob(field) {
    assert(packlength == 4);
  }

  void sql_type(String &res) const override {
    const CHARSET_INFO *cs = res.charset();
    size_t length =
        cs->cset->snprintf(cs, res.ptr(), res.alloced_length(), "%s(%u)",
                           "vector", get_max_dimensions());
    res.length(length);
  }
  Field_vector *clone(MEM_ROOT *mem_root) const override {
    assert(type() == MYSQL_TYPE_VECTOR);
    return new (mem_root) Field_vector(*this);
  }
  uint32 max_data_length() const override { return field_length; }
  uint32 char_length() const override { return field_length; }
  enum_field_types type() const final { return MYSQL_TYPE_VECTOR; }
  enum_field_types real_type() const final { return MYSQL_TYPE_VECTOR; }
  void make_send_field(Send_field *field) const override;
  using Field_blob::store;
  type_conversion_status store(double nr) final;
  type_conversion_status store(longlong nr, bool unsigned_val) final;
  type_conversion_status store_decimal(const my_decimal *) final;
  type_conversion_status store(const char *from, size_t length,
                               const CHARSET_INFO *cs) final;
  uint is_equal(const Create_field *new_field) const override;
  String *val_str(String *, String *) const override;
};
……
```

# 在系统表的数据字典中添加向量字段的支持
在 `sql/dd_table_share.cc` 中添加向量字段的支持
```cpp
enum_field_types dd_get_old_field_type(dd::enum_column_types type) {
  switch (type) {
    ……

    case dd::enum_column_types::VECTOR:
      return MYSQL_TYPE_VECTOR;

    ……

  return MYSQL_TYPE_LONG;
}
```

# 字段之间复制的函数
`sql/field_conv.cc` 中添加向量字段的支持
```cpp
Copy_field::Copy_func *Copy_field::get_copy_func() {
  THD *thd = current_thd;
  if (m_to_field->is_array() && m_from_field->is_array()) return do_copy_blob;

  const bool compatible_db_low_byte_first =
      (m_to_field->table->s->db_low_byte_first ==
       m_from_field->table->s->db_low_byte_first);
  if (m_to_field->type() == MYSQL_TYPE_GEOMETRY) {
    ……
  } else if (m_to_field->is_flag_set(BLOB_FLAG)) {
    /*
      We need to do conversion if we are copying from BLOB to
      non-BLOB, or if we are copying between BLOBs with different
      character sets, or if we are copying between JSON and non-JSON.
    */
    if (!m_from_field->is_flag_set(BLOB_FLAG) ||
        m_from_field->charset() != m_to_field->charset() ||
        ((m_to_field->type() == MYSQL_TYPE_JSON) !=
         (m_from_field->type() == MYSQL_TYPE_JSON)))
      return do_conv_blob;
    if (m_from_field->pack_length() != m_to_field->pack_length() ||
        !compatible_db_low_byte_first) {
      return do_copy_blob;
    }
    if (m_from_field->real_type() == MYSQL_TYPE_VECTOR ||
        m_to_field->real_type() == MYSQL_TYPE_VECTOR) {
      /* Use do_copy_blob if an involved field is VECTOR, since
       * we need to check for explicit field length */
      return do_copy_blob;
    }
  } else {
    ……
  }
  /* Eq fields */
  assert(m_to_field->pack_length() == m_from_field->pack_length());
  return do_field_eq;
}
```
继续调整
```cpp
bool fields_are_memcpyable(const Field *to, const Field *from) {
  assert(to != from);

  ……
  if (to_type == MYSQL_TYPE_JSON || to_real_type == MYSQL_TYPE_GEOMETRY ||
      to_real_type == MYSQL_TYPE_VARCHAR || to_real_type == MYSQL_TYPE_ENUM ||
      to_real_type == MYSQL_TYPE_SET || to_real_type == MYSQL_TYPE_BIT ||
      to_real_type == MYSQL_TYPE_VECTOR) {
    return false;
  }
  ……
}
```

# 在物理字段上的支持
sql/field.cc 
```cpp
size_t calc_pack_length(enum_field_types type, size_t length) {
  switch (type) {
    ……
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_GEOMETRY:
    case MYSQL_TYPE_JSON:
      return 4 + portable_sizeof_char_ptr;
    ……
  }
  assert(false);
  return 0;
}

……

Field *make_field(MEM_ROOT *mem_root, TABLE_SHARE *share, uchar *ptr,
                  size_t field_length, uchar *null_pos, uchar null_bit,
                  enum_field_types field_type,
                  const CHARSET_INFO *field_charset,
                  Field::geometry_type geom_type, uchar auto_flags,
                  TYPELIB *interval, const char *field_name, bool is_nullable,
                  bool is_zerofill, bool is_unsigned, uint decimals,
                  bool treat_bit_as_char, uint pack_length_override,
                  std::optional<gis::srid_t> srid, bool is_array) {
  ……
  /*
    FRMs from 3.23/4.0 can have strings with field_type == MYSQL_TYPE_DECIMAL.
    We should not be getting them after upgrade to new data-dictionary.
  */

  switch (field_type) {
    ……
    case MYSQL_TYPE_VECTOR: {
      const uint pack_length =
          calc_pack_length(field_type, field_length) - portable_sizeof_char_ptr;
      return new (mem_root)
          Field_vector(ptr, field_length, null_pos, null_bit, auto_flags,
                       field_name, share, pack_length, field_charset);
    }
    ……
  return nullptr;
}
```

# 备份工具对向量字段的支持
对 `client/mysqldump.cc` 进行调整
```cpp
static void dump_table(char *table, char *db) {
        ……
        is_blob =
            (field->charsetnr == 63 && (field->type == MYSQL_TYPE_BIT ||
                                        field->type == MYSQL_TYPE_STRING ||
                                        field->type == MYSQL_TYPE_VAR_STRING ||
                                        field->type == MYSQL_TYPE_VARCHAR ||
                                        field->type == MYSQL_TYPE_BLOB ||
                                        field->type == MYSQL_TYPE_VECTOR ||
                                        field->type == MYSQL_TYPE_LONG_BLOB ||
                                        field->type == MYSQL_TYPE_MEDIUM_BLOB ||
                                        field->type == MYSQL_TYPE_TINY_BLOB ||
                                        field->type == MYSQL_TYPE_GEOMETRY))
                ? 1
                : 0;
        ……
```
# 调整 binlog 的事件对向量的支持
`libs/mysql/binlog/event/binary_log_funcs.cpp` 中调整
```cpp
/**
   Compute the maximum display length of a field.

   @param sql_type Type of the field
   @param metadata The metadata from the master for the field.
   @return Maximum length of the field in bytes.
 */
unsigned int max_display_length_for_field(enum_field_types sql_type,
                                          unsigned int metadata) {
  BAPI_ASSERT(metadata >> 16 == 0);

  switch (sql_type) {
    ……
    case MYSQL_TYPE_VECTOR:
    ……
    case MYSQL_TYPE_JSON:
      return uint_max(4 * 8);

    default:
      return UINT_MAX;
  }
}
```
继续调整
```cpp
uint32_t calc_field_size(unsigned char col, const unsigned char *master_data,
                         unsigned int metadata) {
  uint32_t length = 0;

  switch ((col)) {
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_GEOMETRY:
    case MYSQL_TYPE_JSON: {
      /*
        Compute the length of the data. We cannot use get_length() here
        since it is dependent on the specific table (and also checks the
        packlength using the internal 'table' pointer) and replication
        is using a fixed format for storing data in the binlog.
      */
      switch (metadata) {
        case 1:
          length = *master_data;
          break;
        case 2:
          memcpy(&length, master_data, 2);
          length = le32toh(length);
          break;
        case 3:
          memcpy(&length, master_data, 3);
          length = le32toh(length);
          break;
        case 4:
          memcpy(&length, master_data, 4);
          length = le32toh(length);
          break;
        default:
          BAPI_ASSERT(0);  // Should not come here
          break;
      }

      length += metadata;
      break;
    }
    default:
      length = UINT_MAX;
  }
  ……
}
```
# pluginx 对向量的支持
`plugin/x/src/sql_data_result.cc` 调整
```cpp
void Sql_data_result::get_next_field(std::string *value) {
  validate_field_index({MYSQL_TYPE_VARCHAR, MYSQL_TYPE_STRING,
                        MYSQL_TYPE_MEDIUM_BLOB, MYSQL_TYPE_BLOB,
                        MYSQL_TYPE_VECTOR, MYSQL_TYPE_LONG_BLOB});

  Field_value *field_value = get_value();

  *value = "";
  if (field_value && field_value->is_string)
    *value = *field_value->value.v_string;
}
```
`plugin/x/src/streaming_command_delegate.cc` 调整
```cpp
int Streaming_command_delegate::field_metadata(struct st_send_field *field,
                                               const CHARSET_INFO *charset) {
  ……

  switch (type) {
    ……
    case MYSQL_TYPE_BLOB:
    case MYSQL_TYPE_VECTOR:
    case MYSQL_TYPE_MEDIUM_BLOB:
    case MYSQL_TYPE_LONG_BLOB:
    case MYSQL_TYPE_VARCHAR:
    case MYSQL_TYPE_VAR_STRING:
      column_info.set_length(field->length);
      column_info.set_type(Mysqlx::Resultset::ColumnMetaData::BYTES);
      column_info.set_collation(
          get_valid_charset_collation(m_resultcs, charset));
      break;

    ……
  }

  ……
}
```
# 向量转换函数
sql/vector_conversion.h

# 跟踪分析
## 简单跟踪 vector_dim
```
select id,vector_dim(c_v) from t_vector;
```

```cpp
Item_func_vector_dim::Item_func_vector_dim(Item_func_vector_dim * const this, const POS & pos, Item * a) (\data\ldc_docker\mysql-server_9.0.0\sql\item_func.h:1800)
(anonymous namespace)::Instantiator<Item_func_vector_dim, 1, 1>::instantiate((anonymous namespace)::Instantiator<Item_func_vector_dim, 1, 1> * const this, THD * thd, PT_item_list * args) (\data\ldc_docker\mysql-server_9.0.0\sql\item_create.cc:256)
(anonymous namespace)::Function_factory<(anonymous namespace)::Instantiator<Item_func_vector_dim, 1, 1> >::create_func((anonymous namespace)::Function_factory<(anonymous namespace)::Instantiator<Item_func_vector_dim, 1, 1> > * const this, THD * thd, LEX_STRING function_name, PT_item_list * item_list) (\data\ldc_docker\mysql-server_9.0.0\sql\item_create.cc:1042)
PTI_function_call_generic_ident_sys::do_itemize(PTI_function_call_generic_ident_sys * const this, Parse_context * pc, Item ** res) (\data\ldc_docker\mysql-server_9.0.0\sql\parse_tree_items.cc:261)
Item::itemize(Item * const this, Parse_context * pc, Item ** res) (\data\ldc_docker\mysql-server_9.0.0\sql\item.h:1252)
PTI_expr_with_alias::do_itemize(PTI_expr_with_alias * const this, Parse_context * pc, Item ** res) (\data\ldc_docker\mysql-server_9.0.0\sql\parse_tree_items.cc:351)
Item::itemize(Item * const this, Parse_context * pc, Item ** res) (\data\ldc_docker\mysql-server_9.0.0\sql\item.h:1252)
PT_item_list::do_contextualize(PT_item_list * const this, Parse_context * pc) (\data\ldc_docker\mysql-server_9.0.0\sql\parse_tree_helpers.h:118)
PT_select_item_list::do_contextualize(PT_select_item_list * const this, Parse_context * pc) (\data\ldc_docker\mysql-server_9.0.0\sql\parse_tree_nodes.cc:3839)
Parse_tree_node_tmpl<Parse_context>::contextualize(Parse_tree_node_tmpl<Parse_context> * const this, Parse_context * pc) (\data\ldc_docker\mysql-server_9.0.0\sql\parse_tree_node_base.h:323)
PT_query_specification::do_contextualize(PT_query_specification * const this, Parse_context * pc) (\data\ldc_docker\mysql-server_9.0.0\sql\parse_tree_nodes.cc:1238)
Parse_tree_node_tmpl<Parse_context>::contextualize(Parse_tree_node_tmpl<Parse_context> * const this, Parse_context * pc) (\data\ldc_docker\mysql-server_9.0.0\sql\parse_tree_node_base.h:323)
PT_query_expression::do_contextualize(PT_query_expression * const this, Parse_context * pc) (\data\ldc_docker\mysql-server_9.0.0\sql\parse_tree_nodes.cc:4288)
Parse_tree_node_tmpl<Parse_context>::contextualize(Parse_tree_node_tmpl<Parse_context> * const this, Parse_context * pc) (\data\ldc_docker\mysql-server_9.0.0\sql\parse_tree_node_base.h:323)
PT_select_stmt::make_cmd(PT_select_stmt * const this, THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\parse_tree_nodes.cc:766)
LEX::make_sql_cmd(LEX * const this, Parse_tree_root * parse_tree) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_lex.cc:5086)
THD::sql_parser(THD * const this) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_class.cc:3097)
parse_sql(THD * thd, Parser_state * parser_state, Object_creation_ctx * creation_ctx) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:7104)
dispatch_sql_command(THD * thd, Parser_state * parser_state, bool is_retry) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:5225)
dispatch_command(THD * thd, const COM_DATA * com_data, enum_server_command command) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:2122)
do_command(THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:1466)
handle_connection(void * arg) (\data\ldc_docker\mysql-server_9.0.0\sql\conn_handler\connection_handler_per_thread.cc:304)
pfs_spawn_thread(void * arg) (\data\ldc_docker\mysql-server_9.0.0\storage\perfschema\pfs.cc:3061)
libpthread.so.0!start_thread (Unknown Source:0)
libc.so.6!clone (Unknown Source:0)
``

## to_vector 分析
```sql
insert into t_vector values(7,to_vector('[1,2,3,4,0.5,6,7]'));
```
在函数 from_string_to_vector 断点

查看调用栈

先把字符串转 vector
```cpp
from_string_to_vector(const char * input, uint32_t input_len, char * const output, uint32_t * max_output_dims) (\data\ldc_docker\mysql-server_9.0.0\sql\vector_conversion.h:40)
Item_func_to_vector::val_str(Item_func_to_vector * const this, String * str) (\data\ldc_docker\mysql-server_9.0.0\sql\item_strfunc.cc:4166)
Item::save_in_field_inner(Item * const this, Field * field, bool no_conversions) (\data\ldc_docker\mysql-server_9.0.0\sql\item.cc:6952)
Item::save_in_field(Item * const this, Field * field, bool no_conversions) (\data\ldc_docker\mysql-server_9.0.0\sql\item.cc:6856)
fill_record(THD * thd, TABLE * table, const mem_root_deque<Item*> & fields, const mem_root_deque<Item*> & values, MY_BITMAP * bitmap, MY_BITMAP * insert_into_fields_bitmap, bool raise_autoinc_has_expl_non_null_val) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_base.cc:9750)
fill_record_n_invoke_before_triggers(THD * thd, COPY_INFO * optype_info, const mem_root_deque<Item*> & fields, const mem_root_deque<Item*> & values, TABLE * table, enum_trigger_event_type event, int num_fields, bool raise_autoinc_has_expl_non_null_val, bool * is_row_changed) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_base.cc:10077)
Sql_cmd_insert_values::execute_inner(Sql_cmd_insert_values * const this, THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_insert.cc:595)
Sql_cmd_dml::execute(Sql_cmd_dml * const this, THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_select.cc:782)
mysql_execute_command(THD * thd, bool first_level) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:3656)
dispatch_sql_command(THD * thd, Parser_state * parser_state, bool is_retry) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:5331)
dispatch_command(THD * thd, const COM_DATA * com_data, enum_server_command command) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:2122)
do_command(THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:1466)
handle_connection(void * arg) (\data\ldc_docker\mysql-server_9.0.0\sql\conn_handler\connection_handler_per_thread.cc:304)
pfs_spawn_thread(void * arg) (\data\ldc_docker\mysql-server_9.0.0\storage\perfschema\pfs.cc:3061)
libpthread.so.0!start_thread (Unknown Source:0)
libc.so.6!clone (Unknown Source:0)
```

插入时
```cpp
get_dimensions(const uint32_t length, const uint32_t precision) (\data\ldc_docker\mysql-server_9.0.0\sql\vector_conversion.h:139)
Field_vector::get_max_dimensions(const Field_vector * const this) (\data\ldc_docker\mysql-server_9.0.0\sql\field.h:3953)
Table_map_log_event::init_vector_dimensionality_field(Table_map_log_event * const this) (\data\ldc_docker\mysql-server_9.0.0\sql\log_event.cc:11412)
Table_map_log_event::init_metadata_fields(Table_map_log_event * const this) (\data\ldc_docker\mysql-server_9.0.0\sql\log_event.cc:11189)
Table_map_log_event::Table_map_log_event(Table_map_log_event * const this, THD * thd_arg, TABLE * tbl, const mysql::binlog::event::Table_id & tid, bool using_trans) (\data\ldc_docker\mysql-server_9.0.0\sql\log_event.cc:10741)
THD::binlog_write_table_map(THD * const this, TABLE * table, bool is_transactional, bool binlog_rows_query) (\data\ldc_docker\mysql-server_9.0.0\sql\binlog.cc:8549)
write_locked_table_maps(THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\handler.cc:7854)
binlog_log_row(TABLE * table, const uchar * before_record, const uchar * after_record, Log_func * log_func) (\data\ldc_docker\mysql-server_9.0.0\sql\handler.cc:7971)
handler::ha_write_row(handler * const this, uchar * buf) (\data\ldc_docker\mysql-server_9.0.0\sql\handler.cc:8081)
write_record(THD * thd, TABLE * table, COPY_INFO * info, COPY_INFO * update) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_insert.cc:2163)
Sql_cmd_insert_values::execute_inner(Sql_cmd_insert_values * const this, THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_insert.cc:632)
Sql_cmd_dml::execute(Sql_cmd_dml * const this, THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_select.cc:782)
mysql_execute_command(THD * thd, bool first_level) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:3656)
dispatch_sql_command(THD * thd, Parser_state * parser_state, bool is_retry) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:5331)
dispatch_command(THD * thd, const COM_DATA * com_data, enum_server_command command) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:2122)
do_command(THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:1466)
handle_connection(void * arg) (\data\ldc_docker\mysql-server_9.0.0\sql\conn_handler\connection_handler_per_thread.cc:304)
pfs_spawn_thread(void * arg) (\data\ldc_docker\mysql-server_9.0.0\storage\perfschema\pfs.cc:3061)
libpthread.so.0!start_thread (Unknown Source:0)
libc.so.6!clone (Unknown Source:0)
```