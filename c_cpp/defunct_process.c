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
            printf("I am parent process. pid=%d\n",getpid());
            sleep(1);   //子进程睡眠1秒，这期间父进程退出，子进程变成孤儿进程
        }
        
    }
    else if(pid == 0)
    {
        printf("I am child process. pid=%d, ppid=%d\n",getpid(),getppid());
    }
 
    return 0;
}

/*结果
./"defunct_process"
I am child process. pid=267032, ppid=267029
I am parent process. pid=267029
I am child process. pid=267031, ppid=267029
I am child process. pid=267030, ppid=267029
I am child process. pid=267033, ppid=267029
I am child process. pid=267034, ppid=267029
I am parent process. pid=267029
I am parent process. pid=267029
I am parent process. pid=267029
I am parent process. pid=267029


ps查看进程信息会发现这五个僵尸子进程defunct
# ps -a
    PID TTY          TIME CMD
 235815 pts/0    00:00:00 sudo
 235817 pts/2    00:00:00 su
 235818 pts/2    00:00:00 bash
 267029 pts/25   00:00:00 defunct_process
 267030 pts/25   00:00:00 defunct_process <defunct>
 267031 pts/25   00:00:00 defunct_process <defunct>
 267032 pts/25   00:00:00 defunct_process <defunct>
 267033 pts/25   00:00:00 defunct_process <defunct>
 267034 pts/25   00:00:00 defunct_process <defunct>
 267227 pts/28   00:00:00 sudo
 267229 pts/29   00:00:00 su
 267230 pts/29   00:00:00 bash
 267306 pts/29   00:00:00 ps
*/