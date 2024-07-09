- [官方文档](#官方文档)
- [环境准备](#环境准备)
- [源码编译](#源码编译)
  - [configure 选项](#configure-选项)
    - [安装目录选项](#安装目录选项)
    - [安装 PostgreSQL 特征选项](#安装-postgresql-特征选项)
    - [拒绝特征选项](#拒绝特征选项)
    - [编译进程细节](#编译进程细节)
    - [Miscellaneous 选项](#miscellaneous-选项)
    - [开发选项](#开发选项)
    - [设置环境变量](#设置环境变量)
- [创建 Database Cluster](#创建-database-cluster)
- [启动 Database Server](#启动-database-server)
- [参数设置](#参数设置)
  - [通过配置文件设置](#通过配置文件设置)
  - [通过 SQL 设置参数](#通过-sql-设置参数)
  - [通过 SHELL 脚本设置](#通过-shell-脚本设置)
  - [管理配置文件嵌套](#管理配置文件嵌套)
  - [文件路径参数](#文件路径参数)
  - [连接和认证参数](#连接和认证参数)
    - [连接参数](#连接参数)
    - [TCP 设置参数](#tcp-设置参数)
    - [认证参数](#认证参数)
    - [SSL 参数](#ssl-参数)
  - [资源消耗参数](#资源消耗参数)
    - [内存](#内存)
    - [磁盘](#磁盘)
    - [内核资源使用](#内核资源使用)
    - [基于成本的 VACUUM 延迟](#基于成本的-vacuum-延迟)
    - [后台写](#后台写)
    - [异步表现](#异步表现)
  - [WAL 参数](#wal-参数)
    - [配置](#配置)
    - [Checkpoints 设置](#checkpoints-设置)
    - [归档](#归档)
    - [还原](#还原)
    - [归档还原](#归档还原)
    - [还原目标](#还原目标)
    - [WAL 汇总](#wal-汇总)
  - [Replication](#replication)
    - [Sending Servers](#sending-servers)
    - [Primary Server](#primary-server)
    - [Standby Servers](#standby-servers)
    - [Subscribers](#subscribers)
  - [查询计划](#查询计划)
    - [Planner Method Configuration](#planner-method-configuration)
    - [Planner Cost Constants](#planner-cost-constants)
    - [Genetic Query Optimizer](#genetic-query-optimizer)
    - [Other Planner Options](#other-planner-options)
  - [错误报告和日志](#错误报告和日志)
    - [日志记录位置](#日志记录位置)
    - [日志记录时间](#日志记录时间)
    - [日志记录内容](#日志记录内容)
    - [使用 CSV 格式日志输出](#使用-csv-格式日志输出)
    - [使用 JSON 格式日志输出](#使用-json-格式日志输出)
    - [进程标题](#进程标题)
  - [运行时统计](#运行时统计)
    - [累积查询和索引统计](#累积查询和索引统计)
    - [统计监控](#统计监控)
  - [自动清理](#自动清理)
  - [客户端连接默认参数](#客户端连接默认参数)
    - [语句行为](#语句行为)
    - [地区和格式化](#地区和格式化)
    - [共享库预加载](#共享库预加载)
    - [其他默认值](#其他默认值)
  - [锁管理](#锁管理)
  - [版本和平台兼容性](#版本和平台兼容性)
    - [以前的 PostgreSQL 版本](#以前的-postgresql-版本)
    - [平台和客户端兼容性](#平台和客户端兼容性)
  - [错误处理](#错误处理)
  - [预设选项](#预设选项)
  - [自定义选项](#自定义选项)
  - [开发者选项](#开发者选项)
  - [简写选项](#简写选项)
- [客户端认证](#客户端认证)
- [数据库角色](#数据库角色)
  - [Database Roles](#database-roles)
  - [Role Attributes](#role-attributes)
  - [Role Membership](#role-membership)
  - [Dropping Roles](#dropping-roles)
  - [Predefined Roles](#predefined-roles)
  - [Function Security](#function-security)
- [管理 Databases](#管理-databases)
  - [Overview](#overview)
  - [Creating a Database](#creating-a-database)
  - [Template Databases](#template-databases)
  - [Database Configuration](#database-configuration)
  - [Destroying a Database](#destroying-a-database)
  - [Tablespaces](#tablespaces)
- [Localization](#localization)
  - [Locale Support](#locale-support)
  - [Collation Support](#collation-support)
  - [Character Set Support](#character-set-support)
- [日常数据库维护任务](#日常数据库维护任务)
- [Chapter 25. Backup and Restore](#chapter-25-backup-and-restore)
  - [25.1. SQL Dump](#251-sql-dump)
  - [25.2. File System Level Backup](#252-file-system-level-backup)
  - [25.3. Continuous Archiving and Point-in-Time Recovery (PITR)](#253-continuous-archiving-and-point-in-time-recovery-pitr)
- [](#)
- [](#-1)
- [PostgreSQL 内核](#postgresql-内核)
  - [50.1 查询的路径](#501-查询的路径)
  - [50.2. 如何建立连接](#502-如何建立连接)
  - [50.3. 解析阶段](#503-解析阶段)
    - [50.3.1. 解析器](#5031-解析器)
    - [50.3.2. 转换过程](#5032-转换过程)
  - [50.4. PostgreSQL 规则系统](#504-postgresql-规则系统)
  - [50.5. 计划器/优化器](#505-计划器优化器)
    - [50.5.1. 生成可能的计划](#5051-生成可能的计划)
- [50.6. 执行器](#506-执行器)

# 官方文档
https://www.postgresql.org/docs/17/index.html

# 环境准备
参考：https://www.postgresql.org/docs/17/installation.html  
依赖参考：https://www.postgresql.org/docs/17/install-requirements.html  

对CPU架构依赖：https://www.postgresql.org/docs/17/supported-platforms.html  
x86, PowerPC, S/390, SPARC, ARM, MIPS, RISC-V, and PA-RISC, including big-endian, little-endian, 32-bit, and 64-bit variants where applicable.

对OS依赖：Linux, Windows, FreeBSD, OpenBSD, NetBSD, DragonFlyBSD, macOS, Solaris, and illumos. Other Unix-like systems may also work but are not currently being tested. 

必须依赖的包：
- GNU make version 3.81
- Alternatively, PostgreSQL can be built using Meson. 
- You need an ISO/ANSI C compiler (at least C99-compliant). 
- tar is required to unpack the source distribution, in addition to either gzip or bzip2.
- Flex 2.5.35 or later and Bison 2.3 or later are required. 
- Perl 5.14 or later is needed during the build process and to run some test suites. 
- The GNU Readline library is used by default. It allows psql (the PostgreSQL command line SQL interpreter) to remember each command you type, and allows you to use arrow keys to recall and edit previous commands. 
- The zlib compression library is used by default. If you don't want to use it then you must specify the --without-zlib option to configure. Using this option disables support for compressed archives in pg_dump and pg_restore.
- The ICU library is used by default. If you don't want to use it then you must specify the --without-icu option to configure. Using this option disables support for ICU collation features
docker pull ubuntu

可选依赖的包：
- To build the server programming language PL/Perl you need a full Perl installation, including the libperl library and the header files. The minimum required version is Perl 5.14. 
- To build the PL/Python server programming language, you need a Python installation with the header files and the sysconfig module. The minimum required version is Python 3.2.
- To build the PL/Tcl procedural language, you of course need a Tcl installation. The minimum required version is Tcl 8.4.
- To enable Native Language Support (NLS), that is, the ability to display a program's messages in a language other than English, you need an implementation of the Gettext API. Some operating systems have this built-in (e.g., Linux, NetBSD, Solaris), for other systems you can download an add-on package from https://www.gnu.org/software/gettext/. If you are using the Gettext implementation in the GNU C library, then you will additionally need the GNU Gettext package for some utility programs. For any of the other implementations you will not need it.
- You need OpenSSL, if you want to support encrypted client connections. OpenSSL is also required for random number generation on platforms that do not have /dev/urandom (except Windows). The minimum required version is 1.0.2.
- You need MIT Kerberos (for GSSAPI), OpenLDAP, and/or PAM, if you want to support authentication using those services.
- You need LZ4, if you want to support compression of data with that method
- You need Zstandard, if you want to support compression of data with that method
- To build the PostgreSQL documentation, there is a separate set of requirements; see Section J.2.

# 源码编译
```sh
# 使用 ubuntu 镜像作为基础镜像
docker pull ubuntu
docker run -it --rm -v $PWD:/root ubuntu
# 更新 apt 包列表
apt-get update

# 安装必要的软件包
apt-get install cmake git bison flex tar gcc libicu-dev libreadline-dev zlib1g-dev

git clone https://github.com/postgres/postgres.git -b REL_17_STABLE --depth 1

cd postgres/
mkdir build
./configure --prefix=/data/postgres/build --enable-debug --prefix=/data/postgres/build ICU_CFLAGS='-I/usr/include' ICU_LIBS='-L/usr/lib/x86_64-linux-gnu -licui18n -licuuc -licudata'
make -j 32
# useradd postgres
# chown -R postgres:postgres /data/postgres
# su postgres -c'make check'
make install
# make install-docs
# 卸载 make uninstall
# 清理 make clean
```
## configure 选项
### 安装目录选项
```
--prefix=PREFIX
    Install all files under the directory PREFIX instead of /usr/local/pgsql. The actual files will be installed into various subdirectories; no files will ever be installed directly into the PREFIX directory.

--exec-prefix=EXEC-PREFIX
    You can install architecture-dependent files under a different prefix, EXEC-PREFIX, than what PREFIX was set to. This can be useful to share architecture-independent files between hosts. If you omit this, then EXEC-PREFIX is set equal to PREFIX and both architecture-dependent and independent files will be installed under the same tree, which is probably what you want.

--bindir=DIRECTORY
    Specifies the directory for executable programs. The default is EXEC-PREFIX/bin, which normally means /usr/local/pgsql/bin.

--sysconfdir=DIRECTORY
    Sets the directory for various configuration files, PREFIX/etc by default.

--libdir=DIRECTORY
    Sets the location to install libraries and dynamically loadable modules. The default is EXEC-PREFIX/lib.

--includedir=DIRECTORY
    Sets the directory for installing C and C++ header files. The default is PREFIX/include.

--datarootdir=DIRECTORY
    Sets the root directory for various types of read-only data files. This only sets the default for some of the following options. The default is PREFIX/share.

--datadir=DIRECTORY
    Sets the directory for read-only data files used by the installed programs. The default is DATAROOTDIR. Note that this has nothing to do with where your database files will be placed.

--localedir=DIRECTORY
    Sets the directory for installing locale data, in particular message translation catalog files. The default is DATAROOTDIR/locale.

--mandir=DIRECTORY
    The man pages that come with PostgreSQL will be installed under this directory, in their respective manx subdirectories. The default is DATAROOTDIR/man.

--docdir=DIRECTORY
    Sets the root directory for installing documentation files, except “man” pages. This only sets the default for the following options. The default value for this option is DATAROOTDIR/doc/postgresql.

--htmldir=DIRECTORY
    The HTML-formatted documentation for PostgreSQL will be installed under this directory. The default is DATAROOTDIR.
```
### 安装 PostgreSQL 特征选项
```
--enable-nls[=LANGUAGES]
    Enables Native Language Support (NLS), that is, the ability to display a program's messages in a language other than English. LANGUAGES is an optional space-separated list of codes of the languages that you want supported, for example --enable-nls='de fr'. (The intersection between your list and the set of actually provided translations will be computed automatically.) If you do not specify a list, then all available translations are installed.

    To use this option, you will need an implementation of the Gettext API.

--with-perl
    Build the PL/Perl server-side language.

--with-python
    Build the PL/Python server-side language.

--with-tcl
    Build the PL/Tcl server-side language.

--with-tclconfig=DIRECTORY
    Tcl installs the file tclConfig.sh, which contains configuration information needed to build modules interfacing to Tcl. This file is normally found automatically at a well-known location, but if you want to use a different version of Tcl you can specify the directory in which to look for tclConfig.sh.

--with-llvm
    Build with support for LLVM based JIT compilation (see Chapter 30). This requires the LLVM library to be installed. The minimum required version of LLVM is currently 10.

    llvm-config will be used to find the required compilation options. llvm-config, and then llvm-config-$major-$minor for all supported versions, will be searched for in your PATH. If that would not yield the desired program, use LLVM_CONFIG to specify a path to the correct llvm-config. For example

    ./configure ... --with-llvm LLVM_CONFIG='/path/to/llvm/bin/llvm-config'

    LLVM support requires a compatible clang compiler (specified, if necessary, using the CLANG environment variable), and a working C++ compiler (specified, if necessary, using the CXX environment variable).

--with-lz4
    Build with LZ4 compression support.

--with-zstd
    Build with Zstandard compression support.

--with-ssl=LIBRARY
    Build with support for SSL (encrypted) connections. The only LIBRARY supported is openssl. This requires the OpenSSL package to be installed. configure will check for the required header files and libraries to make sure that your OpenSSL installation is sufficient before proceeding.

--with-openssl
    Obsolete equivalent of --with-ssl=openssl.

--with-gssapi
    Build with support for GSSAPI authentication. MIT Kerberos is required to be installed for GSSAPI. On many systems, the GSSAPI system (a part of the MIT Kerberos installation) is not installed in a location that is searched by default (e.g., /usr/include, /usr/lib), so you must use the options --with-includes and --with-libraries in addition to this option. configure will check for the required header files and libraries to make sure that your GSSAPI installation is sufficient before proceeding.

--with-ldap
    Build with LDAP support for authentication and connection parameter lookup (see Section 32.18 and Section 20.10 for more information). On Unix, this requires the OpenLDAP package to be installed. On Windows, the default WinLDAP library is used. configure will check for the required header files and libraries to make sure that your OpenLDAP installation is sufficient before proceeding.

--with-pam
    Build with PAM (Pluggable Authentication Modules) support.

--with-bsd-auth
    Build with BSD Authentication support. (The BSD Authentication framework is currently only available on OpenBSD.)

--with-systemd
    Build with support for systemd service notifications. This improves integration if the server is started under systemd but has no impact otherwise; see Section 18.3 for more information. libsystemd and the associated header files need to be installed to use this option.

--with-bonjour
    Build with support for Bonjour automatic service discovery. This requires Bonjour support in your operating system. Recommended on macOS.

--with-uuid=LIBRARY
    Build the uuid-ossp module (which provides functions to generate UUIDs), using the specified UUID library. LIBRARY must be one of:

        bsd to use the UUID functions found in FreeBSD and some other BSD-derived systems

        e2fs to use the UUID library created by the e2fsprogs project; this library is present in most Linux systems and in macOS, and can be obtained for other platforms as well

        ossp to use the OSSP UUID library

--with-ossp-uuid
    Obsolete equivalent of --with-uuid=ossp.

--with-libxml
    Build with libxml2, enabling SQL/XML support. Libxml2 version 2.6.23 or later is required for this feature.

    To detect the required compiler and linker options, PostgreSQL will query pkg-config, if that is installed and knows about libxml2. Otherwise the program xml2-config, which is installed by libxml2, will be used if it is found. Use of pkg-config is preferred, because it can deal with multi-architecture installations better.

    To use a libxml2 installation that is in an unusual location, you can set pkg-config-related environment variables (see its documentation), or set the environment variable XML2_CONFIG to point to the xml2-config program belonging to the libxml2 installation, or set the variables XML2_CFLAGS and XML2_LIBS. (If pkg-config is installed, then to override its idea of where libxml2 is you must either set XML2_CONFIG or set both XML2_CFLAGS and XML2_LIBS to nonempty strings.)

--with-libxslt
    Build with libxslt, enabling the xml2 module to perform XSL transformations of XML. --with-libxml must be specified as well.

--with-selinux
    Build with SElinux support, enabling the sepgsql extension.
```

### 拒绝特征选项
```
--without-icu
    Build without support for the ICU library, disabling the use of ICU collation features (see Section 23.2).

--without-readline
    Prevents use of the Readline library (and libedit as well). This option disables command-line editing and history in psql.

--with-libedit-preferred
    Favors the use of the BSD-licensed libedit library rather than GPL-licensed Readline. This option is significant only if you have both libraries installed; the default in that case is to use Readline.

--without-zlib
    Prevents use of the Zlib library. This disables support for compressed archives in pg_dump and pg_restore.

--disable-spinlocks
    Allow the build to succeed even if PostgreSQL has no CPU spinlock support for the platform. The lack of spinlock support will result in very poor performance; therefore, this option should only be used if the build aborts and informs you that the platform lacks spinlock support. If this option is required to build PostgreSQL on your platform, please report the problem to the PostgreSQL developers.

--disable-atomics
    Disable use of CPU atomic operations. This option does nothing on platforms that lack such operations. On platforms that do have them, this will result in poor performance. This option is only useful for debugging or making performance comparisons.
```

### 编译进程细节
```
--with-includes=DIRECTORIES
    DIRECTORIES is a colon-separated list of directories that will be added to the list the compiler searches for header files. If you have optional packages (such as GNU Readline) installed in a non-standard location, you have to use this option and probably also the corresponding --with-libraries option.

    Example: --with-includes=/opt/gnu/include:/usr/sup/include.

--with-libraries=DIRECTORIES
    DIRECTORIES is a colon-separated list of directories to search for libraries. You will probably have to use this option (and the corresponding --with-includes option) if you have packages installed in non-standard locations.

    Example: --with-libraries=/opt/gnu/lib:/usr/sup/lib.

--with-system-tzdata=DIRECTORY
    PostgreSQL includes its own time zone database, which it requires for date and time operations. This time zone database is in fact compatible with the IANA time zone database provided by many operating systems such as FreeBSD, Linux, and Solaris, so it would be redundant to install it again. When this option is used, the system-supplied time zone database in DIRECTORY is used instead of the one included in the PostgreSQL source distribution. DIRECTORY must be specified as an absolute path. /usr/share/zoneinfo is a likely directory on some operating systems. Note that the installation routine will not detect mismatching or erroneous time zone data. If you use this option, you are advised to run the regression tests to verify that the time zone data you have pointed to works correctly with PostgreSQL.

    This option is mainly aimed at binary package distributors who know their target operating system well. The main advantage of using this option is that the PostgreSQL package won't need to be upgraded whenever any of the many local daylight-saving time rules change. Another advantage is that PostgreSQL can be cross-compiled more straightforwardly if the time zone database files do not need to be built during the installation.

--with-extra-version=STRING
    Append STRING to the PostgreSQL version number. You can use this, for example, to mark binaries built from unreleased Git snapshots or containing custom patches with an extra version string, such as a git describe identifier or a distribution package release number.

--disable-rpath
    Do not mark PostgreSQL's executables to indicate that they should search for shared libraries in the installation's library directory (see --libdir). On most platforms, this marking uses an absolute path to the library directory, so that it will be unhelpful if you relocate the installation later. However, you will then need to provide some other way for the executables to find the shared libraries. Typically this requires configuring the operating system's dynamic linker to search the library directory; see Section 17.5.1 for more detail.
```

### Miscellaneous 选项
这些选项很少被使用，可能测试时会被使用
```
--with-pgport=NUMBER
    Set NUMBER as the default port number for server and clients. The default is 5432. The port can always be changed later on, but if you specify it here then both server and clients will have the same default compiled in, which can be very convenient. Usually the only good reason to select a non-default value is if you intend to run multiple PostgreSQL servers on the same machine.

--with-krb-srvnam=NAME
    The default name of the Kerberos service principal used by GSSAPI. postgres is the default. There's usually no reason to change this unless you are building for a Windows environment, in which case it must be set to upper case POSTGRES.

--with-segsize=SEGSIZE
    Set the segment size, in gigabytes. Large tables are divided into multiple operating-system files, each of size equal to the segment size. This avoids problems with file size limits that exist on many platforms. The default segment size, 1 gigabyte, is safe on all supported platforms. If your operating system has “largefile” support (which most do, nowadays), you can use a larger segment size. This can be helpful to reduce the number of file descriptors consumed when working with very large tables. But be careful not to select a value larger than is supported by your platform and the file systems you intend to use. Other tools you might wish to use, such as tar, could also set limits on the usable file size. It is recommended, though not absolutely required, that this value be a power of 2. Note that changing this value breaks on-disk database compatibility, meaning you cannot use pg_upgrade to upgrade to a build with a different segment size.

--with-blocksize=BLOCKSIZE
    Set the block size, in kilobytes. This is the unit of storage and I/O within tables. The default, 8 kilobytes, is suitable for most situations; but other values may be useful in special cases. The value must be a power of 2 between 1 and 32 (kilobytes). Note that changing this value breaks on-disk database compatibility, meaning you cannot use pg_upgrade to upgrade to a build with a different block size.

--with-wal-blocksize=BLOCKSIZE
    Set the WAL block size, in kilobytes. This is the unit of storage and I/O within the WAL log. The default, 8 kilobytes, is suitable for most situations; but other values may be useful in special cases. The value must be a power of 2 between 1 and 64 (kilobytes). Note that changing this value breaks on-disk database compatibility, meaning you cannot use pg_upgrade to upgrade to a build with a different WAL block size.
```

### 开发选项
```
--enable-debug
    Compiles all programs and libraries with debugging symbols. This means that you can run the programs in a debugger to analyze problems. This enlarges the size of the installed executables considerably, and on non-GCC compilers it usually also disables compiler optimization, causing slowdowns. However, having the symbols available is extremely helpful for dealing with any problems that might arise. Currently, this option is recommended for production installations only if you use GCC. But you should always have it on if you are doing development work or running a beta version.

--enable-cassert
    Enables assertion checks in the server, which test for many “cannot happen” conditions. This is invaluable for code development purposes, but the tests can slow down the server significantly. Also, having the tests turned on won't necessarily enhance the stability of your server! The assertion checks are not categorized for severity, and so what might be a relatively harmless bug will still lead to server restarts if it triggers an assertion failure. This option is not recommended for production use, but you should have it on for development work or when running a beta version.

--enable-tap-tests
    Enable tests using the Perl TAP tools. This requires a Perl installation and the Perl module IPC::Run. See Section 31.4 for more information.

--enable-depend
    Enables automatic dependency tracking. With this option, the makefiles are set up so that all affected object files will be rebuilt when any header file is changed. This is useful if you are doing development work, but is just wasted overhead if you intend only to compile once and install. At present, this option only works with GCC.

--enable-coverage
    If using GCC, all programs and libraries are compiled with code coverage testing instrumentation. When run, they generate files in the build directory with code coverage metrics. See Section 31.5 for more information. This option is for use only with GCC and when doing development work.

--enable-profiling
    If using GCC, all programs and libraries are compiled so they can be profiled. On backend exit, a subdirectory will be created that contains the gmon.out file containing profile data. This option is for use only with GCC and when doing development work.

--enable-dtrace
    Compiles PostgreSQL with support for the dynamic tracing tool DTrace. See Section 27.5 for more information.

    To point to the dtrace program, the environment variable DTRACE can be set. This will often be necessary because dtrace is typically installed under /usr/sbin, which might not be in your PATH.

    Extra command-line options for the dtrace program can be specified in the environment variable DTRACEFLAGS. On Solaris, to include DTrace support in a 64-bit binary, you must specify DTRACEFLAGS="-64". For example, using the GCC compiler:

    ./configure CC='gcc -m64' --enable-dtrace DTRACEFLAGS='-64' ...

    Using Sun's compiler:

    ./configure CC='/opt/SUNWspro/bin/cc -xtarget=native64' --enable-dtrace DTRACEFLAGS='-64' ...

--enable-injection-points
    Compiles PostgreSQL with support for injection points in the server. Injection points allow to run user-defined code from within the server in pre-defined code paths. This helps in testing and in the investigation of concurrency scenarios in a controlled fashion. This option is disabled by default. See Section 36.10.13 for more details. This option is intended to be used only by developers for testing.

--with-segsize-blocks=SEGSIZE_BLOCKS
    Specify the relation segment size in blocks. If both --with-segsize and this option are specified, this option wins. This option is only for developers, to test segment related code.
```
### 设置环境变量
```
BISON
    Bison program

CC
    C compiler

CFLAGS
    options to pass to the C compiler

CLANG
    path to clang program used to process source code for inlining when compiling with --with-llvm

CPP
    C preprocessor

CPPFLAGS
    options to pass to the C preprocessor

CXX
    C++ compiler

CXXFLAGS
    options to pass to the C++ compiler

DTRACE
    location of the dtrace program

DTRACEFLAGS
    options to pass to the dtrace program

FLEX
    Flex program

LDFLAGS
    options to use when linking either executables or shared libraries

LDFLAGS_EX
    additional options for linking executables only

LDFLAGS_SL
    additional options for linking shared libraries only

LLVM_CONFIG
    llvm-config program used to locate the LLVM installation

MSGFMT
    msgfmt program for native language support

PERL
    Perl interpreter program. This will be used to determine the dependencies for building PL/Perl. The default is perl.

PYTHON
    Python interpreter program. This will be used to determine the dependencies for building PL/Python. If this is not set, the following are probed in this order: python3 python.

TCLSH
    Tcl interpreter program. This will be used to determine the dependencies for building PL/Tcl. If this is not set, the following are probed in this order: tclsh tcl tclsh8.6 tclsh86 tclsh8.5 tclsh85 tclsh8.4 tclsh84.

XML2_CONFIG
    xml2-config program used to locate the libxml2 installation
```

# 创建 Database Cluster
```sh
mkdir data
chown -R postgres:postgres data
su postgres -c 'bin/pg_ctl -Ddata initdb'
```

# 启动 Database Server
```sh
su postgres -c 'bin/pg_ctl -D data -l logfile start'

bin/psql -U postgres
```

# 参数设置
## 通过配置文件设置
修改文件中的参数后，通过 pg_reload_conf() 加载。注意：allow_alter_system 为 on 时不能修改 postgresql.auto.conf
## 通过 SQL 设置参数
[ALTER DATABASE](https://www.postgresql.org/docs/17/sql-alterdatabase.html)  
[ALTER ROLE](https://www.postgresql.org/docs/17/sql-alterrole.html)  
[SHOW](https://www.postgresql.org/docs/17/sql-alterdatabase.html)  
[SET](https://www.postgresql.org/docs/17/sql-set.html)  
Querying this 类似 SHOW，但它更灵活，它可以过滤  
UPDATE on this view，等价于 `SET`  
比如 
```sql
SET configuration_parameter TO DEFAULT; 
等价于
UPDATE pg_settings SET setting = reset_val WHERE name = 'configuration_parameter';
```
## 通过 SHELL 脚本设置
在 server 启动期间，通过 `-c name=value` 来设置，比如
```sh
postgres -c log_connections=yes --log-destination='syslog'
```sh
通过 libpq 启动客户端会话时，可以 
env PGOPTIONS="-c geqo=off --statement-timeout=5min" psql
```
## 管理配置文件嵌套
- include 'filename'
- include_dir 'directory'

## 文件路径参数
```
data_directory (string)  
config_file (string)  
hba_file (string)  
ident_file (string)  
external_pid_file (string)  
```
## 连接和认证参数
### 连接参数
https://www.postgresql.org/docs/17/runtime-config-connection.html

- `listen_addresses (string)` 监听地址：指定服务器监听的IP地址。可以是主机名、IP地址或特殊的 '*'（表示所有IP地址）。
- `port (integer)` 端口：服务器监听的端口号，默认是5432。
- `max_connections (integer)` 最大连接数：允许的最大客户端连接数。
- `reserved_connections (integer)` 预留连接数：为非超级用户预留的最大连接数。
- `superuser_reserved_connections (integer)` 超级用户预留连接数：为超级用户预留的最大连接数。
- `unix_socket_directories (string)` Unix 套接字目录：指定服务器创建 Unix 套接字文件的目录。
- `unix_socket_group (string)` Unix 套接字组：指定 Unix 套接字文件的组权限。
- `unix_socket_permissions (integer)` Unix 套接字权限：指定 Unix 套接字文件的权限模式。
- `bonjour_name (string)` Bonjour 名称：使用 Bonjour 发布的服务器服务名称。
### TCP 设置参数
- `tcp_keepalives_idle (integer)` TCP 保活空闲时间：TCP 保活探测之前的空闲时间（以秒为单位）。
- `tcp_keepalives_interval (integer)` TCP 保活间隔时间：TCP 保活探测之间的时间间隔（以秒为单位）。
- `tcp_keepalives_count (integer)` TCP 保活探测次数：在认定连接断开之前发送的保活探测次数。
- `tcp_user_timeout (integer)` TCP 用户超时时间：发送超时后等待的时间（以毫秒为单位），在这段时间后，如果未收到确认，连接将被关闭。
- `client_connection_check_interval (integer)` 客户端连接检查间隔：检查客户端连接状态的时间间隔（以秒为单位）。

### 认证参数
- `authentication_timeout (integer)` 认证超时时间：设置客户端认证过程的最大等待时间（以秒为单位）。
- `password_encryption (enum)` 密码加密：指定存储用户密码时使用的加密方式，可以是 `md5` 或 `scram-sha-256`。
- `scram_iterations (integer)` SCRAM 迭代次数：指定在 SCRAM-SHA-256 认证中使用的迭代次数。
- `krb_server_keyfile (string)` Kerberos 服务器密钥文件：指定服务器的 Kerberos 密钥表文件（keytab）的路径。
- `krb_caseins_users (boolean)` Kerberos 用户名不区分大小写：启用后，Kerberos 用户名比较时将不区分大小写。
- `gss_accept_delegation (boolean)` 接受 GSSAPI 委派：启用后，服务器将接受客户端的 GSSAPI 委派凭证。
### SSL 参数

## 资源消耗参数
### 内存
- `shared_buffers (integer)` 共享缓冲区大小：用于 PostgreSQL 共享缓冲区的内存大小（以 8KB 为单位）。
- `huge_pages (enum)` 大页支持：控制是否使用大页内存，可选值有 `off`、`on`、`try`。
- `huge_page_size (integer)` 大页大小：设置大页内存的大小（以 KB 为单位）。
- `temp_buffers (integer)` 临时缓冲区：为临时表分配的缓冲区内存大小（以 8KB 为单位）。
- `max_prepared_transactions (integer)` 最大预备事务数：最大允许的预备事务数量。
- `work_mem (integer)` 工作内存：每个排序和哈希操作可使用的内存大小（以 KB 为单位）。
- `hash_mem_multiplier (floating point)` 哈希内存倍数：哈希表内存大小相对于 `work_mem` 的倍数。
- `maintenance_work_mem (integer)` 维护工作内存：数据库维护操作（如 `VACUUM`、`CREATE INDEX`）可使用的内存大小（以 KB 为单位）。
- `autovacuum_work_mem (integer)` 自动清理工作内存：自动清理进程可使用的内存大小（以 KB 为单位）。
- `vacuum_buffer_usage_limit (integer)` 清理缓冲区使用限制：`VACUUM` 操作期间可使用的缓冲区数量。
- `logical_decoding_work_mem (integer)` 逻辑解码工作内存：逻辑解码操作可使用的内存大小（以 KB 为单位）。
- `commit_timestamp_buffers (integer)` 提交时间戳缓冲区：用于存储事务提交时间戳的缓冲区数量。
- `multixact_member_buffers (integer)` 多事务成员缓冲区：用于存储多事务成员的缓冲区数量。
- `multixact_offset_buffers (integer)` 多事务偏移缓冲区：用于存储多事务偏移的缓冲区数量。
- `notify_buffers (integer)` 通知缓冲区：用于存储通知消息的缓冲区数量。
- `serializable_buffers (integer)` 可序列化缓冲区：用于可序列化事务的缓冲区数量。
- `subtransaction_buffers (integer)` 子事务缓冲区：用于存储子事务的缓冲区数量。
- `transaction_buffers (integer)` 事务缓冲区：用于存储事务的缓冲区数量。
- `max_stack_depth (integer)` 最大堆栈深度：允许的最大堆栈深度（以 KB 为单位）。
- `shared_memory_type (enum)` 共享内存类型：设置共享内存的实现类型，可选值有 `mmap`、`sysv`。
- `dynamic_shared_memory_type (enum)` 动态共享内存类型：设置动态共享内存的实现类型，可选值有 `none`、`mmap`、`sysv`、`windows`、`posix`。
- `min_dynamic_shared_memory (integer)` 最小动态共享内存：动态共享内存的最小值（以 KB 为单位）。
### 磁盘
- `temp_file_limit (integer)` 临时文件限制：临时文件的最大允许大小（以 KB 为单位）。设置为 -1 表示没有限制。
- `max_notify_queue_pages (integer)` 最大通知队列页数：用于存储 `LISTEN`/`NOTIFY` 消息的最大共享内存页数。
### 内核资源使用
- `max_files_per_process (integer)` 每个进程的最大文件数：单个服务器进程允许打开的最大文件数。
### 基于成本的 VACUUM 延迟
- `vacuum_cost_delay (floating point)` VACUUM 成本延迟：VACUUM 操作中的每个成本单位延迟时间（以毫秒为单位）。
- `vacuum_cost_page_hit (integer)` VACUUM 成本页命中：VACUUM 操作中每页命中的成本单位。
- `vacuum_cost_page_miss (integer)` VACUUM 成本页未命中：VACUUM 操作中每页未命中的成本单位。
- `vacuum_cost_page_dirty (integer)` VACUUM 成本页脏：VACUUM 操作中每页脏的成本单位。
- `vacuum_cost_limit (integer)` VACUUM 成本限制：VACUUM 操作在延迟前能累计的最大成本单位。
### 后台写
- `bgwriter_delay (integer)` 后台写入延迟：后台写进程每次写操作之间的延迟时间（以毫秒为单位）。
- `bgwriter_lru_maxpages (integer)` 后台写入 LRU 最大页数：后台写进程每次循环中能写入的最大页数。
- `bgwriter_lru_multiplier (floating point)` 后台写入 LRU 乘数：决定后台写进程的写入速度，影响缓冲区的回收。
- `bgwriter_flush_after (integer)` 后台写入刷新后：后台写进程写入多少页后触发文件系统刷新（以页为单位）。
### 异步表现
- `backend_flush_after (integer)` 后端刷新后：普通后台进程写入多少页后触发文件系统刷新（以页为单位）。
- `effective_io_concurrency (integer)` 有效 IO 并发数：磁盘子系统的并行 I/O 操作数量。
- `maintenance_io_concurrency (integer)` 维护 IO 并发数：维护操作（如 `VACUUM` 和 `CREATE INDEX`）的并行 I/O 操作数量。
- `io_combine_limit (integer)` IO 合并限制：在一个系统调用中最多可以合并的 I/O 操作数。
- `max_worker_processes (integer)` 最大工作进程数：服务器允许的最大后台工作进程数。
- `max_parallel_workers_per_gather (integer)` 每个收集的最大并行工作进程数：单个查询中每个 `Gather` 或 `Gather Merge` 节点的最大并行工作进程数。
- `max_parallel_maintenance_workers (integer)` 最大并行维护工作进程数：维护操作（如 `VACUUM` 和 `CREATE INDEX`）允许的最大并行工作进程数。
- `max_parallel_workers (integer)` 最大并行工作进程数：服务器允许的最大并行工作进程总数。
- `parallel_leader_participation (boolean)` 并行领导者参与：控制并行查询中领导进程是否参与实际的查询工作。
## WAL 参数
### 配置
- `wal_level (enum)` WAL 级别：控制写前日志记录的详细程度。
- `fsync (boolean)` 文件同步：控制是否在每个事务提交时将写操作同步到磁盘。
- `synchronous_commit (enum)` 同步提交：控制事务提交时的同步级别。
- `wal_sync_method (enum)` WAL 同步方法：控制写前日志的同步方法。
- `full_page_writes (boolean)` 完整页面写入：控制在 WAL 中写入页面图像。
- `wal_log_hints (boolean)` WAL 日志提示：控制是否记录数据块的非关键修改。
- `wal_compression (enum)` WAL 压缩：控制是否对 WAL 数据进行压缩。
- `wal_init_zero (boolean)` WAL 初始化为零：控制 WAL 文件初始化时是否填充零。
- `wal_recycle (boolean)` WAL 回收：控制是否回收已用的 WAL 文件。
- `wal_buffers (integer)` WAL 缓冲区：设置 WAL 缓冲区的大小。
- `wal_writer_delay (integer)` WAL 写入延迟：控制 WAL 写入进程的写入间隔时间。
- `wal_writer_flush_after (integer)` WAL 写入刷新后：控制 WAL 写入进程在写入多少字节后触发文件系统刷新。
- `wal_skip_threshold (integer)` WAL 跳过阈值：控制 WAL 写入进程在写入多少字节后跳过刷新。
- `commit_delay (integer)` 提交延迟：控制事务提交时的延迟时间（以微秒为单位）。
- `commit_siblings (integer)` 提交兄弟数：控制在事务提交时考虑的并行事务数量。

### Checkpoints 设置
- `checkpoint_timeout (integer)` 检查点超时：控制检查点的时间间隔。
- `checkpoint_completion_target (floating point)` 检查点完成目标：控制检查点完成时间的目标比例。
- `checkpoint_flush_after (integer)` 检查点刷新后：控制检查点写入多少页后触发文件系统刷新。
- `checkpoint_warning (integer)` 检查点警告：在检查点花费时间过长时发出警告。
- `max_wal_size (integer)` 最大 WAL 大小：控制 WAL 文件的最大允许大小。
- `min_wal_size (integer)` 最小 WAL 大小：控制 WAL 文件的最小保持大小。

### 归档
- `archive_mode (enum)` 归档模式：控制是否启用 WAL 归档。
- `archive_command (string)` 归档命令：控制 WAL 归档的命令。
- `archive_library (string)` 归档库：指定用于归档的库。
- `archive_timeout (integer)` 归档超时：控制在归档前的最大等待时间。

### 还原
- `recovery_prefetch (enum)` 还原预取：控制还原时的数据预取。
- `wal_decode_buffer_size (integer)` WAL 解码缓冲区大小：控制 WAL 解码时的缓冲区大小。

### 归档还原
- `restore_command (string)` 还原命令：控制用于还原归档文件的命令。
- `archive_cleanup_command (string)` 归档清理命令：在还原结束时执行的命令。
- `recovery_end_command (string)` 还原结束命令：在还原结束时执行的命令。

### 还原目标
- `recovery_target = 'immediate'` 还原目标：立即还原到目标状态。
- `recovery_target_name (string)` 还原目标名称：指定还原到的命名恢复点。
- `recovery_target_time (timestamp)` 还原目标时间：指定还原到的时间点。
- `recovery_target_xid (string)` 还原目标 XID：指定还原到的事务 ID。
- `recovery_target_lsn (pg_lsn)` 还原目标 LSN：指定还原到的日志序列号。
- `recovery_target_inclusive (boolean)` 还原目标包含：控制还原目标是否包含目标时间点。
- `recovery_target_timeline (string)` 还原目标时间线：指定还原到的时间线。
- `recovery_target_action (enum)` 还原目标动作：在达到还原目标时执行的动作。

### WAL 汇总
- `summarize_wal (boolean)` WAL 汇总：控制是否生成 WAL 汇总信息。
- `wal_summary_keep_time (integer)` WAL 汇总保持时间：控制 WAL 汇总信息的保持时间。

## Replication
### Sending Servers
- `max_wal_senders (integer)` 最大 WAL 发送进程数：控制可同时运行的 WAL 发送进程的最大数量。
- `max_replication_slots (integer)` 最大复制槽数：控制可用的复制槽的最大数量。
- `wal_keep_size (integer)` 保持 WAL 大小：控制在回收前保留的 WAL 文件的最大大小。
- `max_slot_wal_keep_size (integer)` 最大槽 WAL 保持大小：控制复制槽可保留的 WAL 文件的最大大小。
- `wal_sender_timeout (integer)` WAL 发送超时：控制 WAL 发送进程的超时时间。
- `track_commit_timestamp (boolean)` 跟踪提交时间戳：控制是否跟踪事务的提交时间戳。
- `standby_slot_names (string)` 备用槽名称：指定备用服务器使用的复制槽名称。
### Primary Server
- `synchronous_standby_names (string)` 同步备用名称：指定同步复制备用服务器的名称。
### Standby Servers
- `primary_conninfo (string)` 主服务器连接信息：指定连接到主服务器的连接信息。
- `primary_slot_name (string)` 主槽名称：指定从主服务器获取 WAL 的复制槽名称。
- `hot_standby (boolean)` 热备用：控制是否启用热备用模式。
- `max_standby_archive_delay (integer)` 最大备用存档延迟：控制备用服务器处理存档文件的最大延迟时间。
- `max_standby_streaming_delay (integer)` 最大备用流延迟：控制备用服务器处理流复制的最大延迟时间。
- `wal_receiver_create_temp_slot (boolean)` WAL 接收创建临时槽：控制 WAL 接收器是否创建临时复制槽。
- `wal_receiver_status_interval (integer)` WAL 接收状态间隔：控制 WAL 接收器发送状态更新的间隔时间。
- `hot_standby_feedback (boolean)` 热备用反馈：控制备用服务器是否发送热备用反馈以防止主服务器上的老化进程。
- `wal_receiver_timeout (integer)` WAL 接收超时：控制 WAL 接收器的超时时间。
- `wal_retrieve_retry_interval (integer)` WAL 检索重试间隔：控制 WAL 接收器重试检索 WAL 数据的间隔时间。
- `recovery_min_apply_delay (integer)` 最小恢复应用延迟：控制备用服务器应用恢复数据的最小延迟时间。
- `sync_replication_slots (boolean)` 同步复制槽：控制复制槽是否在同步复制模式下同步。
### Subscribers
- `max_replication_slots (integer)` 最大复制槽数：控制可用的复制槽的最大数量。
- `max_logical_replication_workers (integer)` 最大逻辑复制工作进程数：控制逻辑复制可同时运行的工作进程的最大数量。
- `max_sync_workers_per_subscription (integer)` 每个订阅的最大同步工作进程数：控制每个订阅可同时运行的同步工作进程的最大数量。
- `max_parallel_apply_workers_per_subscription (integer)` 每个订阅的最大并行应用工作进程数：控制每个订阅可同时运行的并行应用工作进程的最大数量。
 
## 查询计划
### Planner Method Configuration
- `enable_async_append (boolean)` 启用异步追加：控制是否启用异步追加扫描。
- `enable_bitmapscan (boolean)` 启用位图扫描：控制是否启用位图扫描。
- `enable_gathermerge (boolean)` 启用聚合合并：控制是否启用聚合合并操作。
- `enable_group_by_reordering (boolean)` 启用分组重排序：控制是否启用分组重排序。
- `enable_hashagg (boolean)` 启用哈希聚合：控制是否启用哈希聚合操作。
- `enable_hashjoin (boolean)` 启用哈希连接：控制是否启用哈希连接操作。
- `enable_incremental_sort (boolean)` 启用增量排序：控制是否启用增量排序。
- `enable_indexscan (boolean)` 启用索引扫描：控制是否启用索引扫描。
- `enable_indexonlyscan (boolean)` 启用仅索引扫描：控制是否启用仅索引扫描。
- `enable_material (boolean)` 启用物化：控制是否启用物化操作。
- `enable_memoize (boolean)` 启用记忆化：控制是否启用记忆化操作。
- `enable_mergejoin (boolean)` 启用合并连接：控制是否启用合并连接操作。
- `enable_nestloop (boolean)` 启用嵌套循环：控制是否启用嵌套循环连接。
- `enable_parallel_append (boolean)` 启用并行追加：控制是否启用并行追加扫描。
- `enable_parallel_hash (boolean)` 启用并行哈希：控制是否启用并行哈希连接。
- `enable_partition_pruning (boolean)` 启用分区修剪：控制是否启用分区修剪。
- `enable_partitionwise_join (boolean)` 启用分区连接：控制是否启用分区连接。
- `enable_partitionwise_aggregate (boolean)` 启用分区聚合：控制是否启用分区聚合。
- `enable_presorted_aggregate (boolean)` 启用预排序聚合：控制是否启用预排序聚合。
- `enable_seqscan (boolean)` 启用顺序扫描：控制是否启用顺序扫描。
- `enable_sort (boolean)` 启用排序：控制是否启用排序操作。
- `enable_tidscan (boolean)` 启用 TID 扫描：控制是否启用 TID 扫描。
### Planner Cost Constants
- `seq_page_cost (floating point)` 顺序页成本：设置顺序扫描每页的成本。
- `random_page_cost (floating point)` 随机页成本：设置随机扫描每页的成本。
- `cpu_tuple_cost (floating point)` CPU 元组成本：设置处理一个元组的 CPU 成本。
- `cpu_index_tuple_cost (floating point)` CPU 索引元组成本：设置处理一个索引元组的 CPU 成本。
- `cpu_operator_cost (floating point)` CPU 操作成本：设置执行一个操作的 CPU 成本。
- `parallel_setup_cost (floating point)` 并行设置成本：设置并行查询的初始化成本。
- `parallel_tuple_cost (floating point)` 并行元组成本：设置处理一个并行元组的成本。
- `min_parallel_table_scan_size (integer)` 最小并行表扫描大小：设置允许并行扫描的表的最小大小。
- `min_parallel_index_scan_size (integer)` 最小并行索引扫描大小：设置允许并行扫描的索引的最小大小。
- `effective_cache_size (integer)` 有效缓存大小：设置查询规划器估算的缓存大小。
- `jit_above_cost (floating point)` JIT 启用成本：设置启用 JIT 编译的成本阈值。
- `jit_inline_above_cost (floating point)` JIT 内联启用成本：设置启用 JIT 内联的成本阈值。
- `jit_optimize_above_cost (floating point)` JIT 优化启用成本：设置启用 JIT 优化的成本阈值。
### Genetic Query Optimizer
- `geqo (boolean)` 启用 GEQO：控制是否启用遗传查询优化器。
- `geqo_threshold (integer)` GEQO 阈值：设置启用 GEQO 的连接数阈值。
- `geqo_effort (integer)` GEQO 努力：设置 GEQO 的优化努力级别。
- `geqo_pool_size (integer)` GEQO 池大小：设置 GEQO 使用的种群大小。
- `geqo_generations (integer)` GEQO 代数：设置 GEQO 的代数。
- `geqo_selection_bias (floating point)` GEQO 选择偏差：设置 GEQO 的选择偏差。
- `geqo_seed (floating point)` GEQO 种子：设置 GEQO 的随机种子。
### Other Planner Options
- `default_statistics_target (integer)` 默认统计目标：设置默认的统计数据收集目标。
- `constraint_exclusion (enum)` 约束排除：控制查询规划器是否使用约束排除。
- `cursor_tuple_fraction (floating point)` 游标元组比例：设置游标查询返回元组的比例。
- `from_collapse_limit (integer)` FROM 折叠限制：设置查询规划器折叠 FROM 项的最大数量。
- `jit (boolean)` 启用 JIT：控制是否启用即时编译 (JIT)。
- `join_collapse_limit (integer)` 连接折叠限制：设置查询规划器折叠连接项的最大数量。
- `plan_cache_mode (enum)` 计划缓存模式：控制查询计划的缓存模式。
- `recursive_worktable_factor (floating point)` 递归工作表因子：设置递归工作表的因子。

## 错误报告和日志
### 日志记录位置
- log_destination (string)  # 日志的目标位置
- logging_collector (boolean)  # 是否启用日志收集器
- log_directory (string)  # 日志文件所在的目录
- log_filename (string)  # 日志文件的名称
- log_file_mode (integer)  # 日志文件的权限模式
- log_rotation_age (integer)  # 日志文件轮转的时间间隔（以分钟为单位）
- log_rotation_size (integer)  # 日志文件轮转的大小（以字节为单位）
- log_truncate_on_rotation (boolean)  # 日志文件轮转时是否截断旧文件
- syslog_facility (enum)  # syslog 设施
- syslog_ident (string)  # syslog 标识符
- syslog_sequence_numbers (boolean)  # 是否在 syslog 中包含序列号
- syslog_split_messages (boolean)  # 是否在 syslog 中拆分消息
- event_source (string)  # 事件源名称

### 日志记录时间
- log_min_messages (enum)  # 最低日志记录级别
- log_min_error_statement (enum)  # 记录错误 SQL 语句的最低级别
- log_min_duration_statement (integer)  # 记录慢查询的最低持续时间（以毫秒为单位）
- log_min_duration_sample (integer)  # 记录慢查询采样的最低持续时间（以毫秒为单位）
- log_statement_sample_rate (floating point)  # 记录 SQL 语句采样的比率
- log_transaction_sample_rate (floating point)  # 记录事务采样的比率
- log_startup_progress_interval (integer)  # 启动过程中记录进度的时间间隔（以毫秒为单位）

### 日志记录内容
- application_name (string)  # 应用程序名称
- debug_print_parse (boolean)  # 是否记录解析树
- debug_print_rewritten (boolean)  # 是否记录重写的查询树
- debug_print_plan (boolean)  # 是否记录执行计划
- debug_pretty_print (boolean)  # 是否美化调试输出
- log_autovacuum_min_duration (integer)  # 自动清理的最小持续时间（以毫秒为单位）
- log_checkpoints (boolean)  # 是否记录检查点信息
- log_connections (boolean)  # 是否记录新连接信息
- log_disconnections (boolean)  # 是否记录断开连接信息
- log_duration (boolean)  # 是否记录 SQL 语句的执行时间
- log_error_verbosity (enum)  # 错误日志的详细程度
- log_hostname (boolean)  # 是否记录客户端主机名
- log_line_prefix (string)  # 日志行前缀
- log_lock_waits (boolean)  # 是否记录锁等待事件
- log_recovery_conflict_waits (boolean)  # 是否记录恢复冲突等待事件
- log_parameter_max_length (integer)  # 记录参数的最大长度
- log_parameter_max_length_on_error (integer)  # 在错误时记录参数的最大长度
- log_statement (enum)  # 记录哪些 SQL 语句
- log_replication_commands (boolean)  # 是否记录复制命令
- log_temp_files (integer)  # 记录临时文件的最小大小（以字节为单位）
- log_timezone (string)  # 日志中记录的时区

### 使用 CSV 格式日志输出
### 使用 JSON 格式日志输出
### 进程标题
- cluster_name (string)  # 集群名称
- update_process_title (boolean)  # 是否更新进程标题

## 运行时统计
### 累积查询和索引统计
- track_activities (boolean)  # 是否跟踪活动
- track_activity_query_size (integer)  # 活动查询的最大大小（以字节为单位）
- track_counts (boolean)  # 是否跟踪计数统计信息
- track_io_timing (boolean)  # 是否跟踪 I/O 计时信息
- track_wal_io_timing (boolean)  # 是否跟踪 WAL I/O 计时信息
- track_functions (enum)  # 是否跟踪函数调用
- stats_fetch_consistency (enum)  # 获取统计信息的一致性

### 统计监控
- compute_query_id (enum)  # 是否计算查询 ID
- log_statement_stats (boolean)  # 是否记录语句统计信息
- log_parser_stats (boolean)  # 是否记录解析器统计信息
- log_planner_stats (boolean)  # 是否记录计划器统计信息
- log_executor_stats (boolean)  # 是否记录执行器统计信息

## 自动清理
- autovacuum (boolean)  # 是否启用自动清理
- autovacuum_max_workers (integer)  # 自动清理的最大工作进程数
- autovacuum_naptime (integer)  # 自动清理的休眠时间（秒）
- autovacuum_vacuum_threshold (integer)  # 自动清理的 VACUUM 阈值
- autovacuum_vacuum_insert_threshold (integer)  # 自动清理的插入 VACUUM 阈值
- autovacuum_analyze_threshold (integer)  # 自动清理的 ANALYZE 阈值
- autovacuum_vacuum_scale_factor (floating point)  # 自动清理的 VACUUM 比例因子
- autovacuum_vacuum_insert_scale_factor (floating point)  # 自动清理的插入 VACUUM 比例因子
- autovacuum_analyze_scale_factor (floating point)  # 自动清理的 ANALYZE 比例因子
- autovacuum_freeze_max_age (integer)  # 自动清理的冻结最大年龄
- autovacuum_multixact_freeze_max_age (integer)  # 自动清理的多事务冻结最大年龄
- autovacuum_vacuum_cost_delay (floating point)  # 自动清理的 VACUUM 成本延迟（毫秒）
- autovacuum_vacuum_cost_limit (integer)  # 自动清理的 VACUUM 成本限制

以下是带有中文注释的 PostgreSQL 客户端连接默认参数：


## 客户端连接默认参数
### 语句行为
- client_min_messages (enum)  # 客户端最小消息级别
- search_path (string)  # 搜索路径
- row_security (boolean)  # 行级安全性
- default_table_access_method (string)  # 默认表访问方法
- default_tablespace (string)  # 默认表空间
- default_toast_compression (enum)  # 默认 TOAST 压缩方法
- temp_tablespaces (string)  # 临时表空间
- check_function_bodies (boolean)  # 检查函数体
- default_transaction_isolation (enum)  # 默认事务隔离级别
- default_transaction_read_only (boolean)  # 默认事务只读
- default_transaction_deferrable (boolean)  # 默认事务可推迟
- transaction_isolation (enum)  # 事务隔离级别
- transaction_read_only (boolean)  # 事务只读
- transaction_deferrable (boolean)  # 事务可推迟
- session_replication_role (enum)  # 会话复制角色
- statement_timeout (integer)  # 语句超时时间（毫秒）
- transaction_timeout (integer)  # 事务超时时间（毫秒）
- lock_timeout (integer)  # 锁超时时间（毫秒）
- idle_in_transaction_session_timeout (integer)  # 事务空闲会话超时时间（毫秒）
- idle_session_timeout (integer)  # 空闲会话超时时间（毫秒）
- vacuum_freeze_table_age (integer)  # 真空冻结表年龄
- vacuum_freeze_min_age (integer)  # 真空冻结最小年龄
- vacuum_failsafe_age (integer)  # 真空故障保护年龄
- vacuum_multixact_freeze_table_age (integer)  # 多事务真空冻结表年龄
- vacuum_multixact_freeze_min_age (integer)  # 多事务真空冻结最小年龄
- vacuum_multixact_failsafe_age (integer)  # 多事务真空故障保护年龄
- bytea_output (enum)  # bytea 输出格式
- xmlbinary (enum)  # XML 二进制数据处理方式
- xmloption (enum)  # XML 选项
- gin_pending_list_limit (integer)  # GIN 索引待处理列表限制
- createrole_self_grant (string)  # 授予创建角色的权限
- event_triggers (boolean)  # 事件触发器

### 地区和格式化
- DateStyle (string)  # 日期样式
- IntervalStyle (enum)  # 间隔样式
- TimeZone (string)  # 时区
- timezone_abbreviations (string)  # 时区缩写
- extra_float_digits (integer)  # 额外浮点数字位数
- client_encoding (string)  # 客户端编码
- lc_messages (string)  # 本地化消息
- lc_monetary (string)  # 本地化货币
- lc_numeric (string)  # 本地化数字
- lc_time (string)  # 本地化时间
- icu_validation_level (enum)  # ICU 验证级别
- default_text_search_config (string)  # 默认文本搜索配置

### 共享库预加载
- local_preload_libraries (string)  # 本地预加载库
- session_preload_libraries (string)  # 会话预加载库
- shared_preload_libraries (string)  # 共享预加载库
- jit_provider (string)  # JIT 提供者

### 其他默认值
- dynamic_library_path (string)  # 动态库路径
- gin_fuzzy_search_limit (integer)  # GIN 模糊搜索限制

## 锁管理
- deadlock_timeout (integer)  # 死锁超时时间
- max_locks_per_transaction (integer)  # 每个事务的最大锁数
- max_pred_locks_per_transaction (integer)  # 每个事务的最大预测锁数
- max_pred_locks_per_relation (integer)  # 每个关系的最大预测锁数
- max_pred_locks_per_page (integer)  # 每个页面的最大预测锁数

## 版本和平台兼容性
### 以前的 PostgreSQL 版本
- array_nulls (boolean)  # 数组是否允许 NULL 值
- backslash_quote (enum)  # 反斜杠引用
- escape_string_warning (boolean)  # 转义字符串警告
- lo_compat_privileges (boolean)  # 大对象兼容权限
- quote_all_identifiers (boolean)  # 引用所有标识符
- standard_conforming_strings (boolean)  # 标准符合字符串
- synchronize_seqscans (boolean)  # 同步顺序扫描

### 平台和客户端兼容性
- transform_null_equals (boolean)  # 将 NULL 等号转换
- allow_alter_system (boolean)  # 允许系统修改

## 错误处理
- exit_on_error (boolean)  # 错误退出
- restart_after_crash (boolean)  # 崩溃后重启
- data_sync_retry (boolean)  # 数据同步重试
- recovery_init_sync_method (enum)  # 恢复初始化同步方法

## 预设选项
- block_size (integer)  # 块大小
- data_checksums (boolean)  # 数据校验和
- data_directory_mode (integer)  # 数据目录模式
- debug_assertions (boolean)  # 调试断言
- huge_pages_status (enum)  # 大页状态
- integer_datetimes (boolean)  # 整数日期时间
- in_hot_standby (boolean)  # 热备份状态
- max_function_args (integer)  # 最大函数参数数
- max_identifier_length (integer)  # 最大标识符长度
- max_index_keys (integer)  # 最大索引键数
- segment_size (integer)  # 段大小
- server_encoding (string)  # 服务器编码
- server_version (string)  # 服务器版本
- server_version_num (integer)  # 服务器版本号
- shared_memory_size (integer)  # 共享内存大小
- shared_memory_size_in_huge_pages (integer)  # 共享内存大小（大页）
- ssl_library (string)  # SSL 库
- wal_block_size (integer)  # WAL 块大小
- wal_segment_size (integer)  # WAL 段大小


## 自定义选项
## 开发者选项
- allow_in_place_tablespaces (boolean)  # 允许就地表空间
- allow_system_table_mods (boolean)  # 允许系统表修改
- backtrace_functions (string)  # 回溯函数
- debug_discard_caches (integer)  # 调试丢弃缓存
- debug_io_direct (string)  # 调试直接 IO
- debug_parallel_query (enum)  # 调试并行查询
- ignore_system_indexes (boolean)  # 忽略系统索引
- post_auth_delay (integer)  # 身份验证后延迟
- pre_auth_delay (integer)  # 身份验证前延迟
- trace_notify (boolean)  # 跟踪通知
- trace_sort (boolean)  # 跟踪排序
- trace_locks (boolean)  # 跟踪锁
- trace_lwlocks (boolean)  # 跟踪轻量级锁
- trace_userlocks (boolean)  # 跟踪用户锁
- trace_lock_oidmin (integer)  # 跟踪锁的 OID 最小值
- trace_lock_table (integer)  # 跟踪锁表
- debug_deadlocks (boolean)  # 调试死锁
- log_btree_build_stats (boolean)  # 记录 B 树构建统计
- wal_consistency_checking (string)  # WAL 一致性检查
- wal_debug (boolean)  # WAL 调试
- ignore_checksum_failure (boolean)  # 忽略校验和失败
- zero_damaged_pages (boolean)  # 清零损坏的页面
- ignore_invalid_pages (boolean)  # 忽略无效页面
- jit_debugging_support (boolean)  # JIT 调试支持
- jit_dump_bitcode (boolean)  # JIT 转储字节码
- jit_expressions (boolean)  # JIT 表达式
- jit_profiling_support (boolean)  # JIT 性能分析支持
- jit_tuple_deforming (boolean)  # JIT 元组变形
- remove_temp_files_after_crash (boolean)  # 崩溃后删除临时文件
- send_abort_for_crash (boolean)  # 崩溃时发送中止
- send_abort_for_kill (boolean)  # 终止时发送中止
- debug_logical_replication_streaming (enum)  # 调试逻辑复制流
## 简写选项

# 客户端认证
[Chapter 20. Client Authentication](https://www.postgresql.org/docs/17/client-authentication.html)

# 数据库角色
## Database Roles
```sql
CREATE ROLE name;
DROP ROLE name;

createuser name
dropuser name

SELECT rolname FROM pg_roles;

SELECT rolname FROM pg_roles WHERE rolcanlogin;

\du
```
## Role Attributes
- login privilege
- superuser status
- database creation
- role creation
- initiating replication
- password
- inheritance of privileges
- bypassing row-level security
- connection limit
## Role Membership
```sql
GRANT group_role TO role1, ... ;
REVOKE group_role FROM role1, ... ;

CREATE ROLE joe LOGIN;
CREATE ROLE admin;
CREATE ROLE wheel;
CREATE ROLE island;
GRANT admin TO joe WITH INHERIT TRUE;   -- 将 admin 角色授予 joe 用户，并且设置 INHERIT 为 TRUE
GRANT wheel TO admin WITH INHERIT FALSE;
GRANT island TO joe WITH INHERIT TRUE, SET FALSE;   --将 island 角色授予 joe 用户，并且设置 INHERIT 为 TRUE 和 SET 为 FALSE。这意味着 joe 用户不能显式地设置自己的角色为 island。

SET ROLE admin;

SET ROLE wheel;

SET ROLE joe;
SET ROLE NONE;
RESET ROLE;
```
## Dropping Roles
```sql
ALTER TABLE bobs_table OWNER TO alice;

REASSIGN OWNED BY doomed_role TO successor_role;
DROP OWNED BY doomed_role;
-- repeat the above commands in each database of the cluster
DROP ROLE doomed_role;
```
## Predefined Roles
| Role                      | Allowed Access   |
|---------------------------|---------------------|
| pg_read_all_data          | Read all data (tables, views, sequences), as if having SELECT rights on those objects, and USAGE rights on all schemas, even without having it explicitly. This role does not have the role attribute BYPASSRLS set. If RLS is being used, an administrator may wish to set BYPASSRLS on roles which this role is GRANTed to. |
| pg_write_all_data         | Write all data (tables, views, sequences), as if having INSERT, UPDATE, and DELETE rights on those objects, and USAGE rights on all schemas, even without having it explicitly. This role does not have the role attribute BYPASSRLS set. If RLS is being used, an administrator may wish to set BYPASSRLS on roles which this role is GRANTed to. |
| pg_read_all_settings      | Read all configuration variables, even those normally visible only to superusers.              |
| pg_read_all_stats         | Read all pg_stat_* views and use various statistics related extensions, even those normally visible only to superusers.|
| pg_stat_scan_tables       | Execute monitoring functions that may take ACCESS SHARE locks on tables, potentially for a long |
| pg_monitor                | Read/execute various monitoring views and functions. This role is a member of pg_read_all_settings, pg_read_all_stats and pg_stat_scan_tables.|
| pg_database_owner         | None. Membership consists, implicitly, of the current database owner.|
| pg_signal_backend         | Signal another backend to cancel a query or terminate its session.|
| pg_read_server_files      | Allow reading files from any location the database can access on the server with COPY and other file-access |
| pg_write_server_files     | Allow writing to files in any location the database can access on the server with COPY and other file-access functions.|
| pg_execute_server_program | Allow executing programs on the database server as the user the database runs as with COPY and other functions which allow executing a server-side program.|
| pg_checkpoint             | Allow executing the CHECKPOINT command.|
| pg_maintain               | Allow executing VACUUM, ANALYZE, CLUSTER, REFRESH MATERIALIZED VIEW, REINDEX, and LOCK TABLE on all relations, as if having MAINTAIN rights on those objects, even without having it explicitly.|
| pg_use_reserved_connections | Allow use of connection slots reserved via reserved_connections.|
| pg_create_subscription    | Allow users with CREATE permission on the database to issue CREATE SUBSCRIPTION.|

## Function Security

# 管理 Databases
## Overview
```sql
SELECT datname FROM pg_database;
```
## Creating a Database
```sql
CREATE DATABASE name;
createdb dbname
CREATE DATABASE dbname OWNER rolename;
createdb -O rolename dbname
```
## Template Databases
```sql
CREATE DATABASE dbname TEMPLATE template0;
createdb -T template0 dbname
```
## Database Configuration
```sql
ALTER DATABASE mydb SET geqo TO off;
```
## Destroying a Database
```sql
DROP DATABASE name;
dropdb dbname
```
## Tablespaces
```sql
CREATE TABLESPACE fastspace LOCATION '/ssd1/postgresql/data';
CREATE TABLE foo(i int) TABLESPACE space1;
SET default_tablespace = space1;
CREATE TABLE foo(i int);
SELECT spcname FROM pg_tablespace;
```

# Localization
## Locale Support
https://www.postgresql.org/docs/17/locale.html

    23.1.1. Overview
    23.1.2. Behavior
    23.1.3. Selecting Locales
    23.1.4. Locale Providers
    23.1.5. ICU Locales
    23.1.6. Problems

##  Collation Support
https://www.postgresql.org/docs/17/collation.html

    23.2.1. Concepts
    23.2.2. Managing Collations
    23.2.3. ICU Custom Collations

## Character Set Support
https://www.postgresql.org/docs/17/multibyte.html

    23.3.1. Supported Character Sets
    23.3.2. Setting the Character Set
    23.3.3. Automatic Character Set Conversion Between Server and Client
    23.3.4. Available Character Set Conversions
    23.3.5. Further Reading

# 日常数据库维护任务
https://www.postgresql.org/docs/17/maintenance.html

24.1. Routine Vacuuming

    24.1.1. Vacuuming Basics
    24.1.2. Recovering Disk Space
    24.1.3. Updating Planner Statistics
    24.1.4. Updating the Visibility Map
    24.1.5. Preventing Transaction ID Wraparound Failures
    24.1.6. The Autovacuum Daemon
```
PostgreSQL's VACUUM command has to process each table on a regular basis for several reasons:

    To recover or reuse disk space occupied by updated or deleted rows.
    To update data statistics used by the PostgreSQL query planner.
    To update the visibility map, which speeds up index-only scans.
    To protect against loss of very old data due to transaction ID wraparound or multixact ID wraparound.

Each of these reasons dictates performing VACUUM operations of varying frequency and scope, as explained in the following subsections.

There are two variants of VACUUM: standard VACUUM and VACUUM FULL. VACUUM FULL can reclaim more disk space but runs much more slowly. Also, the standard form of VACUUM can run in parallel with production database operations. (Commands such as SELECT, INSERT, UPDATE, and DELETE will continue to function normally, though you will not be able to modify the definition of a table with commands such as ALTER TABLE while it is being vacuumed.) VACUUM FULL requires an ACCESS EXCLUSIVE lock on the table it is working on, and therefore cannot be done in parallel with other use of the table. Generally, therefore, administrators should strive to use standard VACUUM and avoid VACUUM FULL.

VACUUM creates a substantial amount of I/O traffic, which can cause poor performance for other active sessions. There are configuration parameters that can be adjusted to reduce the performance impact of background vacuuming — see 



以下是翻译：

---

PostgreSQL 的 VACUUM 命令必须定期处理每个表，原因有以下几点：

- 回收或重用被更新或删除的行占用的磁盘空间。
- 更新 PostgreSQL 查询计划器使用的数据统计信息。
- 更新可见性图，这有助于加快仅索引扫描的速度。
- 防止由于事务 ID 或多事务 ID 回绕而导致非常旧的数据丢失。

每个原因决定了以不同的频率和范围执行 VACUUM 操作，具体在以下小节中解释。

VACUUM 有两种变体：标准 VACUUM 和 VACUUM FULL。VACUUM FULL 可以回收更多的磁盘空间，但运行速度要慢得多。此外，标准形式的 VACUUM 可以与生产数据库操作并行运行。（SELECT、INSERT、UPDATE 和 DELETE 等命令将继续正常运行，但在进行 VACUUM 操作时，您将无法使用 ALTER TABLE 等命令修改表的定义。）VACUUM FULL 需要在它正在处理的表上获取一个访问独占锁，因此无法与其他对该表的使用并行进行。因此，管理员通常应努力使用标准 VACUUM，避免使用 VACUUM FULL。

VACUUM 会产生大量的 I/O 流量，这可能会导致其他活动会话的性能下降。有一些配置参数可以调整，以减少后台清理对性能的影响——请参见相关章节。

---
```
24.2. Routine Reindexing
24.3. Log File Maintenance


# Chapter 25. Backup and Restore
## 25.1. SQL Dump

    25.1.1. Restoring the Dump
    25.1.2. Using pg_dumpall
    25.1.3. Handling Large Databases

## 25.2. File System Level Backup
## 25.3. Continuous Archiving and Point-in-Time Recovery (PITR)
    25.3.1. Setting Up WAL Archiving
    25.3.2. Making a Base Backup
    25.3.3. Making an Incremental Backup
    25.3.4. Making a Base Backup Using the Low Level API
    25.3.5. Recovering Using a Continuous Archive Backup
    25.3.6. Timelines
    25.3.7. Tips and Examples
    25.3.8. Caveats

# 
Chapter 26. High Availability, Load Balancing, and Replication

Table of Contents

26.1. Comparison of Different Solutions
26.2. Log-Shipping Standby Servers

    26.2.1. Planning
    26.2.2. Standby Server Operation
    26.2.3. Preparing the Primary for Standby Servers
    26.2.4. Setting Up a Standby Server
```sql
primary_conninfo = 'host=192.168.1.50 port=5432 user=foo password=foopass options=''-c wal_sender_timeout=5000'''
restore_command = 'cp /path/to/archive/%f %p'
archive_cleanup_command = 'pg_archivecleanup /path/to/archive %r'
```
    26.2.5. Streaming Replication
    26.2.6. Replication Slots
```sql
You can create a replication slot like this:

postgres=# SELECT * FROM pg_create_physical_replication_slot('node_a_slot');
  slot_name  | lsn
-------------+-----
 node_a_slot |

postgres=# SELECT slot_name, slot_type, active FROM pg_replication_slots;
  slot_name  | slot_type | active
-------------+-----------+--------
 node_a_slot | physical  | f
(1 row)

To configure the standby to use this slot, primary_slot_name should be configured on the standby. Here is a simple example:

primary_conninfo = 'host=192.168.1.50 port=5432 user=foo password=foopass'
primary_slot_name = 'node_a_slot'
```
    26.2.7. Cascading Replication
    26.2.8. Synchronous Replication
    26.2.9. Continuous Archiving in Standby

26.3. Failover
26.4. Hot Standby

    26.4.1. User's Overview
    26.4.2. Handling Query Conflicts
    26.4.3. Administrator's Overview
    26.4.4. Hot Standby Parameter Reference
    26.4.5. Caveats

# 
Chapter 27. Monitoring Database Activity

Table of Contents

27.1. Standard Unix Tools
27.2. The Cumulative Statistics System

    27.2.1. Statistics Collection Configuration
    27.2.2. Viewing Statistics
    27.2.3. pg_stat_activity
    27.2.4. pg_stat_replication
    27.2.5. pg_stat_replication_slots
    27.2.6. pg_stat_wal_receiver
    27.2.7. pg_stat_recovery_prefetch
    27.2.8. pg_stat_subscription
    27.2.9. pg_stat_subscription_stats
    27.2.10. pg_stat_ssl
    27.2.11. pg_stat_gssapi
    27.2.12. pg_stat_archiver
    27.2.13. pg_stat_io
    27.2.14. pg_stat_bgwriter
    27.2.15. pg_stat_checkpointer
    27.2.16. pg_stat_wal
    27.2.17. pg_stat_database
    27.2.18. pg_stat_database_conflicts
    27.2.19. pg_stat_all_tables
    27.2.20. pg_stat_all_indexes
    27.2.21. pg_statio_all_tables
    27.2.22. pg_statio_all_indexes
    27.2.23. pg_statio_all_sequences
    27.2.24. pg_stat_user_functions
    27.2.25. pg_stat_slru
    27.2.26. Statistics Functions

27.3. Viewing Locks
27.4. Progress Reporting

    27.4.1. ANALYZE Progress Reporting
    27.4.2. CLUSTER Progress Reporting
    27.4.3. COPY Progress Reporting
    27.4.4. CREATE INDEX Progress Reporting
    27.4.5. VACUUM Progress Reporting
    27.4.6. Base Backup Progress Reporting

27.5. Dynamic Tracing

    27.5.1. Compiling for Dynamic Tracing
    27.5.2. Built-in Probes
    27.5.3. Using Probes
    27.5.4. Defining New Probes

27.6. Monitoring Disk Usage

    27.6.1. Determining Disk Usage
    27.6.2. Disk Full Failure



# PostgreSQL 内核

## 50.1 查询的路径

这里我们简要概述了查询必须经过的各个阶段以获得结果。

1. 必须建立从应用程序到 PostgreSQL 服务器的连接。应用程序将查询传输到服务器，并等待接收服务器发回的结果。

2. 解析阶段检查应用程序传输的查询语法是否正确，并创建查询树。

3. 使用启发式规则(放在 system catalogs 中)重写查询树。。

4. 重写系统的一个应用是在实现视图时。每当对视图（即虚拟表）进行查询时，重写系统将用户的查询重写为访问视图定义中给出的基表的查询。

5. 计划器/优化器接收（重写的）查询树并创建一个查询计划，该计划将作为执行器的输入。

6. 它首先创建所有可能导致相同结果的路径。例如，如果要扫描的关系上有一个索引，则有两种路径可以进行扫描。一种可能性是简单的顺序扫描，另一种可能性是使用索引。接下来，估算每条路径的执行成本，并选择最便宜的路径。最便宜的路径被扩展为执行器可以使用的完整计划。

7. 执行器递归地遍历计划树，并以计划表示的方式检索行。执行器在扫描关系时利用存储系统，执行排序和连接，评估条件，最终返回派生的行。

## 50.2. 如何建立连接

PostgreSQL 实现了“每用户进程”的客户端/服务器模型。在这个模型中，每个客户端进程连接到一个后端进程。由于我们事先不知道将会有多少连接，所以我们必须使用一个“监督进程”，每次请求连接时都会生成一个新的后端进程。这个监督进程被称为 postmaster，它监听指定的 TCP/IP 端口以接收传入的连接。每当它检测到连接请求时，就会生成一个新的后端进程。这些后端进程使用信号量和共享内存与彼此及实例的其他进程通信，以确保在并发数据访问中数据的完整性。

客户端进程可以是任何理解第53章描述的 PostgreSQL 协议的程序。许多客户端基于 C 语言库 libpq，但也存在几个独立实现的协议，如 Java JDBC 驱动程序。

一旦建立连接，客户端进程可以向其连接的后端进程发送查询。查询以纯文本形式传输，即客户端没有进行解析。后端进程解析查询，创建执行计划，执行计划，并通过已建立的连接将检索到的行返回给客户端。

## 50.3. 解析阶段

解析阶段由两个部分组成：

1. 由 Unix 工具 bison 和 flex 构建的 gram.y 和 scan.l 中定义的解析器。
2. 转换过程对解析器返回的数据结构进行修改和增强。

### 50.3.1. 解析器

解析器必须检查查询字符串（以纯文本形式传输）的语法是否有效。如果语法正确，则生成解析树并返回；否则返回错误。解析器和词法分析器是使用知名的 Unix 工具 bison 和 flex 实现的。

词法分析器在文件 scan.l 中定义，负责识别标识符、SQL 关键字等。对于找到的每个关键字或标识符，生成一个标记并传递给解析器。

解析器在文件 gram.y 中定义，由一组语法规则和每当规则触发时执行的动作组成。动作代码（实际上是 C 代码）用于构建解析树。

使用 flex 程序将文件 scan.l 转换为 C 源文件 scan.c，使用 bison 将 gram.y 转换为 gram.c。在这些转换完成后，可以使用普通的 C 编译器创建解析器。不要对生成的 C 文件进行任何更改，因为它们会在下次调用 flex 或 bison 时被覆盖。

注意：提到的这些转换和编译通常使用 PostgreSQL 源代码发行版附带的 makefile 自动完成。

对 bison 或 gram.y 中给出的语法规则进行详细描述超出了本手册的范围。有许多书籍和文档处理 flex 和 bison。在开始研究 gram.y 中的语法之前，你应该熟悉 bison，否则你将无法理解那里发生的事情。

### 50.3.2. 转换过程

解析阶段仅使用有关 SQL 句法结构的固定规则创建解析树。它不在系统目录中进行任何查找，因此无法理解请求操作的详细语义。解析器完成后，转换过程将解析器返回的树作为输入，并进行语义解释，以了解查询引用了哪些表、函数和操作符。构建来表示此信息的数据结构称为查询树。

将原始解析与语义分析分开的原因是，系统目录查找只能在事务中进行，而我们不希望在接收到查询字符串后立即启动事务。原始解析阶段足以识别事务控制命令（BEGIN、ROLLBACK 等），这些命令可以在没有进一步分析的情况下正确执行。一旦我们知道我们正在处理实际查询（例如 SELECT 或 UPDATE），如果我们还没有处于事务中，则可以启动事务。只有这样才能调用转换过程。

转换过程创建的查询树在大多数地方在结构上类似于原始解析树，但在细节上有许多不同。例如，解析树中的 FuncCall 节点表示在句法上看起来像函数调用的内容。根据引用名称是普通函数还是聚合函数，这可能会转换为 FuncExpr 或 Aggref 节点。此外，有关列和表达式结果的实际数据类型的信息也会添加到查询树中。

## 50.4. PostgreSQL 规则系统

PostgreSQL 支持一个强大的规则系统，用于定义视图和解决视图更新的歧义。最初，PostgreSQL 规则系统由两种实现方式组成：

1. 第一种通过行级处理工作，深度实现于执行器中。每当访问单独的行时，都会调用规则系统。该实现于 1995 年被移除，当时伯克利 Postgres 项目的最后一个官方版本被转换为 Postgres95。

2. 第二种规则系统的实现方式是一种称为查询重写的技术。重写系统是存在于解析器阶段和计划/优化器之间的一个模块。这种技术至今仍在实现。

第 39 章详细讨论了查询重写器，因此这里无需展开。我们只需指出，重写器的输入和输出都是查询树，也就是说，树的表示方式或语义细节水平没有变化。重写可以被认为是一种宏扩展形式。

## 50.5. 计划器/优化器

计划器/优化器的任务是创建一个最优执行计划。给定的 SQL 查询（即查询树）实际上可以通过多种不同的方式执行，每种方式都会产生相同的结果集。如果计算上可行，查询优化器会检查每个可能的执行计划，最终选择预期运行最快的执行计划。

**注意**
```
在某些情况下，检查查询可以执行的每一种方式会花费过多的时间和内存。特别是，当执行涉及大量连接操作的查询时会发生这种情况。为了在合理的时间内确定合理的（不一定是最优的）查询计划，当连接数超过阈值时，PostgreSQL 使用遗传查询优化器（参见第 60 章）。

计划器的搜索过程实际上处理的是称为路径的数据结构，这些路径只是计划的简化表示，只包含计划器做出决策所需的信息。在确定最便宜的路径后，会构建一个完整的计划树传递给执行器。这表示了执行器可以运行的详细执行计划。在本节的其余部分，我们将忽略路径和计划之间的区别。
```
### 50.5.1. 生成可能的计划

计划器/优化器首先生成扫描查询中每个单独关系（表）的计划。可能的计划取决于每个关系上可用的索引。总是可以对关系执行顺序扫描，因此总是创建顺序扫描计划。假设在关系上定义了一个索引（例如 B-tree 索引）并且查询包含关系.attribute OPR 常量的限制条件。如果关系.attribute 恰好与 B-tree 索引的键匹配，并且 OPR 是索引的操作符类中列出的操作符之一，则会创建另一个使用 B-tree 索引扫描关系的计划。如果存在进一步的索引并且查询中的限制条件恰好匹配索引的键，则会考虑进一步的计划。对于具有可以匹配查询的 ORDER BY 子句（如果有的话）或可能对合并连接有用的排序顺序的索引，也会生成索引扫描计划。

如果查询需要连接两个或多个关系，则在找到扫描单个关系的所有可行计划后，会考虑连接关系的计划。三种可用的连接策略是：

- 嵌套循环连接：对于左关系中找到的每一行，右关系会被扫描一次。这种策略易于实现，但可能非常耗时。（但是，如果可以使用索引扫描扫描右关系，这可能是一个好的策略。可以使用左关系当前行的值作为右关系索引扫描的键。）

- merge join：在连接开始之前，每个关系都会根据连接属性进行排序。然后并行扫描两个关系，并将匹配的行组合形成连接行。这种连接方式很有吸引力，因为每个关系只需扫描一次。所需的排序可以通过显式排序步骤实现，也可以通过使用连接键上的索引按适当顺序扫描关系来实现。

- 哈希连接：首先扫描右关系并将其加载到哈希表中，使用其连接属性作为哈希键。接下来扫描左关系，并使用找到的每一行的适当值作为哈希键查找表中的匹配行。

当查询涉及两个以上的关系时，最终结果必须通过一棵连接步骤树构建，每个步骤有两个输入。计划器检查不同的可能连接顺序以找到最便宜的一个。

如果查询使用的关系少于 geqo_threshold，则会进行近乎穷尽的搜索以找到最佳连接顺序。计划器优先考虑 WHERE 限制条件中存在相应连接子句的任意两个关系之间的连接（即存在 where rel1.attr1=rel2.attr2 这样的限制条件）。只有在没有其他选择时才考虑没有连接子句的连接对，也就是说，特定关系没有可用的连接子句与任何其他关系连接。计划器会为每个考虑的连接对生成所有可能的计划，并选择估计最便宜的一个。

当超过 geqo_threshold 时，连接顺序由启发式确定，如第 60 章所述。其他情况下，过程相同。

最终的计划树由基础关系的顺序或索引扫描、嵌套循环连接、合并连接或哈希连接节点以及任何需要的辅助步骤（如排序节点或聚合函数计算节点）组成。大多数这些计划节点类型还具有选择（丢弃不满足指定布尔条件的行）和投影（根据给定的列值计算派生列集，即在需要时计算标量表达式）的附加功能。计划器的职责之一是将 WHERE 子句中的选择条件和所需输出表达式的计算附加到计划树中最合适的节点上。

# 50.6. 执行器

执行器接收由计划器/优化器创建的计划，并递归地处理它以提取所需的行集。这本质上是一个需求拉动的流水线机制。每次调用计划节点时，它必须交付一行，或报告已完成行的交付。

举一个具体的例子，假设顶层节点是一个 MergeJoin 节点。在进行任何合并之前，必须获取两行（每个子计划一行）。因此，执行器递归地调用自身来处理子计划（从附加到 lefttree 的子计划开始）。新的顶层节点（左子计划的顶层节点）可能是一个 Sort 节点，再次需要递归以获得输入行。Sort 节点的子节点可能是一个 SeqScan 节点，代表实际读取表。执行此节点会导致执行器从表中获取一行，并将其返回到调用节点。Sort 节点会重复调用其子节点以获取所有要排序的行。当输入耗尽（子节点返回 NULL 而不是行时），Sort 代码执行排序，最终能够返回其第一输出行，即按排序顺序的第一行。它将剩余的行存储起来，以便响应后续需求按排序顺序交付它们。

MergeJoin 节点类似地要求从其右子计划获取第一行。然后，它比较这两行以查看它们是否可以连接；如果可以，它会返回一个连接行给其调用者。在下一次调用时，或者如果当前输入对无法连接时立即，它会推进到一个表或另一个表的下一行（取决于比较的结果），并再次检查是否匹配。最终，一个子计划或另一个子计划会耗尽，MergeJoin 节点返回 NULL 以表示无法形成更多的连接行。

复杂查询可能涉及多级计划节点，但总体方法是相同的：每个节点在每次调用时计算并返回其下一个输出行。每个节点还负责应用计划器分配给它的任何选择或投影表达式。

执行器机制用于评估所有五种基本 SQL 查询类型：SELECT、INSERT、UPDATE、DELETE 和 MERGE。对于 SELECT，顶层执行代码只需将查询计划树返回的每一行发送给客户端。INSERT ... SELECT、UPDATE、DELETE 和 MERGE 实际上是特殊顶层计划节点 ModifyTable 下的 SELECT。

INSERT ... SELECT 将行传递给 ModifyTable 进行插入。对于 UPDATE，计划器安排每个计算的行包含所有更新的列值，以及原始目标行的 TID（元组 ID，或行 ID）；这些数据传递到 ModifyTable 节点，该节点使用这些信息创建一个新的更新行并标记旧行已删除。对于 DELETE，计划实际返回的唯一列是 TID，ModifyTable 节点只是使用 TID 访问每个目标行并标记其已删除。对于 MERGE，计划器连接源和目标关系，并包含所有任何 WHEN 子句所需的列值，以及目标行的 TID；这些数据传递到 ModifyTable 节点，该节点使用这些信息确定要执行的 WHEN 子句，然后插入、更新或删除目标行，根据需要。

一个简单的 INSERT ... VALUES 命令创建一个由单个 Result 节点组成的简单计划树，该节点仅计算一个结果行，并将其传递给 ModifyTable 以执行插入。