#include <stdlib.h>
#include <sys/stat.h>
#include <stdio.h>
int main()
{
    struct stat st;
    char* path="/etc/profile";
    if (stat(path, &st) == 0) {
/*      if (!(st.st_mode & (S_IXUSR  | S_IXGRP | S_IXOTH))) {
            printf("%s failed to load: It does not have execute permissions.", path);
            return 1;
        }
*/
    }
    printf("st.st_ino  : %ld\n",st.st_ino);
    printf("st.st_mode : %ld\n",st.st_mode);
    printf("st.st_ctime: %ld\n",st.st_ctime);
    printf("st.st_atime: %ld\n",st.st_atime);
    printf("st.st_mtime: %ld\n",st.st_mtime);

    return 0;
}