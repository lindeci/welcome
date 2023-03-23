/*
void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);

    addr：指定映射的虚拟内存地址，可以设置为 NULL，让 Linux 内核自动选择合适的虚拟内存地址。
    length：映射的长度。
    prot：映射内存的保护模式，可选值如下：
        PROT_EXEC：可以被执行。
        PROT_READ：可以被读取。
        PROT_WRITE：可以被写入。
        PROT_NONE：不可访问。
    flags：指定映射的类型，常用的可选值如下：
        MAP_FIXED：使用指定的起始虚拟内存地址进行映射。
        MAP_SHARED：与其它所有映射到这个文件的进程共享映射空间（可实现共享内存）。
        MAP_PRIVATE：建立一个写时复制（Copy on Write）的私有映射空间。
        MAP_LOCKED：锁定映射区的页面，从而防止页面被交换出内存。
        ...
    fd：进行映射的文件句柄。
    offset：文件偏移量（从文件的何处开始映射）。
*/

#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    int fd;
    void *start;
    struct stat sb;

    fd = open("/etc/passwd", O_RDONLY); /*打开/etc/passwd */
    fstat(fd, &sb); /* 取得文件大小 */
    start = mmap(NULL, sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (start == MAP_FAILED) /* 判断是否映射成功 */
        return 0;
    printf("%s",(char*)start);
    munmap(start, sb.st_size);

    close(fd);
    return 1;
}