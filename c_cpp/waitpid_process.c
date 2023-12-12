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
            sleep(1);
            int status;
            pid_t ret = waitpid(-1,&status,WNOHANG);            
            if(ret > 0)
            {
                if(WIFEXITED(status))
                {
                    printf("子进程退出时状态码:%d. 子进程 pid=%d\n",status,ret);
                }
                if(WIFSIGNALED(status))
                {
                    printf("子进程是被这个信号杀死的:%d. 子进程 pid=%d\n",status,ret);
                }
            }
            else if(ret ==0)
            {
                printf("子进程还没退出，不做任何处理... 子进程 pid=%d\n",ret);
            }
            else
            {
                printf("回收失败，或者已经没有子进程...\n");
            }
            printf("I am parent process. pid=%d\n",getpid());
        }    
    }
    else if(pid == 0)
    {
        printf("I am child process. pid=%d, ppid=%d\n",getpid(),getppid());
    }
 
    return 0;
}

/*结果
t# ./"waitpid_process"
I am child process. pid=286443, ppid=286440
I am child process. pid=286442, ppid=286440
I am child process. pid=286441, ppid=286440
I am child process. pid=286444, ppid=286440
I am child process. pid=286445, ppid=286440
子进程退出时状态码:0. 子进程 pid=286441
I am parent process. pid=286440
子进程退出时状态码:0. 子进程 pid=286442
I am parent process. pid=286440
子进程退出时状态码:0. 子进程 pid=286443
I am parent process. pid=286440
子进程退出时状态码:0. 子进程 pid=286444
I am parent process. pid=286440
子进程退出时状态码:0. 子进程 pid=286445
I am parent process. pid=286440
回收失败，或者已经没有子进程...
*/