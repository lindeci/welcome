#include<stdlib.h>
#include<stdio.h>
int main()
{
    /*
    int atoi(const char *nptr);
    把字符串转换成整型数

    long atol(const char *nptr);
    把字符串转换成长整型数

    long int strtol(const char *nptr,char **endptr,int base);
    strtol函数会将参数nptr字符串根据参数base来转换成长整型数，参数base范围从2至36。
    
    double strtod(const char *nptr, char **endptr);
    strtod是C语言及C++中的重要函数，功能是将字符串转换成浮点数
    */
    char *string, *stopstring;
    double x;
    int base;
    long l;
    unsigned long ul;
    printf("----------atoi----------\n");
    string = "31415926";
    int i = atoi(string);
    printf("string         = %s\n", string);
    printf("atoi           = %d\n", i);
    printf("----------atol----------\n");
    string = "3141592631415926";
    l = atol(string);
    printf("string         = %s\n", string);
    printf("atol           = %ld\n", l);
    printf("----------strtod----------\n");
    string = "3.1415926 This stopped it";
    x = strtod(string, &stopstring);
    printf("string         = %s\n", string);
    printf("strtod         = %f\n", x);
    printf("Stopped scan at: %s\n", stopstring);
    printf("----------strtol----------\n");
    string = "-1011 This stopped it";
    l = strtol(string, &stopstring, 10);
    printf("string         = %s\n", string);
    printf("strtol         = %ld\n", l);
    printf("Stopped scan at: %s\n", stopstring);
    printf("----------strtol----------\n");
    string = "10110134932";
    printf("string         = %s\n", string);
    /*Convertstringusingbase2,4,and8:*/
    for(base = 2; base <= 8; base *= 2)
    {
        /*Convertthestring:*/
        ul = strtoul(string, &stopstring, base);
        printf("strtol         = %ld(base %d)\n", ul, base);
        printf("Stopped scan at: %s\n", stopstring);
    }
    printf("--------------------------\n");
    char* c="h12321h12";
    printf("%s\n",c);
    int a='\032';
    printf("%d\n",a);
    return 0;
}
