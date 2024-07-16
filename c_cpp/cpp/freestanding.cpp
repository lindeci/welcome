#include <iostream>
using namespace std;

int main()
{
        cout << "Standard Clib: " << __STDC_HOSTED__ << endl;   //打印 1
        cout << "Standard C: " << __STDC__ << endl;             //打印1
        cout << "ISO/IEC: " << __STDC_ISO_10646__ << endl;      //打印201103
        cout << "Function name: " << __FUNCTION__ << endl;      //打印main
        cout << "__cplusplus: " <<__cplusplus<< endl;           //打印201703

        return 0;
}
/*
Standard Clib: 1
Standard C: 1
ISO/IEC: 201103
Function name: main
__cplusplus: 201703
*/