#include <stdio.h>
int main()
{

    printf("The OS :");
#ifdef __linux
    printf("Linux\n");
#endif
#ifdef _WIN32
    printf("win 32\n");
#endif
#ifdef _WIN64
    printf("win 64\n");
#endif


    printf("The Compiler : ");
#ifdef __GNUC__
    printf("GCC\n");
#endif
#ifdef _MSC_VER
    printf("VC\n");
#endif
    printf("Test Over!!!");

#define REDISMODULE_API     //空的宏    
    printf("%d\n",REDISMODULE_API 1);
    REDISMODULE_API void * (*RedisModule_Alloc)(size_t bytes) __attribute__((__common__));
    (void)RedisModule_Alloc;
    return 0;
}