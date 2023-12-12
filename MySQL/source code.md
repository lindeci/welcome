- [internals manual](#internals-manual)
- [编码准则](#编码准则)
  - [一般开发准则](#一般开发准则)
  - [DBUG 标签](#dbug-标签)
- [Infrastructure](#infrastructure)
  - [Container](#container)
  - [Synchronization](#synchronization)
  - [File IO](#file-io)
  - [Server building blocks](#server-building-blocks)
  - [Deployment](#deployment)
  - [Startup](#startup)
  - [Shutdown](#shutdown)
  - [Upgrade](#upgrade)
- [Client/Server Protocol](#clientserver-protocol)
  - [Basic Data Types](#basic-data-types)
    - [Integer Types](#integer-types)
    - [String Types](#string-types)


# internals manual

internals manual, see https://dev.mysql.com/doc/internals/en/index.html

# 编码准则

本节显示MySQL开发人员在编写新代码时遵循的准则。

新的MySQL代码使用Google C++编码风格（[https://google.github.io/styleguide/cppguide.html](https://google.github.io/styleguide/cppguide.html)），但有两个例外：

* 成员变量名称：不要使用 foo_。请改用m_foo（非静态）或s_foo（静态）。

旧项目和对旧代码的修改暂时使用旧的MySQL特定样式。从 8.0 开始，MySQL 样式使用与 Google 编码样式相同的格式规则（例如，大括号放置、缩进、行长等），但在几个重要方面有所不同：

* 类名：不要使用 MyClass。请改用My_class。
* 函数名称：使用 snake_case（）。
* 注释样式：使用 // 或 /* **/* 语法。更常见，但暂时允许两种语法。
* Doxygen 注释：使用 /** ...*/ 语法，而不是 /*/* /。
* Doxygen 命令：使用 “@” 而不是 '\' 表示 doxygen 命令。
* 您可能会看到以 st_ 开头的结构并被类型化为一些大写（例如 typedef struct st_foo { ... }福）。但是，这是代码库包含 C 时的遗留问题。不要制作带有st_前缀的新 typedef 或结构，并随意删除已经存在的那些，除了作为 libmysql 一部分的公共头文件（需要可解析为 C99）。

代码格式设置是通过在整个代码库中使用 clang 格式来强制执行的。但是，请注意，格式只是编码风格的一部分;您需要自己处理非格式问题，例如遵循命名约定、明确代码所有权或尽量减少宏的使用。有关整个列表，请参阅Google编码风格指南。

一致的风格对我们来说很重要，因为每个人都必须知道会发生什么。了解我们的规则后，您会发现阅读我们的代码更容易，当您决定贡献时（我们希望您会考虑！），我们会发现阅读和审查您的代码更容易。

## 一般开发准则

我们使用 Git 进行源代码管理。

您应该使用 TRUNK 源代码树（目前称为“mysql-trunk”）进行所有新开发。要下载并设置公共开发分支，请使用以下命令：

```sh
shell> git clone https：//github.com/mysql/mysql-server.git mysql-trunk
shell> cd mysql-trunk
shell> git branch mysql-trunk
```

在做出重大设计决策之前，请先发布一份摘要，说明你想做什么，为什么要做，以及你计划如何做。通过这种方式，我们可以轻松地为您提供反馈，并对其进行彻底讨论。也许其他开发人员可以为您提供帮

## DBUG 标签

DBUG 库的完整文档位于 MySQL 源代码树中的文件 dbug/user.* 中。以下是我们现在使用的一些 DBUG 标签：

* 进入函数的参数。
* 退出函数的结果。
* 信息可能很有趣的东西。
* 警告当某些事情没有走通常的路线或可能出错时。
* 错误当出现问题时。
* 圈
  在循环中写入，这可能仅在调试循环时才有用。当您对代码感到满意并且它已经实际使用一段时间时，通常应该删除这些代码。

一些特定于mysqld的标签，因为我们想仔细观察这些标签：

* 反式启动/停止事务。
* 退出Mysqld 准备死亡时的信息。
* 查询
  打印查询。

# Infrastructure

Basic classes and templates

## Container

See DYNAMIC_ARRAY, List, I_P_List, LF_HASH.

## Synchronization

See native_mutex_t, native_rw_lock_t, native_cond_t.

## File IO

See my_open, my_dir.

## Server building blocks

Virtual Input Output
See Vio, vio_init.

## Deployment

Installation
See opt_initialize, bootstrap::run_bootstrap_thread.

## Startup

See mysqld_main.

## Shutdown

See handle_fatal_signal, signal_hand.

## Upgrade

See Mysql::Tools::Upgrade::Program.



# Client/Server Protocol

**Overview**

The MySQL protocol is used between MySQL Clients and a MySQL Server. It is implemented by:

* Connectors (Connector/C, Connector/J, and so forth)
* MySQL Proxy
* Communication between master and slave replication servers

The protocol supports these features:

* Transparent encryption using SSL
* Transparent compression
* A[Connection Phase](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_connection_phase.html) where capabilities and authentication data are exchanged
* A[Command Phase](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_command_phase.html) which accepts commands from the client and executes them

Further reading:

* [Protocol Basics](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basics.html)
* [Connection Lifecycle](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_connection_lifecycle.html)


## Basic Data Types

The protocol has a few basic types that are used throughout the protocol:

* [Integer Types](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basic_dt_integers.html)
* [String Types](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basic_dt_strings.html)


### Integer Types

The MySQL Protocol has a set of possible encodings for integers.

**Protocol::FixedLengthInteger**

**Fixed-Length Integer Types**

A fixed-length unsigned integer stores its value in a series of bytes with the least significant byte first.

The MySQL uses the following fixed-length unsigned integer variants:

* []()int<1>: 1 byte[Protocol::FixedLengthInteger](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basic_dt_integers.html#sect_protocol_basic_dt_int_fixed).
* []()int<2>: 2 byte[Protocol::FixedLengthInteger](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basic_dt_integers.html#sect_protocol_basic_dt_int_fixed). See int2store()
* []()int<3>: 3 byte[Protocol::FixedLengthInteger](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basic_dt_integers.html#sect_protocol_basic_dt_int_fixed). See int3store()
* []()int<4>: 4 byte[Protocol::FixedLengthInteger](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basic_dt_integers.html#sect_protocol_basic_dt_int_fixed). See int4store()
* []()int<6>: 6 byte[Protocol::FixedLengthInteger](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basic_dt_integers.html#sect_protocol_basic_dt_int_fixed). See int6store()
* []()int<8>: 8 byte[Protocol::FixedLengthInteger](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basic_dt_integers.html#sect_protocol_basic_dt_int_fixed). See int8store()

See int3store() for an example.

**Protocol::LengthEncodedInteger**

**Length-Encoded Integer Type**

An integer that consumes 1, 3, 4, or 9 bytes, depending on its numeric value

To convert a number value into a length-encoded integer:

| Greater or equal | Lower than | Stored as                 |
| ---------------- | ---------- | ------------------------- |
| 0                | 251        | `1-byte integer`        |
| 251              | 2^16^      | `0xFC + 2-byte integer` |
| 2^16^            | 2^24^      | `0xFD + 3-byte integer` |
| 2^24^            | 2^64^      | `0xFE + 8-byte integer` |

Similarly, to convert a length-encoded integer into its numeric value check the first byte.

**Warning**

```
If the first byte of a packet is a length-encoded integer and its byte value is 0xFE, you must check the length of the packet to verify that it has enough space for a 8-byte integer. If not, it may be an EOF_Packet instead.
```

### String Types

Strings are sequences of bytes and appear in a few forms in the protocol.

- Protocol::FixedLengthString  
Fixed-length strings have a known, hardcoded length.  
An example is the sql-state of the [ERR_Packet](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basic_err_packet.html) which is always 5 bytes long.

- Protocol::NullTerminatedString  
Strings that are terminated by a `00` byte.

- Protocol::VariableLengthString  
The length of the string is determined by another field or is calculated at runtime

- Protocol::LengthEncodedString  
A length encoded string is a string that is prefixed with length encoded integer describing the length of the string.  
It is a special case of [Protocol::VariableLengthString](https://dev.mysql.com/doc/dev/mysql-server/8.1.0/page_protocol_basic_dt_strings.html#sect_protocol_basic_dt_string_var)

- Protocol::RestOfPacketString  
If a string is the last component of a packet, its length can be calculated from the overall packet length minus the current position.
