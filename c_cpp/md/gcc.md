- [-fPIC](#-fpic)
- [-shared](#-shared)
- [-o](#-o)
- [-E](#-e)
- [-v](#-v)
- [-S](#-s)
- [-c](#-c)
- [-g](#-g)
- [-L](#-l)
- [-l](#-l-1)
- [-I](#-i)
- [-O](#-o-1)
- [-static](#-static)
- [-std](#-std)
- [-Wall](#-wall)
- [-Wextra](#-wextra)
- [-Werror](#-werror)
- [-D](#-d)
  - [常见宏](#常见宏)
- [-DDEBUG](#-ddebug)
- [查看gcc/g++版本以及对应默认的的C++标准](#查看gccg版本以及对应默认的的c标准)
- [注](#注)

GCC常用选项

## -fPIC
作用于编译阶段，在编译动态库时(.so文件)告诉编译器产生与位置无关代码(Position-Independent Code)，若未指定-fPIC选项编译.so文件，则在加载动态库时需进行重定向

## -shared
创建一个动态链接库

## -o
指定生成的输出文件；

## -E
仅执行编译预处理；

## -v
有两个作用。除了查看gcc版本之外，在编译时带上该选项可以看到详细的编译过程。比如分别执行编译，汇编，链接等命令，并且查看到使用的标准启动文件crt1.o, crti.o等，标准库文件libc，libgcc等

## -S
将C代码转换为汇编代码；

## -c
仅执行编译操作，不进行连接操作

## -g
在编译结果中加入调试信息

## -L
指定库文件路径

## -l
设置 链接库的名字

## -I
指定头文件路径

## -O
指定优化等级

## -static
使用静态链接

## -std
编译程序时所使用的编译标准
```sh
g++ -std=c++17
```

## -Wall
开启大多数的警告信息

## -Wextra
开启额外的警告信息，比如参数未使用警告(-Wunused-parameter)

## -Werror
将警告当作错误，中断编译

## -D
后面直接跟宏命，相当于定义这个宏，默认这个宏的内容是1
### 常见宏
_MSC_VER:  微软的预编译控制

## -DDEBUG

## 查看gcc/g++版本以及对应默认的的C++标准
```sh
$ g++ -dM -E -x c++  /dev/null | grep -F __cplusplus
#define __cplusplus 201703L
```

## 注

1. 可用的优化等级有 4 个，分别是 O0、O1、O2 和 O3。优化等级越高，编译速度越慢，相对而言程序运行速度越快，调试难度越大。其中 O0 表示关闭所有的优化项目。
2. 链接库文件 xxx 时，如果系统中同时存在其对应的静态库和动态库，使用此选项可以使得程序链接静态库，使程序编译之后不依赖于该库文件。
3. 如果你的程序中使用dlopen.dlsym.dlclose.dlerror 显示加载动态库,需要设置链接选项 -ldl 加载动态链接库,首先为共享库分配物理内存,然后在进程对应的页表项中建立虚拟页和物理页面之间的映射.

