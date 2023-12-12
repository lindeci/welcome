gcc -shared -o libfunctions.so -fPIC libfunctions.c  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp  
gcc -L. main.c -ldl -lfunctions -o main.out  
运行结果  
./main.out   
I am ICQ_Process_1:  999




注:
1. -fPIC 作用于编译阶段，在编译动态库时(.so文件)告诉编译器产生与位置无关代码(Position-Independent Code)，若未指定-fPIC选项编译.so文件，则在加载动态库时需进行重定向.
   
2. 

3. CC的全称为“C Compiler”，它是Unix系统用来编译C语言的编译器，只支持C语言的编译。

4. GCC的全称是“Gnu Compiler Collection”，是很多编译器的集合，比如C编译器、 C++编译器、Objective-C编译器、Fortran编译器和Java编译器等等。当调用gcc命令时，GCC编译器会根据文件扩展名自动识别并调用对应的编译器。
