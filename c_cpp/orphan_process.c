#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
 
 
int main()
{
    // 创建子进程
    pid_t pid = fork();  //子进程的fork返回0,父进程返回非0
    if (pid == 0) 
    {
        sleep(1);   //子进程睡眠1秒，这期间父进程退出，子进程变成孤儿进程
        printf("I am orphan child process.\n");
    }
    else if(pid > 0)
    {
        printf("I am parent process.\n");
    }
 
    return 0;
}