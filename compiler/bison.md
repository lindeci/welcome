- [官网](#官网)
- [bison 文件结构](#bison-文件结构)
- [终结符](#终结符)
- [Token](#token)
- [union 类型的 yylval](#union-类型的-yylval)
- [运算符的优先级和结合性](#运算符的优先级和结合性)
- [mysql 的 yy 文件局部分析](#mysql-的-yy-文件局部分析)
- [shift/reduce冲突](#shiftreduce冲突)
  - [例子](#例子)
- [规约](#规约)
  - [规约例子](#规约例子)
- [产生式](#产生式)
- [LR分析](#lr分析)
  - [LR分析例子](#lr分析例子)
- [文法](#文法)
  - [文法的例子](#文法的例子)
- [yyvsp](#yyvsp)
# 官网
https://www.gnu.org/software/bison/

官方文档： https://www.gnu.org/software/bison/manual/  
https://www.gnu.org/software/bison/manual/bison.pdf

# bison 文件结构

Bison 文件通常以 `.y` 结尾，它包含了用于生成语法分析器的上下文无关语法规范。Bison 文件主要由三个部分组成：

1. **控制信息部分**：这部分位于文件的开头，通常包含了一些 C 代码，这些代码会被原样复制到 Bison 生成的 C 文件（通常是 `y.tab.c`）的开头。你可以在这部分中包含一些必要的头文件，定义一些全局变量，或者声明一些函数。
2. **标记或语法定义部分**：这部分包含了你的语法规则。你可以在这部分中定义 token，设置 token 的优先级，以及指定属性的类型。
3. **C 代码部分**：这部分位于文件的末尾，包含了一些 C 代码，这些代码会被原样复制到 Bison 生成的 C 文件的末尾。你可以在这部分中定义一些函数，或者写一些其他的 C 代码。

这三个部分之间用 `%%` 分隔。希望这个答案对你有所帮助！如果你还有其他问题，欢迎随时向我提问。我会尽我所能提供帮助的！

# 终结符
在语法分析中，终结符是语法的基本构成单位，它们是语言的最小单元。终结符不能再被分解为更小的单位。例如，在 C 语言中，关键字（如 `int`、`if` 等）、标识符、常量、运算符（如 `+`、`-` 等）都是终结符。

# Token
在词法分析阶段，词法分析器将输入的字符序列分解为一系列的 token。每个 token 包含一个终结符和与之关联的属性值。例如，一个 token 可能是一个 `int` 关键字，或者一个具有特定值的整数常量。token 是语法分析器的输入单元，语法分析器根据 token 序列来判断输入是否符合语法规则。

# union 类型的 yylval
```c
%union {
    int num;
    Node* node;
}

%token <num> NUM
%type <node> expr term factor
```
- 在这个例子中，yylval 的类型是一个联合，它可以是 int 类型的 num，也可以是 Node* 类型的 node。
- %token <num> NUM：这行代码定义了一个名为 NUM 的 token。<num> 是这个 token 的类型，它必须是在 %union 中定义的一个字段。
- %type <node> expr term factor：这行代码定义了三个非终结符：expr、term 和 factor。<node> 是这些非终结符的类型，它必须是在 %union 中定义的一个字段。

# 运算符的优先级和结合性
```c
%left KEYWORD_USED_AS_IDENT
%nonassoc TEXT_STRING
%left KEYWORD_USED_AS_KEYWORD
```
- %left：声明运算符为左结合。也就是说，当同一个运算符连续出现时，先执行左边的运算。例如，在你的代码中，KEYWORD_USED_AS_IDENT和KEYWORD_USED_AS_KEYWORD被声明为左结合。
- %right：声明运算符为右结合。也就是说，当同一个运算符连续出现时，先执行右边的运算1。
- %nonassoc：声明运算符为非结合。也就是说，当同一个运算符连续出现时，会被视为语法错误。例如，在你的代码中，TEXT_STRING被声明为非结合。

# mysql 的 yy 文件局部分析
```c
// ODR violation here as well, so rename yysymbol_kind_t
#define yysymbol_kind_t my_sql_parser_symbol_kind_t

%}

%start start_entry

%parse-param { class THD *YYTHD }
%parse-param { class Parse_tree_root **parse_tree }

%lex-param { class THD *YYTHD }
%define api.pure                                    /* We have threads */
%define api.prefix {my_sql_parser_}

/*
  1. We do not accept any reduce/reduce conflicts
  2. We should not introduce new shift/reduce conflicts any more.
*/

%expect 63
```

这段Bison代码的含义如下：

- `#define yysymbol_kind_t my_sql_parser_symbol_kind_t`：这是一个预处理器指令，用于将`yysymbol_kind_t`替换为`my_sql_parser_symbol_kind_t`。这样，当预处理器在代码中看到`yysymbol_kind_t`时，就会用`my_sql_parser_symbol_kind_t`来替换它。

- `%start start_entry`：这个指令告诉Bison，语法分析应该从`start_entry`这个非终结符开始。

- `%parse-param { class THD *YYTHD } %parse-param { class Parse_tree_root **parse_tree }`：这些指令定义了传递给语法分析函数的参数。在这个例子中，参数是一个指向THD类的指针和一个指向Parse_tree_root类的双重指针。

- `%lex-param { class THD *YYTHD }`：这个指令定义了传递给词法分析函数的参数。在这个例子中，参数是一个指向THD类的指针。

- `%define api.pure`：这个指令告诉Bison生成一个纯（可重入）的语法分析器。

- `%define api.prefix {my_sql_parser_}`：这个指令定义了生成的函数和数据类型的名称前缀。在这个例子中，前缀是"my_sql_parser_"。

- `%expect 63`：这个指令告诉Bison，预计会有63个shift/reduce冲突。如果实际冲突数超过这个数值，Bison会报错。

# shift/reduce冲突
在编译器设计中，Shift/Reduce冲突是语法分析器（特别是LR分析器）在处理输入时可能遇到的一种问题。

- **Shift操作**：当分析器遇到一个新的符号，它可以选择将该符号"移入"（shift）到栈中，以便稍后处理。

- **Reduce操作**：分析器也可以选择使用某个产生式（规则）将栈顶的几个符号"规约"（reduce）为一个非终结符。

当分析器在同一点上既可以选择Shift操作也可以选择Reduce操作时，就会发生**Shift/Reduce冲突**。这通常是由于语法的二义性或者语法规则定义不清所导致的。

例如，考虑这样一个表达式`a+b*c`。如果我们先执行加法（即先规约`a+b`），然后再执行乘法，那么结果就会不正确。正确的做法应该是先执行乘法（即先规约`b*c`），然后再执行加法。这就需要我们定义运算符的优先级和结合性，以解决可能出现的Shift/Reduce冲突。
## 例子
在编译原理中，Shift/Reduce冲突是自底向上解析过程中常见的问题，它发生在解析器需要决定是将下一个输入符号推入堆栈（即执行Shift操作），还是应用产生式规约堆栈顶部的符号（即执行Reduce操作）。

以SQL查询为例，假设我们有以下文法：

```
<query> ::= SELECT <columns> FROM <table>
<columns> ::= <column> | <column>, <columns>
<column> ::= * | column_name
<table> ::= table_name
```

并且我们要解析以下查询：

```
SELECT column_name, * FROM table_name
```

在解析过程中，当我们遇到`,`时，我们可能会遇到Shift/Reduce冲突。因为我们可以选择将`column_name`规约为`<column>`（即执行Reduce操作），然后再将`,`和`*`推入堆栈。或者，我们也可以选择先将`,`推入堆栈（即执行Shift操作），然后再将`column_name, *`规约为`<columns>`。

这个冲突通常由语法的二义性或者文法定义的不精确导致。解决这个冲突的方法通常包括修改文法以消除二义性，或者使用某种策略（如优先选择Shift或Reduce）来解决冲突。

# 规约
在编译原理中，"规约"是指从一个句子反推回开始符号的过程。这个过程是句子的推导的逆过程。

例如，假设我们有一个文法`S→AB`，`A→a`，`B→b`，那么我们可以从开始符号`S`推导出句子`ab`（即`S→AB→ab`）。这就是一个句子的推导过程。

与之相反，如果我们拿到一个句子`ab`，我们可以通过规约操作将它规约回开始符号`S`（即`ab→AB→S`）。这就是一个句子的规约过程。
## 规约例子
在编译原理中，规约是自底向上解析过程的一个重要步骤，它涉及到将当前输入的一部分替换为由文法产生式定义的非终结符。

以SQL查询为例，假设我们有以下文法：

```
<query> ::= SELECT <columns> FROM <table>
<columns> ::= <column> | <column>, <columns>
<column> ::= *
<table> ::= table_name
```

并且我们要解析以下查询：

```
SELECT * FROM table_name
```

在解析过程中，当我们遇到`*`时，我们可以将其规约为`<column>`，因为我们有产生式`<column> ::= *`。然后，当我们遇到`FROM`时，我们可以将前面的`SELECT <column>`规约为`<query>`，因为我们有产生式`<query> ::= SELECT <columns> FROM <table>`。

这个过程就是规约。在自底向上的解析（如LR解析）中，规约是一个关键步骤，它帮助我们逐步构建出抽象语法树（AST），这是编译器用来表示源代码结构的数据结构。

# 产生式
在编译原理中，产生式（或规则）是用来描述语言的结构的。产生式由一个非终结符和一个由非终结符和终结符组成的序列构成，中间用`::=`分隔。非终结符是语法结构的名称（如`<query>`），终结符是语言的基本单位（如`SELECT`，`FROM`等）。

以SQL查询为例，我们可以定义以下产生式：

```
<query> ::= SELECT <columns> FROM <table>
<columns> ::= <column> | <column>, <columns>
<column> ::= *
<table> ::= table_name
```

在这个例子中，`<query>`、`<columns>`、`<column>`和`<table>`是非终结符，它们代表了SQL查询的不同部分。而`SELECT`、`FROM`、`,`和`*`是终结符，它们是语言的基本单位。

这些产生式可以生成如下的SQL查询：

```
SELECT * FROM table_name
```

这只是一个简单的例子，实际的SQL文法会更复杂，包括子查询、联接、条件等等。但是，基本的概念是相同的：通过定义一组产生式来描述语言的结构。这就是编译原理中产生式的基本思想。在编译器设计中，这些产生式被用来解析和理解源代码。每当编译器遇到一个符合某个产生式的句子时，它就会执行相应的操作（例如生成中间代码）。

# LR分析
LR分析是一种自底向上的语法分析方法，它使用一个栈来保存已经分析过的符号，并使用一个输入缓冲区来保存待分析的输入。LR分析的基本思想是尝试找到输入中的句柄（即可以被某个产生式规约的部分），然后用该产生式的左部替换它，直到整个输入被规约为开始符号。

下面是一个简单的LR分析过程的例子：

假设我们有以下文法G[S]：
```
(1) S → aAcBe
(2) A → b
(3) A → Ab
(4) B → d
```
我们要对输入串 `abbcde#` 进行LR分析。在分析的过程中，我们需要一个表来记录我们的步骤。该表共需7列，行数不定，做到哪是哪。列名如下：
- 步骤
- 符号栈
- 输入符号栈
- 动作
- 状态栈
- ACTION
- GOTO

其中，步骤就是从1向下递增。符号栈用来保存运算中的结果，初始为#，输入符号栈保存输入串，初始值为给定的。动作里面就是用来注释是进行移进，还是规约。状态栈就是保持LR分析表的那个状态了。Action 和Goto同理。

通过前两篇文章的步骤，此题可以构造出如下的一张LR分析表。

然后使用我们将要使用的辅助表来分析吧，为了简单。我还是直接给出答案。然后分析一下典型的情况。
## LR分析例子
LR分析是编译原理中的一种自底向上的语法分析方法，它使用一个堆栈来存储待处理的符号，并使用一个输入缓冲区来存储剩余的输入。LR分析器通过查看堆栈顶部的符号和输入缓冲区的下一个符号来决定下一步是"移位"（将下一个输入符号推入堆栈）还是"规约"（将堆栈中的一些符号替换为它们对应的非终结符）。

以SQL查询为例，假设我们有以下文法：

```
<query> ::= SELECT <columns> FROM <table>
<columns> ::= <column> | <column>, <columns>
<column> ::= *
<table> ::= table_name
```

并且我们要解析以下查询：

```
SELECT * FROM table_name
```

LR分析器的工作过程可能如下：

1. 初始状态：堆栈为空，输入缓冲区为`SELECT * FROM table_name`。因为`SELECT`是一个终结符，所以执行移位操作。

2. 堆栈为`SELECT`，输入缓冲区为`* FROM table_name`。因为`*`也是一个终结符，所以再次执行移位操作。

3. 堆栈为`SELECT *`，输入缓冲区为`FROM table_name`。此时，堆栈顶部的`*`可以被规约为`<column>`。

4. 堆栈为`SELECT <column>`，输入缓冲区仍然为`FROM table_name`。此时，堆栈顶部的`<column>`可以被规约为`<columns>`。

5. 堆栈为`SELECT <columns>`，输入缓冲区仍然为`FROM table_name`。因为`FROM`是一个终结符，所以执行移位操作。

6. 堆栈为`SELECT <columns> FROM`，输入缓冲区为`table_name`。因为`table_name`是一个终结符，所以执行移位操作。

7. 堆栈为`SELECT <columns> FROM table_name`，输入缓冲区为空。此时，堆栈顶部的`table_name`可以被规约为`<table>`。

8. 堆栈为 `SELECT <columns> FROM <table>`，输入缓冲区为空。此时，整个堆栈可以被规约为 `<query>`。

这个过程就是LR分析器如何解析SQL查询的示例。在实际应用中，LR分析器通常使用一个解析表来确定在给定状态下应该执行哪种操作（移位或规约）。这个解析表可以通过对文法进行一些预处理步骤（例如计算每个非终结符的FIRST集和FOLLOW集）来构建。

# 文法
在编译原理中，"文法"是用来描述一种语言语法结构的形式规则。一个文法通常由四个元素组成：
- **非终结符号集合**（也被称为“语法变量”）：每个非终结符号表示一个终结符号串的集合。
- **终结符号集合**（也被称为“词法单元集合”）：终结符号是该文法所定义的语言的基本符号的集合。
- **产生式集合**：每个产生式规定了一个非终结符号可以被替换为哪些符号串。
- **开始符号**：这是一个特殊的非终结符号，用来表示整个语言。

文法可以分为不同的类型，包括上下文无关文法、上下文有关文法、正规文法等。这些类型的文法在编译原理中有着不同的应用，例如上下文无关文法常用于描述程序设计语言的结构。

## 文法的例子
编译原理中的文法是一种形式化的语言描述方法，它用于描述一种语言（例如SQL）的所有可能的句子。这是通过定义一组产生式或规则来完成的，这些规则说明如何从一组终结符和非终结符生成句子。

以SQL查询为例，我们可以定义一个非常简单的文法：

```
<query> ::= SELECT <columns> FROM <table>
<columns> ::= <column> | <column>, <columns>
<column> ::= *
<table> ::= table_name
```

在这个文法中：
- `<query>`、`<columns>`、`<column>`和`<table>`是非终结符，它们代表了SQL查询的不同部分。
- `SELECT`、`FROM`、`,`和`*`是终结符，它们是语言的基本单位。
- `::=`表示定义，`|`表示选择。

这个文法可以生成如下的SQL查询：
```sql
SELECT * FROM table_name
```

这只是一个非常简化的例子，实际的SQL文法会更复杂，包括子查询、联接、条件等等。但是，基本的概念是相同的：通过定义一组规则来描述语言的结构。这就是编译原理中文法的基本思想。在编译器设计中，这些规则被用来解析和理解源代码。每当编译器遇到一个符合某个规则的句子时，它就会执行相应的操作（例如生成中间代码）。 

# yyvsp
在Bison中，`yyvsp`是一个指针，用于访问语法分析堆栈。这个堆栈包含了你正在处理的语法规则的右侧部分的元素。每当Bison完成一个规则的归约，它就会从堆栈中弹出与该规则右侧元素数量相同的项，并将规则的结果（即归约动作的结果）压入堆栈。

在你的代码`*parse_tree= (yyvsp[0].top_level_node);`中，`yyvsp[0]`表示当前正在归约的规则右侧的第一个元素。这里，`top_level_node`可能是你在词法分析阶段赋予该元素的某种属性或值。

总的来说，`yyvsp`数组是Bison用来处理和追踪语法分析过程中符号和它们的值的工具。