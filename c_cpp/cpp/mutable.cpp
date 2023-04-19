/*
在C++中，mutable也是为了突破const的限制而设置的。被mutable修饰的变量，将永远处于可变的状态，即使在一个const函数中。

我们知道，如果类的成员函数不会改变对象的状态，那么这个成员函数一般会声明成const的。但是，有些时候，我们需要在const的函数里面修改一些跟类状态无关的数据成员，那么这个数据成员就应该被mutalbe来修饰。
*/

#include <iostream>

using namespace std;

class A
{
public:
	A(int a):m_a(a),m_b(2*a){}
	void matest()const;
	void macout()const
	{
		cout << m_a << endl;
        cout << m_b << endl;
	}
private:
	int m_a;
    mutable int m_b;
};

void A::matest() const
{
	//m_a = 10;//被const修饰的函数不允许修好任何类状态值(类里面的数据)
    m_b = 20;//在定义时用mutable来突破这层限制
	cout << m_a << endl;
    cout << m_b << endl;
}

int main()
{
	const A a(1);
	a.macout();//用const修饰的一个类使用一个const修饰的方法
	return 0;
}
