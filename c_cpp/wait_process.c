#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
 
 
int main()
{
    pid_t pid;
    for(int i=0;i<5;i++){
        // 创建子进程
        pid = fork();  //子进程的fork返回0,父进程返回非0
        if (pid == 0) 
            break;
    }
    
    if (pid > 0) 
    {
        while(1)
        {
            pid_t ret = wait();
            if(ret > 0)
            {
                printf("成功回收子进程资源. 子进程 pid=%d\n",ret);
            }
            else
            {
                 printf("回收失败，或者已经没有子进程...\n");
            }
            printf("I am parent process. pid=%d\n",getpid());
            sleep(1);
        }
        
    }
    else if(pid == 0)
    {
        printf("I am child process. pid=%d, ppid=%d\n",getpid(),getppid());
    }
 
    return 0;
}

/*结果
# ./"wait_process"
I am child process. pid=269697, ppid=269694
回收失败，或者已经没有子进程...
I am parent process. pid=269694
I am child process. pid=269696, ppid=269694
I am child process. pid=269698, ppid=269694
I am child process. pid=269699, ppid=269694
I am child process. pid=269695, ppid=269694
成功回收子进程资源. 子进程 pid=269695
I am parent process. pid=269694
成功回收子进程资源. 子进程 pid=269696
I am parent process. pid=269694
成功回收子进程资源. 子进程 pid=269698
I am parent process. pid=269694
成功回收子进程资源. 子进程 pid=269699
I am parent process. pid=269694
回收失败，或者已经没有子进程...
I am parent process. pid=269694
回收失败，或者已经没有子进程...
I am parent process. pid=269694
回收失败，或者已经没有子进程...
I am parent process. pid=269694
回收失败，或者已经没有子进程...
*/