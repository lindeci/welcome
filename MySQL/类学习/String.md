- [String](#string)

# String
```cpp
class String { // 定义一个名为String的类

private: // 私有成员

char *m_ptr; // 字符串的指针
size_t m_length; // 字符串的长度
const CHARSET_INFO *m_charset; // 字符集信息
uint32 m_alloced_length; // 已分配的内存长度
bool m_is_alloced; // 是否已分配内存

public: // 公有成员

String(void); // 默认构造函数
String(size_t); // 构造函数，接收一个size_t类型的参数
String(const char , const CHARSET_INFO ); // 构造函数，接收一个字符和字符集信息作为参数
String(const char , size_t, const CHARSET_INFO ); // 构造函数，接收一个字符、长度和字符集信息作为参数
String(char , size_t, const CHARSET_INFO ); // 构造函数，接收一个字符、长度和字符集信息作为参数
String(const String &); // 拷贝构造函数
String(String &&); // 移动构造函数
static void operator new(size_t, MEM_ROOT , const std::nothrow_t &); // 重载new操作符
static void operator delete(void *, size_t); // 重载delete操作符
static void operator delete(void , MEM_ROOT , const std::nothrow_t &); // 重载delete操作符
~String(); // 析构函数

void set_charset(const CHARSET_INFO *); // 设置字符集
const CHARSET_INFO * charset(void) const; // 获取字符集
size_t length(void) const; // 获取字符串长度
void length(size_t); // 设置字符串长度
size_t alloced_length(void) const; // 获取已分配的内存长度
const char & operator const; // 重载[]操作符，获取指定位置的字符
char & operator; // 重载[]操作符，获取指定位置的字符
bool is_empty(void) const; // 判断字符串是否为空
void mark_as_const(void); // 标记为常量
const char * ptr(void) const; // 获取字符串指针
char * ptr(void); // 获取字符串指针
char * c_ptr(void); // 获取C风格的字符串指针
char * c_ptr_quick(void); // 快速获取C风格的字符串指针
char * c_ptr_safe(void); // 安全地获取C风格的字符串指针
LEX_STRING lex_string(void); // 获取LEX_STRING类型的字符串
LEX_CSTRING lex_cstring(void) const; // 获取LEX_CSTRING类型的字符串
void set(String &, size_t, size_t); // 设置字符串
void set(char , size_t, const CHARSET_INFO ); // 设置字符串
void set(const char , size_t, const CHARSET_INFO ); // 设置字符串
bool set(longlong, const CHARSET_INFO *); // 设置字符串
bool set(ulonglong, const CHARSET_INFO *); // 设置字符串
bool set_ascii(const char *, size_t); // 设置ASCII字符串
void set_quick(char , size_t, const CHARSET_INFO ); // 快速设置字符串
bool set_int(longlong, bool, const CHARSET_INFO *); // 设置整数字符串
bool set_real(double, uint, const CHARSET_INFO *); // 设置实数字符串
void chop(void); // 截断字符串
void mem_claim(bool); // 声明内存
void mem_free(void); // 释放内存
bool alloc(size_t); // 分配内存
bool real_alloc(size_t); // 真实分配内存
bool mem_realloc(size_t, bool); // 重新分配内存

private: // 私有成员

size_t next_realloc_exp_size(size_t); // 获取下一次重新分配内存的期望大小
bool mem_realloc_exp(size_t); // 期望重新分配内存

public: // 公有成员

void shrink(size_t); // 缩小字符串
bool is_alloced(void) const; // 判断是否已分配内存
String & operator=(const String &); // 重载=操作符，赋值操作
String & operator=(String &&); // 重载=操作符，移动赋值操作
void takeover(String &); // 接管另一个String对象
bool copy(void); // 复制字符串
bool copy(const String &); // 复制字符串
bool copy(const char , size_t, const CHARSET_INFO ); // 复制字符串
bool copy(const char , size_t, const CHARSET_INFO , const CHARSET_INFO , uint ); // 复制字符串
static bool needs_conversion(size_t, const CHARSET_INFO , const CHARSET_INFO , size_t *); // 判断是否需要转换
bool needs_conversion(const CHARSET_INFO *) const; // 判断是否需要转换
bool is_valid_string(const CHARSET_INFO *) const; // 判断是否是有效的字符串
static bool needs_conversion_on_storage(size_t, const CHARSET_INFO , const CHARSET_INFO ); // 判断存储时是否需要转换
bool copy_aligned(const char , size_t, size_t, const CHARSET_INFO ); // 复制对齐的字符串
bool set_or_copy_aligned(const char , size_t, const CHARSET_INFO ); // 设置或复制对齐的字符串
bool append(const String &); // 追加字符串
bool append(std::string_view); // 追加字符串
bool append(LEX_STRING *); // 追加字符串
bool append(Simple_cstring); // 追加字符串
bool append(const char *, size_t); // 追加字符串
bool append(const char , size_t, const CHARSET_INFO ); // 追加字符串
bool append(char); // 追加字符
bool append(const char *, size_t, size_t); // 追加字符串
bool append_ulonglong(ulonglong); // 追加无符号长整数
bool append_longlong(longlong); // 追加长整数
bool append_with_prefill(const char *, size_t, size_t, char); // 追加字符串，并预填充字符
bool append_parenthesized(int64_t); // 追加带括号的整数
int strstr(const String &, size_t) const; // 查找子字符串
int strrstr(const String &, size_t) const; // 从后向前查找子字符串
String substr(int, int) const; // 获取子字符串
bool replace(size_t, size_t, const char *, size_t); // 替换子字符串
bool replace(size_t, size_t, const String &); // 替换子字符串
bool fill(size_t, char); // 填充字符串
size_t numchars(void) const; // 获取字符数量
size_t charpos(size_t, size_t) const; // 获取字符位置
bool reserve(size_t); // 预留空间
bool reserve(size_t, size_t); // 预留空间
char * prep_append(size_t, size_t); // 准备追加字符串
void print(String *) const; // 打印字符串
void swap(String &); // 交换字符串
bool uses_buffer_owned_by(const String *) const; // 判断是否使用了其他String对象的缓冲区
bool is_ascii(void) const; // 判断是否是ASCII字符串
char dup(MEM_ROOT ) const; // 复制字符串

} // 类定义结束
```