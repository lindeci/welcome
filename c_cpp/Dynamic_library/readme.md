gcc -shared -o libfunctions.so -fPIC libfunctions.c  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp  
gcc -L. main.c -ldl -lfunctions -o main.out  
运行结果  
./main.out   
I am ICQ_Process_1:  999