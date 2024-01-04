/*
Constructs a closure: an unnamed function object capable of capturing variables in scope.
*/
#include <iostream>
 
auto make_function(int& x)
{
    return [&]{ std::cout << x << '\n'; };
}
 
int main()
{
    int i = 3;
    auto f = make_function(i); // the use of x in f binds directly to i
    i = 5;
    f(); // OK: prints 5
}

/*
C++中的Lambda函数的标准格式如下：

```cpp
[capture_list] (parameters) mutable exception -> return_type { function_body }
```

各部分的含义如下：

- `capture_list`：捕获列表，用于指定要从外部作用域捕获的变量。捕获可以按值或按引用进行。
- `parameters`：参数列表，与普通函数的参数列表类似。
- `mutable`：可选的关键字，如果在Lambda函数中需要修改按值捕获的变量，则需要加上这个关键字。
- `exception`：可选的异常规范，用于指定Lambda函数是否抛出异常。
- `return_type`：返回类型，可以省略，编译器会自动推导。
- `function_body`：函数体，包含Lambda表达式的实际执行代码。
*/