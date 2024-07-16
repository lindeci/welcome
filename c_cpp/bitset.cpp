#include <bitset>
#include <iostream>
using namespace std;
int main()
{
    int a;
    a=8;
    cout << "------~操作-----------" << endl;
    cout << "a            :" << a << endl;
    cout << "bitset<8>(a) :" << bitset<8>(a) << endl;
    cout << "bitset<8>(~a):" << bitset<8>(~a) << endl;
    cout << "~a           :" << ~a << endl;
    cout << "-------字符串赋值------" << endl;
    //ldc:字符串类型
    cout<<"bitset<8>(\"10011\")       :" <<  bitset<8>("10011") << endl;
    cout<<"bitset<8>(\"10011\",4)     :" <<  bitset<8>("10011",4) << endl; //获取字符串的前面4位,然后在前面补0。相当bitset<8>("10011",0,4)
    string bitval ("11110011011");
    cout<<"bitset<8>(\"1101011\",3,4) :" <<  bitset<8>(bitval,3,4) << endl;  //从前面的第2+1位开始，往后获取4个字符，然后在前面补0。第一个参数是string，不能写成 bitset<8>("11110011011",3,4)
    cout << "-------函数成员--------" << endl;
    bitval = "10011011";
    bitset<8> me = bitset<8> (bitval);
    cout<< "me              :" << me  <<endl;
    cout<< "me.any()        :" << me.any() << endl;     //是否存在置为1的二进制位
    cout<< "me.none()       :" << me.none() << endl;       //是否全部位0 
    cout<< "me.count()      :" << me.count() << endl;     //二进制位为1的个数
    cout<< "me.size()       :" << me.size() << endl;     //二进制个数
    cout<< "me.flip()       :" << me.flip() << endl;     //把所有二进制位逐位取反
    cout<< "me.flip(2)      :" << me.flip(2) << endl;     //把在pos处的二进制位取反
    cout<< "me[0]           :" << me[0] << endl;     //获取在pos处的二进制位
    cout<< "me.set()        :" << me.set() << endl;     //把所有二进制位都置为1
    cout<< "me.set(1)       :" << me.set(1) << endl;     //把在pos处的二进制位置为1
    cout<< "me.reset()      :" << me.reset() << endl;     //把所有二进制位都置为0
    cout<< "me.reset(2)     :" << me.reset(2) << endl;     // 把在pos处的二进制位置为0
    cout<< "me.test(1)      :" << me.test(1) << endl;     //在pos处的二进制位是否为1
    me.set();
    cout<< "me.to_ulong()   :" << me.to_ulong() << endl;     //用同样的二进制位返回一个unsigned long值
    cout<< "me.to_string()  :" << me.to_string() << endl;     //返回对应的字符串
    return 0;
}
/*
------~操作-----------
a            :8
bitset<8>(a) :00001000
bitset<8>(~a):11110111
~a           :-9
-------字符串赋值------
bitset<8>("10011")       :00010011
bitset<8>("10011",4)     :00001001
bitset<8>("1101011",3,4) :00001001
-------函数成员--------
me              :10011011
me.any()        :1
me.none()       :0
me.count()      :5
me.size()       :8
me.flip()       :01100100
me.flip(2)      :01100000
me[0]           :0
me.set()        :11111111
me.set(1)       :11111111
me.reset()      :00000000
me.reset(2)     :00000000
me.test(1)      :0
me.to_ulong()   :255
me.to_string()  :11111111
*/