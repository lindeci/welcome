mytest.c放在 redis/src/modules/ 目录下

编译 
gcc mytest.c  -fPIC -shared -o libtest.so

加载
module load src/modules/libtest.so

测试
127.0.0.1:6379> ldc_helloworld test
"test"
127.0.0.1:6379>

卸载
module unload ldc_helloworld