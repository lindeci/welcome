/*
其格式一般为: #pragma Para。其中Para 为参数，下面来看一些常用的参数.

message 参数
Message 参数能够在编译信息输出窗口中输出相应的信息，这对于源代码信息的控制是非常重要的。其使用方法为：
#pragma message("消息文本")

code_seg
另一个使用得比较多的pragma参数是code_seg。格式如：	
#pragma code_seg(["section-name"[,"section-class"]])
它能够设置程序中函数代码存放的代码段，当我们开发驱动程序的时候就会使用到它。

#pragma once
(比较常用）
只要在头文件的最开始加入这条指令就能够保证头文件被编译一次，这条指令实际上在VC6中就已经有了，但是考虑到兼容性并没有太多的使用它。

在GCC下，#pragma GCC diagnostic push用于记录当前的诊断状态，#pragma GCC diagnostic pop用于恢复诊断状态。

#pragma warning
#pragma warning(disable:450734;once:4385;error:164)
等价于：
#pragma warning(disable:450734)//不显示4507和34号警告信息
#pragma warning(once:4385)//4385号警告信息仅报告一次
#pragma warning(error:164)//把164号警告信息作为一个错误。

#pragma warning(push[,n])
#pragma warning(pop)
这里n代表一个警告等级(1---4)。
#pragma warning(push)保存所有警告信息的现有的警告状态。
#pragma warning(push,n)保存所有警告信息的现有的警告状态，并且把全局警告等级设定为n。
#pragma warning(pop)向栈中弹出最后一个警告信息

*/

#include <stdio.h>

#pragma once

#pragma GCC diagnostic push
//关闭警告,诊断忽略没有返回值
#pragma GCC diagnostic ignored "-Wreturn-type"

int test1(void)
{
    return;
}
//恢复到之前的诊断状态
#pragma GCC diagnostic pop

int test2(void)
{
    return;
}

int main()
{
#ifdef _X86
#pragma message("_X86 macro activated!")
#endif

#ifdef __x86_64__
#pragma message("__x86_64__ macro activated!")
#endif
    return 0;
}


/*
输出：

# gcc pragma.c  -o pragma -Wall
pragma.c:22:9: warning: #pragma once in main file
   22 | #pragma once
      |         ^~~~
pragma.c: In function ‘test2’:
pragma.c:37:5: warning: ‘return’ with no value, in function returning non-void [-Wreturn-type]
   37 |     return;
      |     ^~~~~~
pragma.c:35:5: note: declared here
   35 | int test2(void)
      |     ^~~~~
pragma.c: In function ‘main’:
pragma.c:47:9: note: ‘#pragma message: __x86_64__ macro activated!’
   47 | #pragma message("__x86_64__ macro activated!")

函数test2会提示警告不带返回值，而函数test1没有警告
*/