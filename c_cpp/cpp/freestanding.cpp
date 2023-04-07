#include <iostream>
using namespace std;

int main()
{
        cout << "Standard Clib: " << __STDC_HOSTED__ << endl;
        cout << "Standard C: " << __STDC__ << endl;
        cout << "ISO/IEC: " << __STDC_ISO_10646__ << endl;
        cout << "Function name: " << __FUNCTION__ << endl;
        cout << "__cplusplus: " <<__cplusplus<< endl;

        return 0;
}