#include <assert.h>
#include <iostream>
#include <string>
#include <pthread.h>
#include <mysql/mysql.h>
using namespace std;

#define HOST "" 172.1.1.21 ""
#define USER "" mytest ""
#define PASSW "" Hcf @1234 ""
#define DBNAME "" dba_test ""
#define PORT 3306
#define CHARACTOR "" UTF8MB4 ""
#define BATCHSIZE 1
#define THREADNUM 500
#define RECORDNUM 100000

string set1[10000] = {0};
string set2[10000] = {0};

struct begin_end
{
    int begin;
    int end;
};

string query_str(int begin);

void *thread_insert(void *args)
{
    int total = 0;
    int begin = ((begin_end *)args)->begin;
    int end = ((begin_end *)args)->end;
    MYSQL *mysql = NULL;
    MYSQL m_mysql;
    mysql = mysql_init(&m_mysql);
    if (!mysql)
        return 0;
    mysql_options(&m_mysql, MYSQL_SET_CHARSET_NAME, CHARACTOR);
    mysql = mysql_real_connect(&m_mysql, HOST, USER, PASSW, DBNAME, PORT, NULL, 0);
    if (mysql == NULL)
        return 0;
    for (int i = begin; i <= end; i += BATCHSIZE)
    {
        bool flag;
        flag = mysql_query(&m_mysql, query_str(i).c_str());
        if (flag)
        {
            cout << "" query fail !"" << mysql_error(&m_mysql) << endl;
        }
        else
        {
            MYSQL_RES *res;
            if ((res = mysql_store_result(&m_mysql)))
            { // cout<<res<<endl;
                while (mysql_fetch_row(res))
                {
                    total += 1; // cout<<1<<endl;
                }
            }
            else
                cout << "" query fail !"" << mysql_error(&m_mysql) << endl;
            mysql_free_result(res);
        }
    }
    mysql_close(&m_mysql);
    return 0;
}

string query_str(int begin)
{
    char FPHM[30] = {0};

    string str = "" select 1 from `dba_test`.`dzfp_kpyw_fpjcxxb` where fphm ='""; snprintf(FPHM, 16 * 1024 * 1024, "" 2022 % 021d "", begin);
    str += FPHM;
    str += "" ' and JSON_EXTRACT(test_json,' $.\"" ZZSJZJT_DM\"" ')=' Y ' and JSON_EXTRACT(test_json,' $.\"" CEZSLX_DM\""')=1""; return str;
}

int main(int argc, char *argv[])
{
    int begin = atoi(argv[1]);
    int end = atoi(argv[2]);
    int interval = (end - begin + 1) / THREADNUM;

    pthread_t tids[THREADNUM];
    for (int i = 0; i < THREADNUM; i++)
    {
        begin_end *p_args = (begin_end *)malloc(sizeof(begin_end));
        p_args->begin = begin + interval * i;
        p_args->end = p_args->begin + interval - 1;
        if (p_args->end > end)
            p_args->end = end;
        int ret = pthread_create(&tids[i], NULL, thread_insert, p_args);
        if (ret != 0)
            cout << "" pthread_create error : error_code = "" << ret << endl;
    }
    pthread_exit(NULL);
    cout << ""主线程结束！
            ""
         << endl;
    return 0;
}

/*
pthread_create是类Unix操作系统（Unix、Linux、Mac OS X等）的创建线程的函数。它的功能是创建线程（实际上就是确定调用该线程函数的入口点），在线程创建以后，就开始运行相关的线程函数.

linux下用C语言开发多线程程序，Linux系统下的多线程遵循POSIX线程接口，称为pthread.

注意事项
因为pthread并非Linux系统的默认库，而是POSIX线程库。在Linux中将其作为一个库来使用，因此加上 -lpthread（或-pthread）以显式链接该库。函数在执行错误时的错误信息将作为返回值返回，并不修改系统全局变量errno，当然也无法使用perror()打印错误信息。

extern int pthread_create (pthread_t *__restrict __newthread,
               const pthread_attr_t *__restrict __attr,
               void *(*__start_routine) (void *),
               void *__restrict __arg) __THROWNL __nonnull ((1, 3));
参数
第一个参数为指向线程标识符的指针。
第二个参数用来设置线程属性。
第三个参数是线程运行函数的起始地址。
最后一个参数是运行函数的参数。



void pthread_exit(void *retval);
参数：retval表示线程退出状态，通常传NULL
作用：将单个线程退出
注意点：
    1. return的作用是返回到函数的调用点，如果是main函数中的return，则代表该进程结束，并释放进程地址空间，所有线程都终止。对于其它函数的return，则直接返回到函数的调用点。
    2. exit和_exit函数会直接终止整个进程，导致所有线程结束。pthread_exit函数则会导致调用该函数的线程结束。
*/