- [折叠](#折叠)
- [Todo list](#todo-list)
      - [markdown todolist 示例](#markdown-todolist-示例)
- [插入标题](#插入标题)
- [分隔符](#分隔符)
- [换行](#换行)
- [文本对齐方式](#文本对齐方式)
- [表格](#表格)
- [代码](#代码)
- [强调](#强调)
- [列表](#列表)
- [标题](#标题)
- [引用](#引用)
- [图片与链接](#图片与链接)

# 折叠
<details>
<summary>菜单</summary>
菜单内容
</details>

<details>
<summary>源码</summary>

```cpp
a=1;
b=2;
```
</details>

# Todo list
#### markdown todolist 示例
- [ ] 待完成
- [x] 已完成
- [ ] ~~未完成~~

# 插入标题
```sh
Ctrl+Shift+p
然后选择 Markdown All in One:Create Table of Contens
```

# 分隔符
---
***
___
* * *

# 换行
在行尾添加两个空格加回车表示换行

# 文本对齐方式
<p align="left">居左文本</p>
<p align="center">居中文本</p>
<p align="right">居右文本</p>

# 表格
表格对齐格式

    居左：:----
    居中：:----:或-----
    居右：----:

例子：

|标题|标题|标题|
|:---|:---:|---:|
|居左测试文本|居中测试文本|居右测试文本|
|居左测试文本1|居中测试文本2|居右测试文本3|
|居左测试文本11|居中测试文本22|居右测试文本33|
|居左测试文本111|居中测试文本222|居右测试文本333|

# 代码
这是行内代码`onCreate(Bundle savedInstanceState)`的例子  
这是代码块和语法高亮：
``` java
// 注意java前面有空格
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
}
```
```
这里是代码1
```
    这里是代码2

# 强调
**加粗文本** 或者 __加粗文本__

*斜体文本*  或者_斜体文本_

~~删除文本~~

# 列表
- Red
- Green
- Blue

* Red
* Green
* Blue

+ Red
+ Green
+ Blue

1. Red
2. Green
3. Blue

# 标题
```sh
在 标题开头 加上1~6个#，依次代表一级标题、二级标题....六级标题
# 一级标题
## 二级标题
### 三级标题
##### 四级标题
###### 五级标题
###### 六级标题
```
```
在 标题底下 加上任意个=代表一级标题，-代表二级标题

一级标题
======

二级标题
----------
```
# 引用
> 这是一段引用    //在`>`后面有 1 个空格
> 
>     这是引用的代码块形式    //在`>`后面有 5 个空格
>     
> 代码例子：
>   
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

> 一级引用
> > 二级引用
> > > 三级引用

> #### 这是一个四级标题
> 
> 1. 这是第一行列表项
> 2. 这是第二行列表项

# 图片与链接
图片与链接的语法很像，区别在一个 ! 号。二者格式：
```
图片：![]()    ![图片文本(可忽略)](图片地址)

链接：[]()     [链接文本](链接地址)
```

链接又分为行内式、参考式和 自动链接：

这是行内式链接：[ConnorLin's Blog](http://connorlin.github.io)。

这是参考式链接：[ConnorLin's Blog][url]，其中url为链接标记，可置于文中任意位置。

[url]: http://connorlin.github.io/ "ConnorLin's Blog"

链接标记格式为：[链接标记文本]:  链接地址  链接title(可忽略)

这是自动链接：直接使用`<>`括起来<http://connorlin.github.io>

这是图片：![][avatar]

[avatar]: https://connorlin.github.io/images/avatar.jpg
