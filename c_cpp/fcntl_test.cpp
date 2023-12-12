#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>
using namespace std;
 
 
int test_fun() {
    char buf[10];
    int fcntl_flags;
 
    char prompt[] = "please input text:\n";
 
    /*从标准输入取标志位*/
    fcntl_flags = fcntl(STDIN_FILENO, F_GETFL);
 
    /*增加非阻塞状态标志*/
    fcntl_flags |= O_NONBLOCK;
 
    /*重写标准输入标志位*/
    if (fcntl(STDIN_FILENO, F_SETFL, fcntl_flags) == -1)
    {
        cout << "fcntl fail." << endl;
        return -1;
    }
 
    while(1) {
        /*读取数据从标准输入*/
        int n = read(STDIN_FILENO, buf, 10);
        if (n < 0) {
            if (errno == EAGAIN) {
                sleep(1);
                write(STDOUT_FILENO, prompt, strlen(prompt));
                continue;
            }
            return 1;
        }
        write(STDOUT_FILENO, buf, n);
        return 0;
    }
}
 
int main(void)
{
    int res = test_fun();
    cout <<"res:" <<res;
    return 0;
}

/*
输出
please input text:
please input text:
please input text:
please input text:
helplease input text:
lo
please input text:
hello
res:0
*/

/*
当没有数据输入时，在while(1)循环中一直打印“please input text:“，直到有数据输入。从标准输入将输入的数据读出，并且输出到标准输出中。

可以看到，虽然没有数据输入，但是，并没有阻塞程序（一直在输出“please input text”）。
*/