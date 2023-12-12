- [Mem\_root\_array\<Element\_type\>](#mem_root_arrayelement_type)
- [Mem\_root\_array\_YY\<Element\_type\>](#mem_root_array_yyelement_type)
- [Parse\_tree\_node\_tmpl](#parse_tree_node_tmpl)
- [class mem\_root\_deque](#class-mem_root_deque)
- [List\<PT\_key\_part\_specification\>](#listpt_key_part_specification)
- [base\_list](#base_list)
- [list\_node](#list_node)
- [collation\_unordered\_map](#collation_unordered_map)
- [base\_list\_iterator](#base_list_iterator)
- [List\_iterator](#list_iterator)
- [SQL\_I\_List\<Table\_ref\>](#sql_i_listtable_ref)

# Mem_root_array<Element_type>
```cpp
class Mem_root_array<String> [with Element_type = String] : public Mem_root_array_YY<Element_type> {
  public:
    Mem_root_array(void);  // 默认构造函数
    Mem_root_array(MEM_ROOT *);  // 带参数的构造函数
    Mem_root_array(Mem_root_array<Element_type> &&);  // 移动构造函数
    Mem_root_array(MEM_ROOT *, size_t);  // 带两个参数的构造函数
    Mem_root_array(MEM_ROOT *, size_t, const Element_type &);  // 带三个参数的构造函数
    Mem_root_array(MEM_ROOT *, const_iterator, const_iterator);  // 带三个参数的构造函数
    Mem_root_array(MEM_ROOT *, const Mem_root_array<Element_type> &);  // 带两个参数的构造函数
    Mem_root_array(std::initializer_list<Element_type>);  // 列表初始化构造函数
    Mem_root_array(const Mem_root_array<Element_type> &);  // 拷贝构造函数
    Mem_root_array<Element_type> & operator=(Mem_root_array<Element_type> &&);  // 移动赋值运算符重载
    Mem_root_array<Element_type> & operator=(const Mem_root_array<Element_type> &);  // 赋值运算符重载
    ~Mem_root_array();  // 析构函数

    typedef Element_type value_type;  // 值类型定义
    typedef Mem_root_array_YY<Element_type>::const_iterator const_iterator;  // 常量迭代器类型定义
}
```

# Mem_root_array_YY<Element_type>
```cpp
class Mem_root_array_YY<String> [with Element_type = String] {
  private:
    static const bool has_trivial_destructor;  // 是否具有平凡析构函数

  protected:
    MEM_ROOT *m_root;  // 内存根指针
    const_iterator m_array;  // 常量迭代器指针
    size_t m_size;  // 大小
    size_t m_capacity;  // 容量

  public:
    void init(MEM_ROOT *);  // 初始化函数
    void init_empty_const(void);  // 初始化空常量函数
    const_iterator data(void);  // 数据指针
    const_iterator data(void) const;  // 常量数据指针
    Element_type & at(size_t);  // 获取特定位置元素的引用
    const Element_type & at(size_t) const;  // 获取特定位置元素的常量引用
    Element_type & operator[](size_t);  // 重载下标操作符
    const Element_type & operator[](size_t) const;  // 重载下标操作符（常量版本）
    Element_type & back(void);  // 获取末尾元素的引用
    const Element_type & back(void) const;  // 获取末尾元素的常量引用
    const_iterator begin(void);  // 起始迭代器
    const_iterator begin(void) const;  // 起始迭代器（常量版本）
    const_iterator end(void);  // 结束迭代器
    const_iterator end(void) const;  // 结束迭代器（常量版本）
    const_iterator cbegin(void) const;  // 常量起始迭代器
    const_iterator cend(void) const;  // 常量结束迭代器
    void clear(void);  // 清空容器
    void chop(size_t);  // 裁剪函数
    bool reserve(size_t);  // 预留空间
    bool push_back(const Element_type &);  // 在尾部插入元素
    bool push_back(Element_type &&);  // 在尾部移动插入元素
    bool push_front(const Element_type &);  // 在开头插入元素
    bool push_front(Element_type &&);  // 在开头移动插入元素
    void pop_back(void);  // 弹出尾部元素
    void resize(size_t, const Element_type &);  // 调整大小，并使用特定值填充
    void resize(size_t);  // 调整大小
    const_iterator erase(const_iterator, const_iterator);  // 删除指定范围内的元素
    const_iterator erase(const_iterator);  // 删除指定位置的元素
    const_iterator erase(size_t);  // 删除特定位置的元素
    const_iterator erase(const_iterator);  // 删除指定位置的元素
    const_iterator insert(const_iterator, const Element_type &);  // 插入元素
    size_t erase_value(const Element_type &);  // 删除特定值的元素个数
    size_t capacity(void) const;  // 容量大小
    size_t element_size(void) const;  // 元素大小
    bool empty(void) const;  // 是否为空
    size_t size(void) const;  // 大小
    bool emplace_back<String>(Element_type &&);  // 在尾部就地构造元素

    typedef const Element_type *const_iterator;  // 常量迭代器类型定义
    typedef Element_type value_type;  // 值类型定义
    typedef Element_type *iterator;  // 迭代器类型定义
}
```

# Parse_tree_node_tmpl
```cpp
class Parse_tree_node_tmpl<Context> [with Context = Table_ddl_parse_context] {
  private:
    bool contextualized;  // 上下文化标识

  public:
    POS m_pos;  // 位置

  private:
    Parse_tree_node_tmpl(const Parse_tree_node_tmpl<Context> &);  // 拷贝构造函数

  protected:
    Parse_tree_node_tmpl(void);  // 默认构造函数
    Parse_tree_node_tmpl(const POS &);  // 构造函数，带位置参数
    Parse_tree_node_tmpl(const POS &, const POS &);  // 构造函数，带两个位置参数

  private:
    void operator=(const Parse_tree_node_tmpl<Context> &);  // 赋值运算符重载

  public:
    static void * operator new(size_t, MEM_ROOT *, const std::nothrow_t &);  // new运算符重载
    static void operator delete(void *, size_t);  // delete运算符重载
    static void operator delete(void *, MEM_ROOT *, const std::nothrow_t &);  // delete运算符重载

  protected:
    bool begin_parse_tree(Show_parse_tree *);  // 开始解析树
    bool end_parse_tree(Show_parse_tree *);  // 结束解析树
    virtual bool do_contextualize(Context *);  // 执行上下文化
    virtual void add_json_info(Json_object *);  // 添加JSON信息

  public:
    ~Parse_tree_node_tmpl();  // 析构函数
    bool is_contextualized(void) const;  // 是否已上下文化
    virtual bool contextualize(Context *);  // 上下文化
    void error(Context *, const POS &) const;  // 错误处理函数
    void error(Context *, const POS &, const char *) const;  // 错误处理函数，带字符串参数
    void errorf(Context *, const POS &, const char *, ...) const;  // 格式化错误处理函数

    typedef Context context_t;  // 上下文类型定义
}
```

# class mem_root_deque
```cpp
class mem_root_deque<Item*> [with Element_type = Item *] {
  private:
    static const size_t block_elements; /**< 块中的元素数量上限 */
    mem_root_deque<Item*>::Block *m_blocks; /**< 块数组指针 */
    size_t m_begin_idx; /**< 开始索引 */
    size_t m_end_idx; /**< 结束索引 */
    size_t m_capacity; /**< 容量 */
    MEM_ROOT *m_root; /**< 内存根节点 */
    size_t m_generation; /**< 代数，用于标识当前状态的变化

  public:
    mem_root_deque(MEM_ROOT *); /**< 构造函数，接受一个内存根节点作为参数 */
    mem_root_deque(const mem_root_deque<Item*> &); /**< 拷贝构造函数 */
    mem_root_deque(mem_root_deque<Item*> &&); /**< 移动构造函数 */
    mem_root_deque<Item*> & operator=(const mem_root_deque<Item*> &); /**< 赋值运算符 */
    mem_root_deque<Item*> & operator=(mem_root_deque<Item*> &&); /**< 移动赋值运算符 */
    ~mem_root_deque(); /**< 析构函数 */
    Item *& operator[](size_t) const; /**< 重载下标运算符，获取指定位置的元素引用 */
    bool push_back(Item * const&); /**< 后端插入元素的函数，接受常引用参数 */
    bool push_back(Item *&&); /**< 后端插入元素的函数，接受右值引用参数 */
    bool push_front(Item * const&); /**< 前端插入元素的函数，接受常引用参数 */
    bool push_front(Item *&&); /**< 前端插入元素的函数，接受右值引用参数 */
    void pop_back(void); /**< 后端删除元素的函数 */
    void pop_front(void); /**< 前端删除元素的函数 */
    Item *& front(void); /**< 获取队列前端元素的引用 */
    Item * const& front(void) const; /**< 获取队列前端元素的常引用 */
    Item *& back(void); /**< 获取队列后端元素的引用 */
    Item * const& back(void) const; /**< 获取队列后端元素的常引用 */
    void clear(void); /**< 清空队列 */
    iterator begin(void); /**< 获取队列起始迭代器 */
    const_iterator begin(void) const; /**< 获取队列起始迭代器，常版本 */
    iterator end(void); /**< 获取队列结束迭代器 */
    const_iterator end(void) const; /**< 获取队列结束迭代器，常版本 */
    reverse_iterator rbegin(void); /**< 获取反向迭代器的起始位置 */
    reverse_const_iterator rbegin(void) const; /**< 获取反向迭代器的起始位置，常版本 */
    reverse_iterator rend(void); /**< 获取反向迭代器的结束位置 */
    reverse_const_iterator rend(void) const; /**< 获取反向迭代器的结束位置，常版本 */
    const_iterator cbegin(void); /**< 获取常版本的起始迭代器 */
    const_iterator cend(void); /**< 获取常版本的结束迭代器 */
    reverse_const_iterator crbegin(void) const; /**< 获取常版本的反向迭代器的起始位置 */
    reverse_const_iterator crend(void) const; /**< 获取常版本的反向迭代器的结束位置 */
    size_t size(void) const; /**< 获取队列中的元素数量 */
    bool empty(void) const; /**< 判断队列是否为空 */
    iterator erase(const_iterator, const_iterator); /**< 删除指定范围内的元素 */
    iterator erase(const_iterator); /**< 删除指定位置的元素 */
    iterator insert(const_iterator, Item * const&); /**< 在指定位置插入元素，接受常引用参数 */
    iterator insert(const_iterator, Item *&&); /**< 在指定位置插入元素，接受右值引用参数 */

  private:
    void invalidate_iterators(void); /**< 使迭代器失效 */
    bool add_initial_block(void); /**< 添加初始块 */
    bool add_block_back(void); /**< 后端添加块 */
    bool add_block_front(void); /**< 前端添加块 */
    size_t num_blocks(void) const; /**< 获取块的数量 */
    Item *& get(size_t) const; /**< 获取指定位置的元素引用 */
    size_t generation(void) const; /**< 获取代数信息 */

  public:
    typedef mem_root_deque<Item*>::Iterator<Item*> iterator; /**< 定义迭代器类型 */
    typedef std::reverse_iterator<mem_root_deque<Item*>::Iterator<Item*> > reverse_iterator; /**< 定义反向迭代器类型 */
    typedef mem_root_deque<Item*>::Iterator<Item* const> const_iterator; /**< 定义常版本迭代器类型 */
    typedef std::reverse_iterator<mem_root_deque<Item*>::Iterator<Item* const> > reverse_const_iterator; /**< 定义常版本反向迭代器类型 */
}
```

# List<PT_key_part_specification>
```cpp
class List<PT_key_part_specification> [with T = PT_key_part_specification] : public base_list {
  public:
    List(void);
    List(const List<T> &);
    List(const List<T> &, MEM_ROOT *);
    List<T> & operator=(const List<T> &);
    bool push_back(T *);
    bool push_back(T *, MEM_ROOT *);
    bool push_front(T *);
    bool push_front(T *, MEM_ROOT *);
    T * head(void);
    const T * head(void) const;
    T ** head_ref(void);
    T * pop(void);
    void concat(List<T> *);
    void disjoin(List<T> *);
    void prepend(List<T> *);
    void delete_elements(void);
    void destroy_elements(void);
    T * operator[](uint) const;
    void replace(uint, T *);
    bool swap_elts(uint, uint);
    iterator begin(void);
    const_iterator begin(void) const;
    iterator end(void);
    const_iterator end(void) const;
    const_iterator cbegin(void) const;
    const_iterator cend(void) const;

    typedef List_STL_Iterator<T> iterator;
    typedef List_STL_Iterator<T const> const_iterator;
}
```
代码例子
```cpp
List_iterator<Create_field> it(alter_info->create_list);
  for (; (sql_field = it++); field_no++) {
```
```cpp
for (const Create_field &new_field_def : alter_info->create_list) {
```

# base_list
```cpp
class base_list {
  protected:
    list_node *first;
    list_node **last;
  public:
    uint elements;

    bool operator==(const base_list &) const;
    void clear(void);
    base_list(void);
    base_list(const base_list &);
    base_list(const base_list &, MEM_ROOT *);
    base_list & operator=(const base_list &);
    bool push_back(void *);
    bool push_back(void *, MEM_ROOT *);
    bool push_front(void *);
    bool push_front(void *, MEM_ROOT *);
    void remove(list_node **);
    void concat(base_list *);
    void * pop(void);
    void disjoin(base_list *);
    void prepend(base_list *);
    void swap(base_list &);
    list_node * last_node(void);
    list_node * first_node(void);
    void * head(void);
    const void * head(void) const;
    void ** head_ref(void);
    bool is_empty(void) const;
    list_node * last_ref(void);
    uint size(void) const;
  protected:
    void after(void *, list_node *);
    bool after(void *, list_node *, MEM_ROOT *);
}
```

# list_node
```cpp
struct list_node {
    list_node *next;
    void *info;
  public:
    list_node(void *, list_node *);
    list_node(void);
}
```

# collation_unordered_map
```cpp
/**
  std::unordered_map, but with my_malloc and collation-aware comparison.
*/
template <class Key, class Value>
class collation_unordered_map
    : public std::unordered_map<Key, Value, Collation_hasher,
                                Collation_key_equal,
                                Malloc_allocator<std::pair<const Key, Value>>> {
 public:
  collation_unordered_map(const CHARSET_INFO *cs, PSI_memory_key psi_key)
      : std::unordered_map<Key, Value, Collation_hasher, Collation_key_equal,
                           Malloc_allocator<std::pair<const Key, Value>>>(
            /*bucket_count=*/10, Collation_hasher(cs), Collation_key_equal(cs),
            Malloc_allocator<>(psi_key)) {}
};
```



# base_list_iterator
```cpp
class base_list_iterator {
  protected:
    base_list *list;
    list_node **el;
    list_node **prev;
    list_node *current;

    void sublist(base_list &, uint);
  public:
    base_list_iterator(void);
    base_list_iterator(base_list &);
    void init(base_list &);
    void * next(void);
    void * next_fast(void);
    void rewind(void);
    void * replace(void *);
    void * replace(base_list &);
    void remove(void);
    void after(void *);
    bool after(void *, MEM_ROOT *);
    void ** ref(void);
    bool is_last(void);
    bool is_before_first(void) const;
    bool prepend(void *, MEM_ROOT *);
}
```
```cpp
inline void *next(void) {
    prev = el;
    current = *el;
    el = &current->next;
    return current->info;
  }
```

# List_iterator
```cpp
template <class T>
class List_iterator : public base_list_iterator {
 public:
  List_iterator(List<T> &a) : base_list_iterator(a) {}
  List_iterator() : base_list_iterator() {}
  inline void init(List<T> &a) { base_list_iterator::init(a); }
  inline T *operator++(int) { return (T *)base_list_iterator::next(); }
  inline T *replace(T *a) { return (T *)base_list_iterator::replace(a); }
  inline T *replace(List<T> &a) { return (T *)base_list_iterator::replace(a); }
  inline void rewind(void) { base_list_iterator::rewind(); }
  inline void remove() { base_list_iterator::remove(); }
  inline void after(T *a) { base_list_iterator::after(a); }
  inline bool after(T *a, MEM_ROOT *mem_root) {
    return base_list_iterator::after(a, mem_root);
  }
  inline T **ref(void) {
    return const_cast<T **>(
        (std::remove_const_t<T> **)base_list_iterator::ref());
  }
};
```

# SQL_I_List<Table_ref>
```cpp
class SQL_I_List<Table_ref> [with T = Table_ref] {
  public:
    uint elements;
    T *first;
    T **next;

    SQL_I_List(void);
    SQL_I_List(const SQL_I_List<T> &);
    SQL_I_List(SQL_I_List<T> &&);
    void clear(void);
    void link_in_list(T *, T **);
    void save_and_clear(SQL_I_List<T> *);
    void push_front(SQL_I_List<T> *);
    void push_back(SQL_I_List<T> *);
    uint size(void) const;
    SQL_I_List<T> & operator=(SQL_I_List<T> &);
    SQL_I_List<T> & operator=(SQL_I_List<T> &&);
}
```