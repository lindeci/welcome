//const pointer usage
#include <iostream>

int main()
{
//1、const修饰普通类型的变量
{
    const int  a = 7; 
    a = 8;       // 错误，a 被编译器认为是一个常量，其值不允许修改。
}
//---------------------------------------------------------------------------------------------
//2、const修饰指针变量
//2.1、如果const位于 * 的左侧，const 修饰指针指向的内容，则内容为不可变量，简称左定值；
{
    int a = 7;
    int b = 8;
    const int* c = &a;
    *c = b; //错误：指针指向的内容不可修改
    c = &b;//正确：指针可以修改
}
//2.2、如果const位于*的右侧，const 修饰指针，则指针为不可变量，简称右定向；
{
    int a = 7;
    int b = 8;
    int* const c = &a;
    *c = b; //正确：指针指向的内容可修改
    c = &b;//错误：指针为不可变量
}
//2.3、const 修饰指针和指针指向的内容，则指针和指针指向的内容都为不可变量
{
    int a = 7;
    int b = 8;
    const int* const  c = &a;
    *c = b;//错误：指针指向的内容不可修改   
    c = &b;//错误：指针为不可变量
}
//---------------------------------------------------------------------------------------------
//3、const参数传递和函数返回值
//3.1、值传递的 const 修饰传递，传递过来的参数在函数内不可以改变
{
    void func(const int p)
    {
            cout << "p = " << p << endl;
            //++p;//错误：p值不能修改
    }
    
}
//3.2、当 const 参数为指针时，可以防止指针被意外篡改
{
    void func(int* const  p)
    {
        cout << "*p = " << *p << endl;
        ++*p;
        //p = &b;//错误：p不能被修改
    }
}
//3.3、自定义类型的参数传递，需要临时对象复制参数，对于临时对象的构造，需要调用构造函数，比较浪费时间，因此我们采取 const 外加引用传递的方法。并且对于一般的 int、double 等内置类型，我们不采用引用的传递方式。同时，传递的对象不能被修改
{
    class Student
    {
    public:
        Student(){}
        Student(int num):number(num){}
        int get_number()const
        {
        return number;
        }
        int set_number(int num);
    private:
        int number;
    };
    void get_student_number(const Student& stu)
    {
        cout<<stu.get_number()<<endl;
        //stu.set_number(3333);//对象stu不能被修改
    }
}
//3.4 const 修饰内置类型的返回值，修饰与不修饰返回值作用一样,因此这种写法没有意义
{
    const int func1()
    {
        return 1;
    }
    
    int func2()
    {
        return 2;
    }
}
//3.5 const 修饰自定义类型的作为返回值，此时返回的值不能作为左值使用，既不能被赋值，也不能被修改
//3.6 const 修饰返回的指针或者引用，是否返回一个指向 const 的指针，取决于我们想让用户干什么
//一般情况下，函数的返回值为某个对象时，如果将其声明为const时，多用于操作符的重载
//---------------------------------------------------------------------------------------------
//4、const修饰类成员函数
//const 修饰类成员函数，其目的是防止成员函数修改被调用对象的值，如果我们不想修改一个调用对象的值，所有的成员函数都应当声明为 const 成员函数
}