gcc main.c enter.c print.c -o extern.o
或者gcc ../extern/main.c  ../extern/enter.c ../extern/print.c -o extern.o
输出:
./extern.o
abcdef                   # 输入的字符串
d                        # 要删除的字符
abcef                    # 删除后的字符串