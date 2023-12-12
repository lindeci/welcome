- [基本语法规则](#基本语法规则)
- [数据类型](#数据类型)
- [YAML 对象](#yaml-对象)
- [YAML 数组](#yaml-数组)
- [复合结构](#复合结构)
- [纯量](#纯量)
  - [对于多行的文字，YAML 提供了两种特殊的语法支持](#对于多行的文字yaml-提供了两种特殊的语法支持)
  - [空（Null）](#空null)
- [引用](#引用)
- [类型转换](#类型转换)
- [特殊符号](#特殊符号)

YAML 是 “YAML Ain’t a Markup Language”（YAML 不是一种标记语言）的递归缩写。在开发的这种语言时，YAML 的意思其实是：“Yet Another Markup Language”（仍是一种标记语言）。YAML 的语法和其他高级语言类似，并且可以简单表达清单、散列表，标量等数据形态。它使用空白符号缩进和大量依赖外观的特色，特别适合用来表达或编辑数据结构、各种配置文件、倾印调试内容、文件大纲1。

# 基本语法规则
- 大小写敏感
- 使用缩进表示层级关系
- 缩进时不允许使用Tab键，只允许使用空格
- 缩进的空格数目不重要，只要相同层级的元素左侧对齐即可
- '#'表示注释，从这个字符一直到行尾，都会被解析器忽略
- 
# 数据类型
- 对象：键值对的集合，又称为映射（mapping）/ 哈希（hashes） / 字典（dictionary）
- 数组：一组按次序排列的值，又称为序列（sequence） / 列表（list）
- 纯量（scalars）：单个的、不可再分的值

# YAML 对象
对象键值对使用冒号结构表示 key: value，冒号后面要加一个空格。  
也可以使用 `key:{key1: value1, key2: value2, ...}`。  
还可以使用缩进表示层级关系；
```yaml
key: 
    child-key: value
    child-key2: value2
```
较为复杂的对象格式，可以使用问号加一个空格代表一个复杂的 key，配合一个冒号加一个空格代表一个 value：
```yaml
?  
    - complexkey1
    - complexkey2
:
    - complexvalue1
    - complexvalue2
```
意思即对象的属性是一个数组 `[complexkey1,complexkey2]`，对应的值也是一个数组 `[complexvalue1,complexvalue2]`

# YAML 数组
以 - 开头的行表示构成一个数组：
```yaml
- A
- B
- C
```
YAML 支持多维数组，可以使用行内表示：
```yaml
key: [value1, value2, ...]
```
数据结构的子成员是一个数组，则可以在该项下面缩进一个空格。
```yaml
-
 - A
 - B
 - C
```
一个相对复杂的例子：
```yaml
companies:
    -
        id: 1
        name: company1
        price: 200W
    -
        id: 2
        name: company2
        price: 500W
```
意思是 companies 属性是一个数组，每一个数组元素又是由 id、name、price 三个属性构成。

数组也可以使用流式(flow)的方式表示：
```yaml
companies: [{id: 1,name: company1,price: 200W},{id: 2,name: company2,price: 500W}]
```

# 复合结构
数组和对象可以构成复合结构，例：
```yaml
languages:
  - Ruby
  - Perl
  - Python 
websites:
  YAML: yaml.org 
  Ruby: ruby-lang.org 
  Python: python.org 
  Perl: use.perl.org
```
转换为 json 为：
```yaml
{ 
  languages: [ 'Ruby', 'Perl', 'Python'],
  websites: {
    YAML: 'yaml.org',
    Ruby: 'ruby-lang.org',
    Python: 'python.org',
    Perl: 'use.perl.org' 
  } 
}
```

# 纯量
纯量是最基本的，不可再分的值，包括：
- 字符串
- 布尔值
- 整数
- 浮点数
- Null
- 时间
- 日期
使用一个例子来快速了解纯量的基本使用：
```yaml
boolean: 
    - TRUE  #true,True都可以
    - FALSE  #false，False都可以
float:
    - 3.14
    - 6.8523015e+5  #可以使用科学计数法
int:
    - 123
    - 0b1010_0111_0100_1010_1110    #二进制表示
null:
    nodeName: 'node'
    parent: ~  #使用~表示null
string:
    - 哈哈
    - 'Hello world'  #可以使用双引号或者单引号包裹特殊字符
    - newline
      newline2    #字符串可以拆成多行，每一行会被转化成一个空格
date:
    - 2018-02-17    #日期必须使用ISO 8601格式，即yyyy-MM-dd
datetime: 
    -  2018-02-17T15:02:31+08:00    #时间使用ISO 8601格式，时间和日期之间使用T连接，最后使用+代表时区
```
## 对于多行的文字，YAML 提供了两种特殊的语法支持
- 保留换行(Newlines preserved)

使用竖线符“ | ”来表示该语法，每行的缩进和行尾空白都会被去掉，而额外的缩进会被保留
```yaml
lines: |
  我是第一行
  我是第二行
    我是吴彦祖
      我是第四行
  我是第五行
```
对应的 json
```JSON
"lines": "我是第一行\n我是第二行\n  我是吴彦祖\n     我是第四行\n我是第五行"
```
- 折叠换行(Newlines folded)

使用右尖括号“ > ”来表示该语法，只有空白行才会被识别为换行，原来的换行符都会被转换成空格
```YAML
lines: >
  我是第一行
  我也是第一行
  我仍是第一行
  我依旧是第一行

  我是第二行
  这么巧我也是第二行
```
对应的 json
```JSON
"lines": "我是第一行 我也是第一行 我仍是第一行 我依旧是第一行\n我是第二行 这么巧我也是第二行"
```
## 空（Null）
“null”、“Null”和“~”都是空，不指定值默认也是空
```YAML
nulls:
  - null
  - Null
  - ~
  -
```
对应的 json
```JSON
"nulls": [ null, null, null, null ]
```

# 引用
`&` 锚点和 `*` 别名，可以用来引用:
```yaml
defaults: &defaults
  adapter:  postgres
  host:     localhost

development:
  database: myapp_development
  <<: *defaults

test:
  database: myapp_test
  <<: *defaults
```
相当于:
```yaml
defaults:
  adapter:  postgres
  host:     localhost

development:
  database: myapp_development
  adapter:  postgres
  host:     localhost

test:
  database: myapp_test
  adapter:  postgres
  host:     localhost
```
`&` 用来建立锚点（defaults），`<<` 表示合并到当前数据，`*` 用来引用锚点。

下面是另一个例子:
```yaml
- &showell Steve 
- Clark 
- Brian 
- Oren 
- *showell 
```
转为 JavaScript 代码如下:
```js
[ 'Steve', 'Clark', 'Brian', 'Oren', 'Steve' ]
```

# 类型转换
YAML 支持使用严格类型标签 `!!` （双感叹号+目标类型）来强制转换类型
```yaml
a: !!float '666' # !! 为严格类型标签
b: '666' # 其实双引号也算是类型转换符
c: !!str 666 # 整数转为字符串
d: !!str 666.66 # 浮点数转为字符串
e: !!str true # 布尔值转为字符串
f: !!str yes # 布尔值转为字符串
```
对应的 json
```json
"a": 666,
"b": "666",
"c": "666",
"d": "666.66",
"e": "true"
"f": "yes"
```

# 特殊符号
- `…` 和`---`配合使用，在一个配置文件中代表一个文件的结束：
```yaml
---
time: 20:03:20
player: Sammy Sosa
action: strike (miss)
...
---
time: 20:03:47
player: Sammy Sosa
action: grand slam
...
```
- {} 流式风格
```yaml
key: { child-key1: value1, child-key2: value2 }
```
- |- 和 |+  
|-：这个符号表示保留每行尾部的换行符 \n，但删除内容结尾处的换行符。例如：
```yaml
s3: |-
  Foo 
```
这里，字符串 “Foo” 后面的换行符将会被删除。

|+：这个符号表示保留每行尾部的换行符 \n，同时也保留内容结尾处的换行符。例如：
```yaml
s2: |+
  Foo 
```
这里，字符串 “Foo” 后面的换行符将会被保留。