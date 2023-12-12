/*
(void)0，把0强制转换为无类型，凡是用到assert_param(expr)的地方都用(void)0替换掉.
assert宏的原型定义在<assert.h>中，其作用是如果它的条件返回错误，则终止程序执行.
*/
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
int main( void )
{
    printf("1\n");
    assert(1);
    printf("2\n");
    assert(0);
    printf("3\n");
    return 0;
}

/*
输出：
1
2
assert: assert.c:13: main: Assertion `0' failed.
Aborted (core dumped)
*/