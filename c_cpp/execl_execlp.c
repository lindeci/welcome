#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
 
 
int main()
{
    // 创建子进程
    pid_t pid = fork();  //子进程的fork返回0,父进程返回非0
    // 在子进程中执行磁盘上的可执行程序
    if(pid == 0)
    {
        // 磁盘上的可执行程序 /bin/ps
#if 0
        //该函数可用于执行任意一个可执行程序，函数需要通过指定的文件路径才能找到这个可执行程序
        execl("/bin/ps", "title", "aux", NULL);
        // 也可以这么写
        // execl("/bin/ps", "title", "a", "u", "x", NULL);  
#else
        //该函数常用于执行已经设置了环境变量的可执行程序，函数中的  path，也是说这个函数会自动搜索系统的环境变量 PATH，因此使用这个函数执行可执行程序不需要指定路径，只需要指定出名字即可
        execlp("ps", "title", "aux", NULL);
        // 也可以这么写
        // execl("ps", "title", "a", "u", "x", NULL);
#endif
        // 如果成功当前子进程的代码区别 ps中的代码区代码替换
        // 下面的所有代码都不会执行
        // 如果函数调用失败了,才会继续执行下面的代码
        perror("execl");
        printf("++++++++++++++++++++++++\n");
        printf("++++++++++++++++++++++++\n");
        printf("++++++++++++++++++++++++\n");
        printf("++++++++++++++++++++++++\n");
        printf("++++++++++++++++++++++++\n");
        printf("++++++++++++++++++++++++\n");
    }
    else if(pid > 0)
    {
        printf("我是父进程.....\n");
    }
 
    return 0;
}