/*
一、final修饰类的虚函数
final的用法是写在虚函数的后面，告知后面继承该类的类不可以再重写该虚函数。

当孙子类中不能重写final修饰的虚函数时，如果父类的指针指向孙子类，并且调用final修饰的虚函数，实际上，调用的是子类（孙子类的父类）的虚函数



二、修饰类
直接加在类名的后面，表示该类是断子绝孙类，其他类不能再继承该类
*/

//final修饰类的虚函数
#include <iostream>
 
class Base {
public:
	Base() {
 
	}
public:
	virtual void func()  = 0 ;
	virtual void func2() = 0;
};
 
class Son :public Base
{
public:
	Son()
	{
 
	}
public:
	void func()
	{
		std::cout << "son func "<< std::endl;
	}
	void func2() final
	{
		std::cout << "son func2 " << std::endl;
 
	}
 
};
 
class Son2 :public Son
{
	void func()
	{
		std::cout << "son2 func " << std::endl;
	}
};
 
 
int main()
{
	Base* p = new Son2;
	p->func2();//son func2
}

/*
输出： 
son func2
*/