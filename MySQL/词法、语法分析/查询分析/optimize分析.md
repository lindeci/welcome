
```md
    -# Logical transformations:
      - Outer to inner joins transformation.
      - Equality/constant propagation.
      - Partition pruning.
      - COUNT(*), MIN(), MAX() constant substitution in case of
        implicit grouping.
      - ORDER BY optimization.
    -# Perform cost-based optimization of table order and access path
       selection. See JOIN::make_join_plan()
    -# Post-join order optimization:
       - Create optimal table conditions from the where clause and the
         join conditions.
       - Inject outer-join guarding conditions.
       - Adjust data access methods after determining table condition
         (several times.)
       - Optimize ORDER BY/DISTINCT.
    -# Code generation
       - Set data access functions.
       - Try to optimize away sorting/distinct.
       - Setup temporary table usage for grouping and/or sorting. 
```
举例介绍
## Outer to inner joins transformation
内连接通常比外连接更高效
```sql
SELECT orders.order_id, customers.customer_name
FROM orders
LEFT OUTER JOIN customers ON orders.customer_id = customers.customer_id;
```

如果查询优化器确定orders.customer_id始终在customers表中有匹配的行，那么它可以将这个左外连接转换为更高效的内连接，如下所示：
```sql
SELECT orders.order_id, customers.customer_name
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;
```
##  **Equality/constant propagation**
等式/常量传播是一种优化技术，它通过在查询中传播等式和常量来简化表达式和条件。例如，考虑以下查询：

```sql
SELECT * FROM employees WHERE department_id = 10 AND salary = department_id;
```

在这个查询中，`department_id`和`10`是等式，因此，查询优化器可以将`salary = department_id`替换为`salary = 10`，从而简化查询。

##   **Partition pruning**
分区修剪是一种优化技术，它通过只查询与查询条件匹配的分区来减少查询的数据量。例如，如果我们有一个按年份分区的`sales`表，并且我们正在查询2019年的销售数据，那么查询优化器只会查询2019年的分区，而不是整个`sales`表。

```sql
SELECT * FROM sales WHERE year = 2019;
```

## **COUNT(*), MIN(), MAX() constant substitution in case of implicit grouping**
在隐式分组的情况下，如果查询优化器可以确定某些聚合函数的结果是常量，那么它可以将这些函数替换为对应的常量。例如，如果我们有一个只包含2019年数据的`sales`表，并且我们正在查询最小和最大的年份，那么查询优化器可以将`MIN(year)`和`MAX(year)`替换为常量`2019`。

```sql
SELECT MIN(year), MAX(year) FROM sales;
```

## **ORDER BY optimization**
`ORDER BY`优化是一种优化技术，它通过各种方法（如索引扫描、临时表、文件排序等）来提高排序操作的效率。例如，如果我们正在根据索引列进行排序，那么查询优化器可以使用索引扫描来避免昂贵的排序操作。

```sql
SELECT * FROM employees ORDER BY employee_id;
```

在这个查询中，如果`employee_id`是一个索引，那么查询优化器可以直接使用索引扫描来获取排序的结果，而不需要进行额外的排序操作。
