#include <iostream>
using namespace std;
/*
constexpr 说明符声明编译时可以对函数或变量求值。这些变量和函数（给定了合适的函数实参的情况下）即可用于需要编译期常量表达式的地方。 

constexpr 变量
    constexpr 变量必须满足下列要求：
        它的类型必须是字面类型 (LiteralType) 。
        它必须立即被初始化。
        它的初始化包括所有隐式转换、构造函数调用等的全表达式必须是常量表达式 



constexpr 函数

constexpr 构造函数

constexpr 析构函数

*/

/*
示例

计算阶乘的 C++11 constexpr 函数的定义，及扩展字符串字面量的字面类型：
*/
#include <iostream>
#include <stdexcept>
 
// C++11 constexpr 函数使用递归而非迭代
// （C++14 constexpr 函数可使用局部变量和循环）
constexpr int factorial(int n)
{
    return n <= 1 ? 1 : (n * factorial(n - 1));
}
 
// 字面类
class conststr
{
    const char* p;
    std::size_t sz;
public:
    template<std::size_t N>
    constexpr conststr(const char(&a)[N]): p(a), sz(N - 1) {}
 
    // constexpr 函数通过抛异常来提示错误
    // C++11 中，它们必须用条件运算符 ?: 来这么做
    constexpr char operator[](std::size_t n) const
    {
        return n < sz ? p[n] : throw std::out_of_range("");
    }
 
    constexpr std::size_t size() const { return sz; }
};
 
// C++11 constexpr 函数必须把一切放在单条 return 语句中
// （C++14 无此要求）
constexpr std::size_t countlower(conststr s, std::size_t n = 0,
                                             std::size_t c = 0)
{
    return n == s.size() ? c :
        'a' <= s[n] && s[n] <= 'z' ? countlower(s, n + 1, c + 1) :
                                     countlower(s, n + 1, c);
}
 
// 输出要求编译时常量的函数，用于测试
template<int n>
struct constN
{
    constN() { std::cout << n << '\n'; }
};
 
int main()
{
    std::cout << "4! = " ;
    constN<factorial(4)> out1; // 在编译时计算
 
    volatile int k = 8; // 使用 volatile 防止优化
    std::cout << k << "! = " << factorial(k) << '\n'; // 运行时计算
 
    std::cout << "\"Hello, world!\" 里小写字母的个数是 ";
    constN<countlower("Hello, world!")> out2; // 隐式转换到常量字符串
}