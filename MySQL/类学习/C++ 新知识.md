- [前置声明](#前置声明)
- [C++ 中的类的 virtual 的作用](#c-中的类的-virtual-的作用)
- [C++ 中 override 的作用](#c-中-override-的作用)
- [计算符优先级](#计算符优先级)
  - [\*a\[1\]](#a1)
  - [i-\>a\[0\]](#i-a0)
  - [\*i-\>a](#i-a)
  - [总结](#总结)
- [scope\_guard 和 decltype](#scope_guard-和-decltype)
- [extern 关键字](#extern-关键字)
- [map 的 key 的类型](#map-的-key-的类型)
- [using](#using)
- [explicit](#explicit)
- [std::enable\_if\_t](#stdenable_if_t)
- [模板一些知识](#模板一些知识)
  - [std::remove\_const\_t](#stdremove_const_t)
  - [std::enable\_if\_t](#stdenable_if_t-1)
  - [typename =](#typename-)
  - [组合使用](#组合使用)
  - [萃取器](#萃取器)
  - [运算符重载不会改变运算符的操作位置](#运算符重载不会改变运算符的操作位置)
- [(\*p)-\>m 和 p-\>m 是否等价](#p-m-和-p-m-是否等价)
- [std::stable\_sort](#stdstable_sort)
  - [TriviallyDestructible](#triviallydestructible)
- [函数返回  副本、指针、引用](#函数返回--副本指针引用)
- [函数名字前面或者后面加 const](#函数名字前面或者后面加-const)
- [模板参数包 和  完美转发](#模板参数包-和--完美转发)
- [友元](#友元)
- [const std::nothrow\_t \&arg \[\[maybe\_unused\]\] = std::nothrow](#const-stdnothrow_t-arg-maybe_unused--stdnothrow)
- [noexcept](#noexcept)
- [namespace {int stack\_direction = 0;}](#namespace-int-stack_direction--0)
- [__attribute__((noinline))](#attributenoinline)
- [std::deque](#stddeque)
- [for (int i : d)](#for-int-i--d)
- [ptype 使用](#ptype-使用)
- [virtual + final](#virtual--final)
- [单向链表中的双指针](#单向链表中的双指针)
- [GDB 调试 MySQL](#gdb-调试-mysql)
- [左值、右值、完美转发](#左值右值完美转发)
  - [举例介绍](#举例介绍)

# 前置声明
- 在类 A 的头文件中进行了类 B 的前置声明，这允许在类 A 中使用 ClassB 的指针或引用，但并不允许直接调用类 B 的函数成员。这是因为前置声明只表明这个名称是一个有效的类型，但不提供关于类的具体信息。
- 如果要使用 ClassB 的函数成员，需要在 ClassA.cpp 文件中包含 ClassB.h 头文件，以获取完整的定义。
```cpp
// ClassA.h

#ifndef CLASSA_H
#define CLASSA_H

class ClassB;  // Forward declaration of ClassB

class ClassA {
public:
    void doSomethingWithB(ClassB* objB);  // 可以接受 ClassB 的指针参数
    void doSomethingMoreWithB(ClassB& objB);  // 也可以接受 ClassB 的引用参数
    // 但以下代码是不允许的：
    // void doSomethingMoreWithB(ClassB objB);  // 直接传递 ClassB 的实例
    // objB.someFunctionInClassB();  // 直接调用 ClassB 的成员函数
};

#endif
```

# C++ 中的类的 virtual 的作用
虚函数允许被子类覆盖，实现了所谓的“动态联编”或“多态”。

当我们在基类中声明一个函数为虚函数时，我们可以在派生类中重新定义这个函数。当我们通过一个基类的指针或引用来调用这个函数时，实际上调用的是派生类中的版本，这就是虚函数的主要作用。

```cpp
class Base {
public:
    void show() { cout << "Base::show() called" << endl; }
    virtual void print() { cout << "Base::print() called" << endl; }
};

class Derived : public Base {
public:
    void show() { cout << "Derived::show() called" << endl; }
    void print() { cout << "Derived::print() called" << endl; }
};

int main() {
    Base* bptr;
    Derived d;
    bptr = &d;

    // 虚函数 print() 是多态的
    bptr->print();  // 输出 "Derived::print() called"

    // 非虚函数 show() 是非多态的
    bptr->show();  // 输出 "Base::show() called"

    return 0;
}
```

# C++ 中 override 的作用
在C++中，当我们在类的成员函数后面添加override关键字时，这表示我们希望这个函数覆盖（重写）基类中的同名虚函数。这个关键字可以帮助我们在编译时检查是否正确地覆盖了基类的虚函数。如果没有正确覆盖，编译器会报错。

# 计算符优先级
## *a[1]
[]运算符的优先级高于*运算符。因此，*a[1]首先会计算a[1]，然后对结果进行解引用。
## i->a[0]
在C++中，->运算符的优先级高于[]运算符。因此，i->a[0]首先会计算i->a，然后得到结果数组的第一个元素。
## *i->a
->运算符的优先级高于*运算符。因此，*i->a首先会计算i->a，然后对结果进行解引用。
## 总结
->  
[]  
*

# scope_guard 和 decltype
好的，我来举一个简单的例子来解释这段代码。

假设我们有一个类`Person`，它有一个成员变量`name`：

```cpp
class Person {
public:
    std::string name;
};
```

然后我们创建了一个`Person`对象`p`：

```cpp
Person p;
p.name = "Alice";
```

现在我们想要在离开某个作用域时自动将`p.name`重置为默认值，我们可以使用`scope_guard`和`decltype`来实现这个功能：

```cpp
{
    auto reset_name = create_scope_guard([&]() {
        p.name = decltype(p.name)();
    });

    // 在这个作用域中，我们可以对p.name进行各种操作
    p.name = "Bob";
} // 当离开这个作用域时，reset_name会自动执行，将p.name重置为默认值
```

在这个例子中，`decltype(p.name)()`得到的是`std::string`的默认构造函数，也就是一个空字符串。所以，当离开作用域时，`p.name`会被自动重置为一个空字符串。

这就是`scope_guard`和`decltype`的基本用法。

# extern 关键字
在 C++ 中，`extern` 关键字用于声明一个变量，而不定义它。也就是说，`extern bool sql_check;` 这行代码告诉编译器，存在一个名为 `sql_check` 的 `bool` 类型的全局变量。然而，这个变量在哪里定义，编译器并不知道。

当编译器遇到 `extern` 声明时，它会在链接阶段查找这个变量的定义。如果在所有的源文件中都找不到这个变量的定义，链接器会报错，因为它无法找到这个变量的存储空间。

因此，您需要在 `.cc` 文件中提供 `bool sql_check = true;` 这行代码，以定义 `sql_check` 变量。这样，链接器就可以找到 `sql_check` 的定义，并分配存储空间。

总的来说，`extern` 关键字允许您在一个源文件中声明一个变量，然后在另一个源文件中定义这个变量。这对于在多个源文件中共享全局变量非常有用。

# map 的 key 的类型

  // SQL 审核时，记录所有字段的类型
  std::unordered_map<std::string, enum_field_types> m_sql_check_columns_type;
    // SQL 审核时，记录所有字段的类型
  std::unordered_map<const char*, enum_field_types> m_sql_check_columns_type;

# using
在C++中，`using`关键字可以用来定义类型别名。`size_type`是一个常见的类型别名，通常在容器类中定义，用来表示容器中元素的数量或者索引。

例如，`using size_type = size_t;`就是定义了一个名为`size_type`的类型别名，它的实际类型是`size_t`。这样，你就可以在代码中使用`size_type`来代替`size_t`。

这样做的好处是提高了代码的可读性和可维护性。如果以后需要改变`size_type`的实际类型，你只需要修改这个`using`语句，而不需要修改使用`size_type`的所有地方。

例如，你可能会在自定义的容器类中看到这样的代码：

```cpp
class MyContainer {
public:
    using size_type = size_t;
    // ...
};
```

然后，在使用这个容器类时，你可以这样写：

```cpp
MyContainer c;
MyContainer::size_type i = c.size();
```

这样，即使`size_type`的实际类型发生了改变，你也不需要修改这段代码。。

# explicit
在C++中，`explicit`关键字用于防止类构造函数的隐式自动转换。通常，如果一个类的构造函数只需要一个参数，那么这个构造函数可以用来将一个值隐式地转换为这个类的对象。这种转换被称为隐式转换。

例如，假设我们有一个名为`MyClass`的类，它有一个接受`int`参数的构造函数：

```cpp
class MyClass {
public:
    MyClass(int value) { /* ... */ }
};
```

在这种情况下，你可以使用一个`int`值来隐式地创建一个`MyClass`对象：

```cpp
MyClass obj = 42;  // 隐式转换
```

然而，有时候这种隐式转换可能会导致一些意想不到的结果，特别是在函数重载等情况下。为了避免这种情况，你可以使用`explicit`关键字来阻止构造函数的隐式转换：

```cpp
class MyClass {
public:
    explicit MyClass(int value) { /* ... */ }
};
```

现在，你不能再使用一个`int`值来隐式地创建一个`MyClass`对象：

```cpp
MyClass obj = 42;  // 编译错误
```

你必须显式地调用构造函数来创建对象：

```cpp
MyClass obj(42);  // 正确
```

总的来说，`explicit`关键字可以帮助你编写更安全、更清晰的代码，避免因隐式转换导致的潜在问题

# std::enable_if_t
在`std::enable_if_t<std::is_integral<T>::value, int>`这个表达式中，`std::is_integral<T>::value`和`int`并不冗余，它们各自有不同的作用。

`std::is_integral<T>::value`是一个编译时常量，它的值为`true`或`false`，取决于模板参数`T`是否是整数类型。这个值用于决定`std::enable_if_t`是否定义一个类型。

`int`是`std::enable_if_t`的第二个模板参数，它是默认参数，只有在第一个参数为`true`时才会使用。这个参数决定了`std::enable_if_t`定义的类型。在这个例子中，如果`T`是整数类型，那么`std::enable_if_t<std::is_integral<T>::value, int>`就是`int`类型。如果`T`不是整数类型，那么`std::enable_if_t<std::is_integral<T>::value, int>`就不定义任何类型。

所以，`std::is_integral<T>::value`和`int`并不冗余，它们各自扮演了不同的角色。`std::is_integral<T>::value`用于检查`T`是否是整数类型，`int`用于定义`std::enable_if_t`的类型。这是C++模板元编程中常见的模式，用于在编译时进行条件判断和类型定义。这种技术可以帮助我们编写更安全、更灵活的代码。

# 模板一些知识
## std::remove_const_t
`std::remove_const_t` 是 C++ 标准库中的一个类型萃取器，它用于移除类型的 `const` 修饰符。这个模板接受一个类型参数，如果这个类型是 `const` 类型，那么 `std::remove_const_t` 就会移除 `const`，否则它就直接返回原始类型。

下面是一个简单的例子：

```cpp
#include <type_traits>
#include <iostream>

int main() {
    std::cout << std::is_same<std::remove_const_t<const int>, int>::value << '\n';  // 输出 "1"
    std::cout << std::is_same<std::remove_const_t<int>, int>::value << '\n';  // 输出 "1"
    return 0;
}
```

在这个例子中，`std::remove_const_t<const int>` 是 `int` 类型，因为 `const int` 是一个 `const` 类型，所以 `std::remove_const_t` 移除了 `const`。`std::remove_const_t<int>` 也是 `int` 类型，因为 `int` 不是一个 `const` 类型，所以 `std::remove_const_t` 直接返回了原始类型。

这种技术常常用于模板编程中，当我们需要一个不带 `const` 修饰符的类型时，可以使用 `std::remove_const_t` 来获取。这是 C++ 模板元编程的一个重要特性，它使我们的代码更加通用和可重用。如果你还有其他问题，欢迎随时提问。

## std::enable_if_t
`std::enable_if_t`是C++标准库中的一个模板，它用于在编译时根据条件启用或禁用某个函数或类模板。这种技术被称为SFINAE（Substitution Failure Is Not An Error），意思是如果模板替换失败，那么这不是一个错误，编译器会继续寻找其他可以匹配的模板。

下面是一个简单的例子，这个例子中定义了一个函数模板`foo`，它只接受整数类型的参数：

```cpp
#include <type_traits>

template <typename T, std::enable_if_t<std::is_integral<T>::value, int> = 0>
void foo(T val) {
    // ...
}
```

在这个例子中，`std::enable_if_t`用于检查模板参数`T`是否是整数类型。如果`T`是整数类型，那么`std::is_integral<T>::value`就是`true`，`std::enable_if_t`就会定义一个类型，这样`foo`函数就可以被编译器接受。如果`T`不是整数类型，那么`std::is_integral<T>::value`就是`false`，`std::enable_if_t`就不会定义一个类型，这样`foo`函数就会被编译器忽略。

这样，我们就可以保证`foo`函数只接受整数类型的参数，如果我们尝试用非整数类型的参数调用`foo`函数，那么编译器就会报错。

注意，`std::enable_if_t`是C++14引入的，它是`std::enable_if`的一个别名，用于简化代码。在C++11中，我们需要写`typename std::enable_if<...>::type`，在C++14中，我们可以简化为`std::enable_if_t<...>`。这两者的功能是完全一样的。

## typename =
在C++模板中，`typename =` 的用法通常与 `std::enable_if_t` 结合使用，用于启用或禁用某个模板。这是一种基于条件的编译技术，也被称为 SFINAE（替换失败并非错误）。

下面是一个使用 `typename =` 的例子：

```cpp
#include <type_traits>
#include <iostream>

template <typename T, typename = std::enable_if_t<std::is_integral<T>::value>>
void print(const T& value) {
    std::cout << value << '\n';
}

int main() {
    print(1);  // 输出 "1"
    // print(1.0);  // 编译错误，因为1.0不是整数类型
    return 0;
}
```

在这个例子中，`print` 函数的模板参数列表中有一个 `typename = std::enable_if_t<std::is_integral<T>::value>`。这个表达式的作用是，如果 `T` 是整数类型，那么 `std::enable_if_t<std::is_integral<T>::value>` 就是 `void` 类型，`print` 函数就会被编译器接受。如果 `T` 不是整数类型，那么 `std::enable_if_t<std::is_integral<T>::value>` 就不定义任何类型，`print` 函数就会被编译器忽略，不会产生编译错误。

这种技术可以让我们的代码更加灵活，我们可以根据需要控制模板的启用条件。这是C++模板编程的一个重要特性，它使我们的代码更加通用和可重用。

## 组合使用
```cpp
template <
    class T,
    typename = std::enable_if_t<
        std::is_const<Iterator_element_type>::value &&
        std::is_same<typename T::value_type,
                      std::remove_const_t<Iterator_element_type>>::value>> 
```
这段代码是一个模板，它定义了一个从非常量迭代器到常量迭代器的隐式转换。这个转换在你想要从一个可以修改元素的迭代器（非const）得到一个不能修改元素的迭代器（const）时会被使用。

这段代码的写法有些复杂，这是为了避免声明迭代器的显式拷贝构造函数，因为在某些编译器中，这会导致其他地方出现编译器警告。

`std::enable_if_t`是一个模板，它用于启用或禁用某个函数模板。在这里，它被用来确保只有当`T::value_type`（非const迭代器的元素类型）和`std::remove_const_t<Iterator_element_type>`（去除const后的迭代器元素类型）相同时，这个隐式转换才会被启用。这就确保了只有当非const迭代器和const迭代器的元素类型相同时，这个转换才会被允许。如果这两个类型不同，那么这个转换就会被禁用，尝试使用这个转换将导致编译错误。这是一种类型安全的保证。 

这段代码的最后一行 `std::is_same<typename T::value_type, std::remove_const_t<Iterator_element_type>>::value` 是一个类型萃取，它检查 `T::value_type`（非const迭代器的元素类型）是否和 `std::remove_const_t<Iterator_element_type>`（去除const后的迭代器元素类型）是同一种类型。如果是，返回 `true`；否则，返回 `false`。这是为了确保我们不会错误地将一个类型的非const迭代器转换为另一个不同类型的const迭代器。 

总的来说，这段代码提供了一种安全的方式，使得非const迭代器可以被转换为const迭代器，同时保证了类型的一致性。这是一种常见的编程技巧，用于提高代码的健壮性和安全性。

## 萃取器
在C++中，"萃取器"（traits）是一种用于处理类型信息的技术。它们通常被用于泛型编程中，以便在编译时获取关于类型的信息。以下是一些常见的C++萃取器：

1. `std::iterator_traits`: 提供了一种方式来访问迭代器的一些类型。
2. `std::char_traits`: 提供了一种处理字符类型的方式，这对于字符串和流类非常有用。
3. `std::numeric_limits`: 提供了一种获取关于数值类型（如int，float等）的信息的方式。
4. `std::pointer_traits`: 提供了一种获取关于指针类型的信息的方式。
5. `std::allocator_traits`: 提供了一种获取关于分配器类型的信息的方式。
6. `std::type_traits`: 这是一个包含许多不同萃取器的头文件，每个萃取器都提供了关于类型的不同信息。例如：
    - `std::is_pointer`
    - `std::is_array`
    - `std::is_class`
    - `std::is_integral`
    - `std::is_floating_point`
    - `std::is_arithmetic`
    - `std::is_compound`
    - `std::is_const`
    - `std::is_volatile`
    - `std::is_pod`
    - `std::is_empty`
    - `std::is_polymorphic`
    - `std::is_abstract`
    - `std::is_signed`
    - `std::is_unsigned`

以上就是C++中常见的一些萃取器。它们都是模板，可以用于获取类型的各种属性。

## 运算符重载不会改变运算符的操作位置
运算符重载不会改变运算符的操作位置。例如，对于二元运算符（如`+`），无论是否进行重载，它的左操作数总是在运算符的左边，右操作数总是在运算符的右边。同样，对于一元运算符（如`++`和`--`），无论是前缀形式还是后缀形式，操作数的位置都是固定的。

运算符重载主要是改变了运算符的行为，使其能够用于自定义类型（如类）。但是，它并不改变运算符本身的语法，包括操作数的位置、运算符的优先级和结合性等。

# (*p)->m 和 p->m 是否等价

在C++中，`(*p)->m`和`p->m`的等价性取决于`p`的类型。

- 当`p`是一个指向指针的指针时，`(*p)->m`和`p->m`是不等价的。在这种情况下，`(*p)->m`是解引用`p`得到的指针，然后访问其成员`m`。而`p->m`试图直接从指针`p`访问成员`m`，这将导致编译错误，因为`p`不是一个结构体或类的实例。

```cpp
struct Test {
    int m;
};

Test a;
Test* p1 = &a;
Test** p2 = &p1;

(*p2)->m = 10;  // 正确
p2->m = 10;     // 错误
```

- 当`p`是一个指向结构体或类的指针时，`(*p)->m`和`p->m`是等价的。在这种情况下，`p->m`和`(*p).m`都是访问指针`p`所指向的结构体或类的成员`m`。

```cpp
struct Test {
    int m;
};

Test a;
Test* p = &a;

p->m = 10;      // 正确
(*p).m = 10;    // 正确，等价于 p->m
```

总的来说，`(*p)->m`和`p->m`的等价性取决于`p`的类型和你试图访问的是什么。如果`p`是一个指向结构体或类的指针，那么`p->m`和`(*p).m`是等价的。如果`p`是一个指向指针的指针，那么需要使用`(*p)->m`来访问成员`m`。在任何情况下，都不能使用`p->m`来从指向指针的指针`p`访问成员`m`。这将导致编译错误。因此，理解`p`的类型以及你试图访问的是什么非常重要。这将帮助你正确地使用`->`运算符来访问成员。

# std::stable_sort
`std::stable_sort`是C++标准库中的一个算法，用于对序列进行排序。与`std::sort`不同，`std::stable_sort`保证相等元素的相对顺序不变，这就是所谓的稳定性。

下面是一个简单的例子：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

struct Employee {
    int age;
    std::string name;
};

int main() {
    std::vector<Employee> v = {
        {30, "Bob"},
        {20, "Alice"},
        {20, "Tom"},
    };

    std::stable_sort(v.begin(), v.end(), [](const Employee& a, const Employee& b) {
        return a.age < b.age;
    });

    for (const auto& e : v) {
        std::cout << e.name << ", " << e.age << '\n';
    }

    return 0;
}
```

在这个例子中，我们有一个`Employee`结构体，包含`age`和`name`两个字段。我们创建了一个`Employee`对象的向量，并使用`std::stable_sort`按照年龄进行排序。因为`std::stable_sort`是稳定的，所以当两个员工的年龄相同时（比如Alice和Tom），他们在排序后的序列中的相对顺序保持不变。也就是说，Alice仍然在Tom之前，因为她在原始序列中就在Tom之前。这就是`std::stable_sort`的稳定性。

## TriviallyDestructible
`std::is_trivially_destructible` 是一个类型特性，用于在编译时检查给定类型的析构函数是否是平凡的。如果一个类型的析构函数是平凡的，那么它就不会执行任何动作，也不需要被显式调用。这对于优化代码非常有用。

下面是一个简单的例子：

```cpp
#include <type_traits>
#include <iostream>

struct TriviallyDestructible {
    int x;
};

struct NonTriviallyDestructible {
    ~NonTriviallyDestructible() {}
};

int main() {
    std::cout << std::boolalpha
              << "Is TriviallyDestructible trivially destructible? "
              << std::is_trivially_destructible<TriviallyDestructible>::value << '\n'
              << "Is NonTriviallyDestructible trivially destructible? "
              << std::is_trivially_destructible<NonTriviallyDestructible>::value << '\n';
    return 0;
}
```

在这个例子中，`TriviallyDestructible` 是一个平凡的析构函数，因为它没有定义析构函数。而 `NonTriviallyDestructible` 不是一个平凡的析构函数，因为它定义了一个析构函数，即使这个析构函数什么都没做。所以，当你运行这段代码时，你会看到以下输出：

```
Is TriviallyDestructible trivially destructible? true
Is NonTriviallyDestructible trivially destructible? false
```

# 函数返回  副本、指针、引用
函数可以返回值、引用或指针，具体返回什么取决于函数的设计和它的使用场景
返回值：当函数需要返回一个新的对象（例如，通过计算或组合输入参数得到的结果）时，通常会返回值。这意味着函数会返回这个对象的一个副本。例如：
```cpp
int add(int a, int b) {
    return a + b;
}
```

# 函数名字前面或者后面加 const
在 C++ 中，`const` 关键字可以用于修饰函数，具体的使用方式和含义如下：

- **在函数参数列表后面使用 `const`**：这表示该函数不会修改它所属对象的状态。这种函数被称为常量成员函数。例如：

```cpp
class MyClass {
public:
    int getValue() const {
        return value;
    }

private:
    int value;
};
```

在这个例子中，`getValue` 是一个常量成员函数，它不能修改 `MyClass` 的任何成员变量。

- **在函数参数类型前面使用 `const`**：这表示该函数的参数是常量，函数内部不能修改这个参数的值。例如：

```cpp
void printValue(const int value) {
    std::cout << value << std::endl;
}
```

在这个例子中，`printValue` 函数的参数 `value` 是一个常量，函数内部不能修改 `value` 的值。

# 模板参数包 和  完美转发
```cpp
template <typename... Args>
  bool emplace_back(Args &&... args) {
    constexpr size_t min_capacity = 20;
    constexpr size_t expansion_factor = 2;
    if (m_size == m_capacity) {
      if (reserve(std::max(min_capacity, m_capacity * expansion_factor))) {
        return true;
      }
    }
    Element_type *p = &m_array[m_size++];
    ::new (p) Element_type(std::forward<Args>(args)...);
    return false;
  }
```
这段代码中的 `typename... Args` 和 `std::forward<Args>(args)...` 是 C++ 的模板和完美转发特性。

- **`typename... Args`**：这是一个变长模板参数，也被称为模板参数包。它可以接受任意数量和类型的参数。在这个例子中，`Args` 是一个模板参数包，代表了一组类型。

- **`std::forward<Args>(args)...`**：这是 C++ 的完美转发特性。完美转发可以保持参数的原始类型（包括左值和右值），并将参数传递给另一个函数。在这个例子中，`std::forward<Args>(args)...` 将所有的参数以它们原始的类型转发给 `Element_type` 的构造函数。

这段代码的功能是在容器的末尾添加一个新元素。如果容器的容量不足，它会自动扩容。然后，它使用完美转发将所有参数传递给 `Element_type` 的构造函数，以在容器的末尾就地构造一个新元素。

# 友元
在 C++ 中，友元（friend）是一种允许某些非成员函数或其他类访问类的私有或保护成员的机制。

# const std::nothrow_t &arg [[maybe_unused]] = std::nothrow
```cpp
static void *operator new(size_t size, MEM_ROOT *mem_root,
                            const std::nothrow_t &arg
                            [[maybe_unused]] = std::nothrow) noexcept {
    return mem_root->Alloc(size);
  }
```
这个函数是一个重载的 `new` 操作符，它接受三个参数：要分配的内存大小、一个 `MEM_ROOT` 指针和一个 `std::nothrow_t` 引用。

- `size_t size`：这是要分配的内存的大小。
- `MEM_ROOT *mem_root`：这是一个指向 `MEM_ROOT` 类型的指针，`MEM_ROOT` 是一个用于内存分配的类。
- `const std::nothrow_t &arg [[maybe_unused]] = std::nothrow`：这是一个 `std::nothrow_t` 类型的引用，它是 `new` 操作符的一个标准参数。当你使用 `new (std::nothrow)` 来分配内存时，如果内存分配失败，`new` 不会抛出异常，而是返回一个空指针。`[[maybe_unused]]` 是一个属性，用于告诉编译器这个参数可能不会被使用，这样即使在没有使用这个参数的情况下，编译器也不会产生警告。

这个函数的作用是在 `MEM_ROOT` 指向的内存区域中分配指定大小的内存，并返回分配的内存的指针。如果内存分配失败，它不会抛出异常，而是返回一个空指针。

# noexcept
`noexcept` 是 C++11 引入的一个关键字，用于指定函数是否会抛出异常。

如果你在函数声明后面加上 `noexcept`，那么这个函数就被声明为不会抛出任何异常。如果这个函数确实抛出了异常，那么程序会立即调用 `std::terminate` 来结束程序。

例如：

```cpp
void myFunction() noexcept {
    // 这个函数不会抛出异常
}
```

`noexcept` 的主要用途是优化代码。如果编译器知道一个函数不会抛出异常，那么它就可以生成更优化的代码。此外，一些 C++ 特性（如移动语义和 `std::vector::push_back`）需要知道函数是否可能抛出异常来决定使用哪种策略。

# namespace {int stack_direction = 0;}
这段代码定义了一个未命名的命名空间（也被称为匿名命名空间），并在其中声明了一个整型变量 `stack_direction`。

未命名的命名空间在 C++ 中有特殊的含义。在同一个文件或编译单元中，未命名的命名空间可以被视为一个普通的命名空间，你可以在任何地方使用它的成员。但是，在不同的文件或编译单元中，每个未命名的命名空间都是唯一的，你不能访问其他文件或编译单元中未命名的命名空间的成员。

因此，这段代码的含义是：在这个文件或编译单元中，定义了一个整型变量 `stack_direction`，并将其初始化为 `0`。这个变量只能在这个文件或编译单元中访问，不能在其他文件或编译单元中访问。

# __attribute__((noinline))
`__attribute__((noinline))` 是 GCC 编译器的一个特性，用于告诉编译器不要内联某个函数。内联是一种优化技术，可以减少函数调用的开销，但有时我们可能不希望编译器进行这种优化。

例如，下面的代码定义了一个不会被内联的函数：

```cpp
__attribute__((noinline)) void myFunction() {
    // 这个函数不会被内联
}
```

在这个例子中，`myFunction` 函数被声明为 `noinline`，所以编译器在优化代码时不会将其内联。

需要注意的是，`__attribute__((noinline))` 是 GCC 特有的，不是 C++ 标准的一部分，所以在其他编译器（如 MSVC 或 Clang）上可能不起作用。

# std::deque
在 C++ 的标准模板库（STL）中，`std::deque`（通常读作 "deck"）是一个双端队列（double-ended queue），它是一种序列容器，允许在其开始和结束处进行快速插入和删除。

与 `std::vector` 相比，`std::deque` 在插入和删除元素时更高效。此外，`std::deque` 的元素不一定连续存储：典型的实现使用一系列单独分配的固定大小数组，有额外的记录，这意味着对 `deque` 的索引访问必须执行两次指针解引用，而 `vector` 的索引访问只执行一次。

以下是一个简单的 `std::deque` 使用示例：

```cpp
#include <deque>
#include <iostream>

int main() {
    std::deque<int> d;

    // 在队列的前后添加元素
    d.push_front(1);
    d.push_back(2);

    // 输出队列的元素
    for (int i : d) {
        std::cout << i << ' ';
    }

    return 0;
}
```

在这个示例中，我们创建了一个 `std::deque`，然后在队列的前后添加了元素，最后输出了队列的所有元素。

# for (int i : d)
它是一种简洁的方式来遍历一个容器（如数组或 std::vector）或任何其他可以迭代的对象。

范围 `for` 循环是在 C++11 标准中引入的。这种 `for` 循环可以让我们更简洁地遍历一个序列，如数组或向量，而无需显式使用迭代器或随机访问运算符。

# ptype 使用
```sh
# 只显示数据成员
ptype /m var

# 显示父类
set print object on

# 不显示父类
set print object off
```

其它技巧
`ptype`命令的可选参数有以下几种：
- `/r`：以原始数据的方式显示，不会代替一些typedef定义。
- `/m`：查看类时，不显示类的方法，只显示类的成员变量。
- `/M`：与`/m`相反，显示类的方法（默认选项）。
- `/t`：不打印类中的typedef数据。
- `/o`：打印结构体字段的偏移量和大小。

此外，`ptype`命令还支持`/x`和`/d`，这两个参数影响用于打印尺寸和偏移量的基数。希望这个信息对你有所帮助！

# virtual + final
在C++中，如果一个函数后面加了`final`，那么它就已经被隐式地声明为`virtual`。因此，如果你在函数后面加了`final`，那么在函数前面加`virtual`就没有必要了。

但是，为了代码的可读性和清晰性，有些开发者可能仍然会在函数前面加上`virtual`，以明确表示这个函数是虚函数。这主要取决于你的编码风格和团队的编码规范。

总的来说，如果一个函数后面加了`final`，那么无论它前面是否加了`virtual`，它都是虚函数，并且不能被派生类重写。

# 单向链表中的双指针
```cpp
双指针在很多情况下可以使代码更加直接和高效。让我们通过一个简单的链表节点删除的例子来说明这一点。

假设我们有一个单向链表，我们想要删除一个特定的节点。如果我们只有一个指向该节点的单指针，我们需要从链表的头部开始遍历，找到要删除节点的前一个节点，然后修改它的`next`指针来删除节点。这需要我们遍历整个链表，时间复杂度是O(n)。

```cpp
struct Node {
  int value;
  Node* next;
};

void deleteNode(Node* head, Node* toDelete) {
  if (head == toDelete) {
    head = head->next;
    delete toDelete;
    return;
  }

  Node* prev = head;
  while (prev->next != toDelete) {
    prev = prev->next;
  }

  prev->next = toDelete->next;
  delete toDelete;
}
```

但是，如果我们有一个指向要删除节点的前一个节点的`next`指针的指针（也就是双指针），我们可以直接修改这个双指针来删除节点，无需遍历链表。

```cpp
void deleteNode(Node** prevNext, Node* toDelete) {
  *prevNext = toDelete->next;
  delete toDelete;
}
```

这就是为什么双指针在某些情况下可以使代码更加直接和高效的原因。

# GDB 调试 MySQL
```sh
gdb

file /data/mysql-server-8.2.0/build/runtime_output_directory/mysqld-debug

b sql_lex.cc:5041

run --user=mysql --datadir=/data/mysql-server-8.2.0/build/runtime_output_directory/../../data --socket=/data/mysql-server-8.2.0/build/runtime_output_directory/../../data/mysql.sock.lock
```
# 左值、右值、完美转发
简单来说，左值是指可以取地址的、具有持久性的对象，而右值是指不能取地址的、临时生成的对象。

```cpp
template <typename T>
void forward_to_print(T &&arg) {
    print(std::forward<T>(arg));
}

std::string str = "Hello, world!";
forward_to_print(str);  // 传入左值
forward_to_print("Hello, world!");  // 传入右值
```
std::forward的工作原理是这样的：如果参数是一个左值引用，std::forward将返回一个左值引用；如果参数是一个右值引用，std::forward将返回一个右值引用。这样，无论输入的参数是左值还是右值，std::forward都能保证参数的原始性质在传递过程中得以保留。

## 举例介绍

左值是指可以用内置的&运算符取地址的表达式，例如变量、数组元素、字符串字面量等。右值是指不能用内置的&运算符取地址的表达式，例如临时变量、函数返回值、算术表达式等。完美转发是指在函数参数传递时，保持原来参数的类型和值属性不变，即不改变参数的左值或右值性质。

如果不使用完美转发，那么函数不能正确地将参数转发给print函数。例如，假设有以下代码：

```c++
#include <iostream>
#include <type_traits>

template<typename T>
void print(T &&t) {
    std::cout << "Left value" << std::endl;
}

template<typename T>
void print(T &t) {
    std::cout << "Right value" << std::endl;
}

int main() {
    int x = 10;
    print(x); // 调用print函数时，x是一个右值
    print(x); // 调用print函数时，x仍然是一个右值
}

// 结果：
// Right value
// Right value
```

在这个例子中，如果不使用完美转发，那么第一次调用print函数时，x会被转换为一个左值引用，并传递给print函数；第二次调用print函数时，x仍然是一个右值，并传递给print函数。这样就会导致编译错误或者输出错误的结果。

为了避免这种情况，我们可以使用std::forward<T>来实现完美转发。std::forward<T>是一个模板函数，它可以根据参数的类型自动选择合适的转换方式。例如：

```c++
#include <iostream>
#include <type_traits>

template<typename T>
void print(T &&t) {
    std::cout << "Left value" << std::endl;
}

template<typename T>
void print(T &t) {
    std::cout << "Right value" << std::endl;
}

int main() {
    int x = 10;
    print(std::forward<int>(x)); // 调用print函数时，x被转换为一个左值引用
    print(std::forward<int>(x)); // 调用print函数时，x仍然被转换为一个左值引用
}

// 结果：
// Left value
// Left value
```

在这个例子中，我们使用std::forward<int>来将x作为一个左值引用传递给print函数。这样就可以保证每次调用print函数时都得到正确的结果。