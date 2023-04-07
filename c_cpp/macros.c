#include <stdio.h>
int main()
{
#if __STDC_HOSTED__ != 1
#  error "Not a hosted implementation"
#endif
 
#if __cplusplus <= 202302L
#  warning "Using #warning as a standard feature"
#endif


#ifdef _X86
#pragma message("_X86 macro activated!")
#endif

#ifdef __x86_64__
#pragma message("__x86_64__ macro activated!")
#endif

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