#include<stdio.h>
#include<stddef.h>
struct S
{
    char c1;
    int a;
    char c2;
};
int main()
{
 //offsetof()返回 结构体成员 在内存中的偏移量
    printf("%d\n", offsetof(struct S, c1));//0
    printf("%d\n", offsetof(struct S, a));//4
    printf("%d\n", offsetof(struct S, c2));//8
    return 0;
}