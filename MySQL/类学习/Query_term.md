- [类成员注释](#类成员注释)
- [类介绍](#类介绍)
  - [对应SQL例子](#对应sql例子)
- [enum Query\_term\_type 介绍](#enum-query_term_type-介绍)
  - [枚举值](#枚举值)
  - [说明](#说明)
  - [例子说明](#例子说明)

# 类成员注释
```cpp
class Query_term { // 查询项类
 protected:
   Query_term_set_op *m_parent; // 父查询项集操作符
   Query_result *m_setop_query_result; // 连接查询结果
   bool m_owning_operand; // 是否拥有操作数
   Table_ref *m_result_table; // 结果表
   mem_root_deque<Item*> *m_fields; // 字段列表
 private:
   uint m_curr_id; // 当前ID

 public:
   Query_term * pushdown_limit_order_by(Query_term_set_op *); // 下推限制排序
   bool validate_structure(const Query_term *, int) const; // 验证结构
   std::pair<bool, bool> redundant_order_by(Query_block *, int); // 冗余排序
   virtual Query_term_type term_type(void) const; // 查询项类型
   virtual const char * operator_string(void) const; // 操作符字符串
   ~Query_term(); // 析构函数
   virtual size_t child_count(void) const; // 子查询项数量
   Query_term_set_op * parent(void) const; // 父查询项集操作符
   virtual void cleanup(bool); // 清理
   virtual void destroy_tree(void); // 销毁树
   virtual bool open_result_tables(THD *, int); // 打开结果表
   virtual void debugPrint(int, std::ostringstream &) const; // 调试打印
   static void indent(int, std::ostringstream &); // 缩进
   void printPointers(std::ostringstream &) const; // 打印指针
   static void print_order(const THD *, String *, ORDER *, enum_query_type); // 打印排序
   virtual Query_block * query_block(void) const; // 查询块
   void set_setop_query_result(Query_result *); // 设置连接查询结果
   Query_result * setop_query_result(void); // 连接查询结果
   Query_result_union * setop_query_result_union(void); // 连接查询结果联合
   void cleanup_query_result(bool); // 清理查询结果
   void set_owning_operand(void); // 设置拥有操作数
   bool owning_operand(void); // 是否拥有操作数
   void set_result_table(Table_ref *); // 设置结果表
   Table_ref & result_table(void); // 结果表
   void set_fields(mem_root_deque<Item*> *); // 设置字段列表
   mem_root_deque<Item*> * fields(void); // 字段列表
}
```

# 类介绍
```sql
Example: ((SELECT * FROM t1 UNION SELECT * FROM t2 UNION ALL SELECT * FROM t3
           ORDER BY a LIMIT 5) INTERSECT
          (((SELECT * FROM t3 ORDER BY a LIMIT 4) ) EXCEPT SELECT * FROM t4)
          ORDER BY a LIMIT 4) ORDER BY -a LIMIT 3;

->
            m_query_term   +------------------+     slave(s)
            +--------------|-Query_expression |------------------+
            |              +------------------+                  |
            V        post_                                       |
+-------------------+processing_ +----------------------+        |
| Query_term_unary  |block()     |Query_block           |        |
|                   |----------->|order by -(`a) limit 3|        |
+-------------------+            +----------------------+        |
 |m_children                                                     |
 | +-----------------------+   +----------------------+          |
 | |Query_term_intersect   |   |Query_block           |          |
 +>|last distinct index: 1 |-->|order by `a` limit 4  |          |
   +-----------------------+   +----------------------+          |
    |m_children                                                  |
    |  +-----------------------+   +----------------------+      |
    |  |Query_term_union       |   |Query_block           |      |
    +->|last distinct index: 1 |-->|order by `a`  limit 5 |      |
    |  +-----------------------+   +----------------------+      |
    |    |m_children                                             |
    |    |   +------------+        SELECT * FROM t1             /
    |    +-->|Query_block |  <---------------------------------+
    |    |   +------------+  ----------------------------------+ next
    |    |                                                      \
    |    |   +------------+        SELECT * FROM t2             /
    |    +-->|Query_block |  <---------------------------------+
    |    |   +------------+  ----------------------------------+ next
    |    |                                                      \
    |    |   +------------+        SELECT * FROM t3             /
    |    +-->|Query_block |  <---------------------------------+
    |        +------------+  ----------------------------------+ next
    |                                                           \
    |  +-----------------------+  +------------+                 |
    |  |Query_term_except      |->|Query_block |                 |
    +->|last distinct index: 1 |  +------------+                 |
       +-----------------------+                                 |
         |m_children                                             |
         |   +----------------------+                            |
         |   |Query_block           |      SELECT * FROM t3      /
         +-->|order by `a`  limit 4 |  <------------------------+
         |   +----------------------+  -------------------------+ next
         |                                                       \
         |   +------------+                SELECT * FROM t4      |
         +-->|Query_block | <------------------------------------+
             +------------+
```
</details>

## 对应SQL例子
```sql
(
	(
		(
			(
				SELECT * FROM t1
				UNION
				SELECT * FROM t2
				UNION ALL
				SELECT * FROM t3
			)
			ORDER BY a LIMIT 5
		)
		INTERSECT
		(
			(
				SELECT * FROM t3
				ORDER BY a LIMIT 4
			)
			EXCEPT
			SELECT * FROM t4
		)
	)
    ORDER BY a LIMIT 4
)
ORDER BY -a LIMIT 3;
```


# enum Query_term_type 介绍
## 枚举值
|枚举值|描述|
|:---|:---:|
|QT_QUERY_BLOCK 	|Represents Query specification, table value constructor and explicit table.|
|QT_UNARY 	|Represents a query primary with parentesized query expression body with order by clause and/or limit/offset clause.If none of order by or limit is present, we collapse this level of parentheses.|
|QT_INTERSECT 	|Represents the three set operations. Nodes are N-ary, i.e. a node can hold two or more operands.|
|QT_EXCEPT 	| |
|QT_UNION 	| |

## 说明
```sql
<query expression> ::=
    [ <with clause> ] <query expression body>
    [ <order by clause> ] [ <limit/offset> ]

<query expression body> ::=
   <query term>
 | <query expression body> UNION [ ALL | DISTINCT ]
   [ <corresponding spec> ] <query term>
 | <query expression body> EXCEPT [ ALL | DISTINCT ]
   [ <corresponding spec> ] <query term>

<query term> ::=
   <query primary>
 | <query expression body> INTERSECT [ ALL | DISTINCT ]
   [ <corresponding spec> ] <query primary>

<query primary> ::=
   <simple table>
 | <left paren> <query expression body>
   [ <order by clause> ] [ <limit/offset (*)> ]
   <right paren>

<simple table> ::=
   <query specification>
 | <table value constructor>
 | <explicit table>

(*) MySQL syntax and semantics. The standard uses /<result offset clause/> and
    \<fetch first clause\>.
```
## 例子说明
```sql
<table value constructor>
SELECT olympiad ,host_city 
FROM 
( 
VALUES 
(2012, 'London') ,
(2016, 'Rio de Janeiro') ,
(2020, 'Tokyo') ,
(2024, 'Paris') ,
(2028, 'Los Angeles') 
) as olympics(olympiad, host_city)

<query specification>
SELECT column1, column2
FROM table1
WHERE condition order by column1 limit 5;

上面 table1 为 <explicit table>


<left paren> 为左括号
<right paren> 为右括号
SELECT column1, column2
FROM 
(
    SELECT column1, column2
    FROM table1
    WHERE condition1
) AS subquery
WHERE condition2


<corresponding spec>
SELECT column1, column2
FROM table1
UNION CORRESPONDING BY (column1, column2)
SELECT column1, column2
FROM table2
```
## 
```sql

```