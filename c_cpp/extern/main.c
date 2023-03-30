/*
内部函数
如果一个函数只能被本文件中其他函数所调用，它称为内部函数。在定义内部函数时，在函数名和函数类型的前面加 static。
内部函数又称静态函数。使用内部函数，可以使函数的作用域只局限于所在文件。即使在不同的文件中有同名的内部函数，也互不干扰。提高了程序的可靠性。

外部函数
如果在定义函数时，在函数的首部的最左端加关键字 extern，则此函数是外部函数，可供其它文件调用。
C 语言规定，如果在定义函数时省略 extern，则默认为外部函数。
*/

#include <stdio.h>
 
extern void enter(char str[]); // 对函数的声明
extern void print(char str[]); // 对函数的声明
extern int enter_test;


static void delete_string(char str[],char ch);
int main()
{    
    char c,str[100];
    enter(str);
    scanf("%c",&c);
    delete_string(str,c);
    print(str);
    printf("%d\n",enter_test);
    return 0;
}
 
static void delete_string(char str[],char ch)//内部函数
{
    int i,j;
    for(i=j=0;str[i]!='\0';i++)
    if(str[i]!=ch)
    str[j++]=str[i];
    str[j]='\0';
}

/*
输出:
./extern.o
aabbcc
aa
bbcc

31415
*/