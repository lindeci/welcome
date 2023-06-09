- [什么是 man](#什么是-man)
- [man 手册构成](#man-手册构成)
- [man 手册的数字编号](#man-手册的数字编号)
- [快捷键](#快捷键)

### 什么是 man

man 手册这样介绍：

> man - an interface to the system reference manuals

### man 手册构成

一个 man 手册遵守下面的章节结构。

> Conventional
> section  names  include  NAME,  SYNOPSIS,  CONFIGURATION, DESCRIPTION,
> OPTIONS, EXIT STATUS, RE‐TURN VALUE, ERRORS, ENVIRONMENT, FILES,
> VERSIONS, CONFORMING TO, NOTES, BUGS, EXAMPLE, AUTHORS, and SEE ALSO.

| 章节名称      | 解释                                                                   |
| --------------- | ------------------------------------------------------------------------ |
| NAME          | 命令名称和命令简短的介绍                                               |
| SYNOPSIS      | 语法，使用的方法，比如需要 #include  或命令参数 objdump [-d] |
| CONFIGURATION | 配置信息                                                               |
| DESCRIPTION   | 命令的描述                                                             |
| OPTIONS       | 命令的选项，比如 ls -l 中的 -l 就是选项                                |
| EXIT STATUS   | 命令的退出状态                                                         |
| RETURN VALUE  | 命令返回值                                                             |
| ERRORS        | 命令的错误信息                                                         |
| ENVIRONMENT   | 命令使用的环境变量                                                     |
| FILES         | 命令用到的文件                                                         |
| VERSIONS      | 命令的版本                                                             |
| CONFORMING TO | 命令遵循的标准，比如 POSIX 标准，可以参考 man _exit                    |
| NOTES         | 其他可以参考的资料，可以参考 man _exit                                 |
| BUGS          | 提交 BUG 的方式，man ls 中为 REPORTING BUGS                            |
| EXAMPLE       | 示例用法                                                               |
| AUTHORS       | 命令的作者                                                             |
| SEE ALSO      | 类似于友情链接，显示一些相关的命令                                     |

还有一些章节名称没有在 man man 中，其他手册可以看到。

* COPYRIGHT 版权信息
* COLOPHON 出版信息，可以参考 man _exit

### man 手册的数字编号

`man 1 kill`、`man 2 kill`，这些命令都是查看 kill 命令的手册，但是文档却大不相同。

因为 kill 是一个命令行的工具，`which kill` 看到 /usr/bin/kill 是一个二进制文件；其实，也有一个系统调用叫做 kill。

man 1 kill 显示的是命令行工具 kill 的手册；

man 2 kill 显示系统调用 kill 的手册；

显示什么类型的手册，由 man 和命令中间的数字决定，目前共有 9 个 man 支持的数字。

| 数字 | 说明                                                                                                |
| ------ | ----------------------------------------------------------------------------------------------------- |
| 1    | 可执行程序或 Shell 命令                                                                             |
| 2    | 系统调用（内核提供的函数）                                                                          |
| 3    | 库调用                                                                                              |
| 4    | 特殊文件（通常位于 /dev 目录）                                                                      |
| 5    | 文件格式和约定（比如 /etc/passwd）                                                                  |
| 6    | 游戏                                                                                                |
| 7    | 杂项（包和一些约定）Miscellaneous (including macro packages and conventions), e.g. man(7), groff(7) |
| 8    | 系统管理命令（通常是 root 用户执行的命令）                                                          |
| 9    | 内核相关的文件 Kernel routines [Non standard]                                                       |

### 快捷键

man man 打开 man 命令的 man 手册，然后按 h 键可以进去帮助界面，会有一些快捷键的使用说明。  
j 走到下一行  
k 走到上一行  
g 回到第一行  
G 跳到最后一行  
f 向下翻一页  
b 向上翻一页  
/ 向下搜索 搭配 n 键跳到下一个搜索到的位置  
? 向上搜索 搭配 n 键跳到下一个搜索到的位置  

