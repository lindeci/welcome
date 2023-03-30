#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(void)
{
   int fd[2], nbytes;
   pid_t childpid;
   char string[] = "Hello, world!\n";
   char readbuffer[80];

   pipe(fd);

   if((childpid = fork()) == -1)
   {
       printf("Error:fork");
       exit(1);
   }

   if(childpid == 0) /* 子进程是管道的读进程 */
   {
       close(fd[1]); /*关闭管道的写端 */
       nbytes = read(fd[0], readbuffer, sizeof(readbuffer));
       printf("Received string: %s", readbuffer);
       exit(0);
   }
   else /* 父进程是管道的写进程 */
   {
       close(fd[0]); /*关闭管道的读端 */
       write(fd[1], string, strlen(string)); 
   }

   return(0);
}

/*
注意，在这个例子中，为什么这两个进程都关闭它所不需的管道端呢？
这是因为写进程完全关闭管道端时，文件结束的条件被正确地传递给读进程。而读进程完全关闭管道端时，写进程无需等待继续写数据。

阻塞读和写分别成为对空和满管道的默认操作，这些默认操作也可以改变，这就需要调用 fcntl() 系统调用，
对管道文件描述符设置 O_NONBLOCK 标志可以忽略默认操作：
#include <fcntl.h>
fcntl（fd,F_SETFL,O_NONBlOCK）;
*/