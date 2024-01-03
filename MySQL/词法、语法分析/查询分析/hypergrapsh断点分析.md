
```sql
set optimizer_switch="hypergraph_optimizer=on";
```

SET optimizer_trace='enabled=on';

select
	l_orderkey,
	sum(l_extendedprice * (1 - l_discount)) as revenue,
	o_orderdate,
	o_shippriority
from
	customer,
	orders,
	lineitem
where
	c_mktsegment = 'HOUSEHOLD'
	and c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and o_orderdate < '1995-03-23'
	and l_shipdate > '1995-03-23'
group by
	l_orderkey,
	o_orderdate,
	o_shippriority
order by
	revenue desc,
	o_orderdate
LIMIT 10;



ysql> SELECT * FROM `information_schema`.`OPTIMIZER_TRACE`\G
*************************** 1. row ***************************
                            QUERY: select
l_orderkey,
sum(l_extendedprice * (1 - l_discount)) as revenue,
o_orderdate,
o_shippriority
from
customer,
orders,
lineitem
where
c_mktsegment = 'HOUSEHOLD'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < '1995-03-23'
and l_shipdate > '1995-03-23'
group by
l_orderkey,
o_orderdate,
o_shippriority
order by
revenue desc,
o_orderdate
LIMIT 10
                            TRACE: {
  "steps": [
    {
      "join_preparation": {
        "select#": 1,
        "steps": [
          {
            "expanded_query": "/* select#1 */ select `lineitem`.`L_ORDERKEY` AS `l_orderkey`,sum((`lineitem`.`L_EXTENDEDPRICE` * (1 - `lineitem`.`L_DISCOUNT`))) AS `revenue`,`orders`.`O_ORDERDATE` AS `o_orderdate`,`orders`.`O_SHIPPRIORITY` AS `o_shippriority` from `customer` join `orders` join `lineitem` where ((`customer`.`C_MKTSEGMENT` = 'HOUSEHOLD') and (`customer`.`C_CUSTKEY` = `orders`.`O_CUSTKEY`) and (`lineitem`.`L_ORDERKEY` = `orders`.`O_ORDERKEY`) and (`orders`.`O_ORDERDATE` < '1995-03-23') and (`lineitem`.`L_SHIPDATE` > '1995-03-23')) group by `lineitem`.`L_ORDERKEY`,`orders`.`O_ORDERDATE`,`orders`.`O_SHIPPRIORITY` order by `revenue` desc,`orders`.`O_ORDERDATE` limit 10"
          }
        ]
      }
    },
    {
      "join_optimization": {
        "select#": 1,
        "steps": [
          {
            "condition_processing": {
              "condition": "WHERE",
              "original_condition": "((`customer`.`C_MKTSEGMENT` = 'HOUSEHOLD') and (`customer`.`C_CUSTKEY` = `orders`.`O_CUSTKEY`) and (`lineitem`.`L_ORDERKEY` = `orders`.`O_ORDERKEY`) and (`orders`.`O_ORDERDATE` < '1995-03-23') and (`lineitem`.`L_SHIPDATE` > '1995-03-23'))",
              "steps": [
                {
                  "transformation": "equality_propagation",
                  "resulting_condition": "((`orders`.`O_ORDERDATE` < '1995-03-23') and (`lineitem`.`L_SHIPDATE` > '1995-03-23') and multiple equal('HOUSEHOLD', `customer`.`C_MKTSEGMENT`) and multiple equal(`customer`.`C_CUSTKEY`, `orders`.`O_CUSTKEY`) and multiple equal(`lineitem`.`L_ORDERKEY`, `orders`.`O_ORDERKEY`))"
                },
                {
                  "transformation": "constant_propagation",
                  "resulting_condition": "((`orders`.`O_ORDERDATE` < '1995-03-23') and (`lineitem`.`L_SHIPDATE` > '1995-03-23') and multiple equal('HOUSEHOLD', `customer`.`C_MKTSEGMENT`) and multiple equal(`customer`.`C_CUSTKEY`, `orders`.`O_CUSTKEY`) and multiple equal(`lineitem`.`L_ORDERKEY`, `orders`.`O_ORDERKEY`))"
                },
                {
                  "transformation": "trivial_condition_removal",
                  "resulting_condition": "((`orders`.`O_ORDERDATE` < DATE'1995-03-23') and (`lineitem`.`L_SHIPDATE` > DATE'1995-03-23') and multiple equal('HOUSEHOLD', `customer`.`C_MKTSEGMENT`) and multiple equal(`customer`.`C_CUSTKEY`, `orders`.`O_CUSTKEY`) and multiple equal(`lineitem`.`L_ORDERKEY`, `orders`.`O_ORDERKEY`))"
                }
              ]
            }
          },
          {
            "substitute_generated_columns": {
            }
          },
          [
            {
              "index": "PRIMARY",
              "usable": true,
              "key_parts": [
                "O_ORDERKEY"
              ]
            },
            {
              "index": "I_O_CUSTKEY",
              "usable": true,
              "key_parts": [
                "O_CUSTKEY",
                "O_ORDERKEY"
              ]
            },
            {
              "index": "I_O_ORDERDATE",
              "usable": true,
              "key_parts": [
                "O_ORDERDATE",
                "O_ORDERKEY"
              ]
            }
          ],
          {
            "chosen": false,
            "cause": "not_single_table"
          },
          {
            "chosen": false,
            "cause": "not_single_table"
          },
          [
            {
              "index": "PRIMARY",
              "usable": true,
              "key_parts": [
                "C_CUSTKEY"
              ]
            },
            {
              "index": "I_C_NATIONKEY",
              "usable": true,
              "key_parts": [
                "C_NATIONKEY",
                "C_CUSTKEY"
              ]
            }
          ],
          [
            {
              "index": "PRIMARY",
              "usable": true,
              "key_parts": [
                "L_ORDERKEY",
                "L_LINENUMBER"
              ]
            },
            {
              "index": "I_L_ORDERKEY",
              "usable": true,
              "key_parts": [
                "L_ORDERKEY",
                "L_LINENUMBER"
              ]
            },
            {
              "index": "I_L_PARTKEY",
              "usable": true,
              "key_parts": [
                "L_PARTKEY",
                "L_ORDERKEY",
                "L_LINENUMBER"
              ]
            },
            {
              "index": "I_L_SUPPKEY",
              "usable": true,
              "key_parts": [
                "L_SUPPKEY",
                "L_ORDERKEY",
                "L_LINENUMBER"
              ]
            },
            {
              "index": "I_L_PARTKEY_SUPPKEY",
              "usable": true,
              "key_parts": [
                "L_PARTKEY",
                "L_SUPPKEY",
                "L_ORDERKEY",
                "L_LINENUMBER"
              ]
            },
            {
              "index": "I_L_SHIPDATE",
              "usable": true,
              "key_parts": [
                "L_SHIPDATE",
                "L_ORDERKEY",
                "L_LINENUMBER"
              ]
            },
            {
              "index": "I_L_COMMITDATE",
              "usable": true,
              "key_parts": [
                "L_COMMITDATE",
                "L_ORDERKEY",
                "L_LINENUMBER"
              ]
            },
            {
              "index": "I_L_RECEIPTDATE",
              "usable": true,
              "key_parts": [
                "L_RECEIPTDATE",
                "L_ORDERKEY",
                "L_LINENUMBER"
              ]
            }
          ],
          {
            "chosen": false,
            "cause": "not_single_table"
          },
          {
            "chosen": false,
            "cause": "not_single_table"
          },
          {
            "creating_tmp_table": {
              "tmp_table_info": {
                "table": "<temporary>",
                "columns": 4,
                "row_length": 36,
                "key_length": 0,
                "unique_constraint": false,
                "makes_grouped_rows": false,
                "cannot_insert_duplicates": false,
                "location": "TempTable"
              }
            }
          },
          {
            "join_optimizer": [
              "Join list after simplification:",
              "* lineitem  join_type=inner",
              "* orders  join_type=inner",
              "* customer  join_type=inner",
              "",
              "Made this relational tree; WHERE condition is ((orders.O_ORDERDATE < DATE'1995-03-23') and (lineitem.L_SHIPDATE > DATE'1995-03-23') and multiple equal('HOUSEHOLD', customer.C_MKTSEGMENT) and multiple equal(customer.C_CUSTKEY, orders.O_CUSTKEY) and multiple equal(lineitem.L_ORDERKEY, orders.O_ORDERKEY)):",
              "* Inner join [companion set 0xffff30d014f8] (flattened)",
              "  * customer [companion set 0xffff30d014f8]",
              "  * orders [companion set 0xffff30d014f8]",
              "  * lineitem [companion set 0xffff30d014f8]",
              "",
              "Pushing conditions down.",
              "",
              "After pushdown; remaining WHERE conditions are (orders.O_ORDERDATE < DATE'1995-03-23') AND (lineitem.L_SHIPDATE > DATE'1995-03-23') AND (customer.C_MKTSEGMENT = 'HOUSEHOLD'), table filters are (none):",
              "* Inner join [companion set 0xffff30d014f8] (equijoin condition = (lineitem.L_ORDERKEY = orders.O_ORDERKEY))",
              "  * lineitem [companion set 0xffff30d014f8]",
              "  * Inner join [companion set 0xffff30d014f8] (equijoin condition = (customer.C_CUSTKEY = orders.O_CUSTKEY))",
              "    * customer [companion set 0xffff30d014f8]",
              "    * orders [companion set 0xffff30d014f8]",
              "",
              "Companion set: 0xffff30d014f8:{{lineitem.L_ORDERKEY, orders.O_ORDERKEY}, {customer.C_CUSTKEY, orders.O_CUSTKEY}}",
              "Selectivity of join (customer.C_CUSTKEY = orders.O_CUSTKEY):",
              " - capping selectivity to 6.73927e-06 since index is unique",
              " - found 1-field prefix of candidate index I_O_CUSTKEY with selectivity 9.93098e-06 for last field orders.O_CUSTKEY",
              " - used an index or a histogram for multiple equal(customer.C_CUSTKEY, orders.O_CUSTKEY), selectivity = 6.73927e-06",
              "Selectivity of join (lineitem.L_ORDERKEY = orders.O_ORDERKEY):",
              " - found 1-field prefix of candidate index PRIMARY with selectivity 6.75672e-07 for last field lineitem.L_ORDERKEY",
              " - capping selectivity to 6.7567e-07 since index is unique",
              " - used an index or a histogram for multiple equal(lineitem.L_ORDERKEY, orders.O_ORDERKEY), selectivity = 6.7567e-07",
              " - capping selectivity to 6.73927e-06 since index is unique",
              " - found 1-field prefix of candidate index I_O_CUSTKEY with selectivity 9.93098e-06 for last field orders.O_CUSTKEY",
              " - used an index or a histogram for multiple equal(customer.C_CUSTKEY, orders.O_CUSTKEY), selectivity = 6.73927e-06",
              " - found 1-field prefix of candidate index PRIMARY with selectivity 6.75672e-07 for last field lineitem.L_ORDERKEY",
              " - capping selectivity to 6.7567e-07 since index is unique",
              " - used an index or a histogram for multiple equal(lineitem.L_ORDERKEY, orders.O_ORDERKEY), selectivity = 6.7567e-07",
              "",
              "Constructed hypergraph:",
              "digraph G {  # 2 edges",
              "  customer -> orders [label=\"(customer.C_CUSTKEY = orders.O_CUSTKEY) (6.74e-06)\",arrowhead=none]",
              "  lineitem -> orders [label=\"(lineitem.L_ORDERKEY = orders.O_ORDERKEY) (6.76e-07)\",arrowhead=none]",
              "}",
              "",
              " - fallback selectivity for (orders.O_ORDERDATE < DATE'1995-03-23') = 0.3333",
              "Total eligibility set for (orders.O_ORDERDATE < DATE'1995-03-23'): {orders}",
              " - fallback selectivity for (lineitem.L_SHIPDATE > DATE'1995-03-23') = 0.3333",
              "Total eligibility set for (lineitem.L_SHIPDATE > DATE'1995-03-23'): {lineitem}",
              " - fallback selectivity for (customer.C_MKTSEGMENT = 'HOUSEHOLD') = 0.1",
              "Total eligibility set for (customer.C_MKTSEGMENT = 'HOUSEHOLD'): {customer}",
              "",
              "Found sargable join condition (lineitem.L_ORDERKEY = orders.O_ORDERKEY) on lineitem",
              " - found 1-field prefix of candidate index PRIMARY with selectivity 6.75672e-07 for last field lineitem.L_ORDERKEY",
              " - capping selectivity to 6.7567e-07 since index is unique",
              " - used an index or a histogram for multiple equal(lineitem.L_ORDERKEY, orders.O_ORDERKEY), selectivity = 6.7567e-07",
              "Found sargable join condition (customer.C_CUSTKEY = orders.O_CUSTKEY) on customer",
              " - capping selectivity to 6.73927e-06 since index is unique",
              " - found 1-field prefix of candidate index I_O_CUSTKEY with selectivity 9.93098e-06 for last field orders.O_CUSTKEY",
              " - used an index or a histogram for multiple equal(customer.C_CUSTKEY, orders.O_CUSTKEY), selectivity = 6.73927e-06",
              "Found sargable join condition (lineitem.L_ORDERKEY = orders.O_ORDERKEY) on orders",
              "Found sargable join condition (customer.C_CUSTKEY = orders.O_CUSTKEY) on orders",
              " - capping selectivity to 6.73927e-06 since index is unique",
              " - found 1-field prefix of candidate index I_O_CUSTKEY with selectivity 9.93098e-06 for last field orders.O_CUSTKEY",
              " - used an index or a histogram for multiple equal(customer.C_CUSTKEY, orders.O_CUSTKEY), selectivity = 6.73927e-06",
              " - found 1-field prefix of candidate index PRIMARY with selectivity 6.75672e-07 for last field lineitem.L_ORDERKEY",
              " - capping selectivity to 6.7567e-07 since index is unique",
              " - used an index or a histogram for multiple equal(lineitem.L_ORDERKEY, orders.O_ORDERKEY), selectivity = 6.7567e-07",
              "",
              "Functional dependencies (after pruning):",
              " - lineitem.L_ORDERKEY=orders.O_ORDERKEY",
              " - {orders.O_ORDERKEY} -> orders.O_ORDERDATE [always active]",
              " - {orders.O_ORDERKEY} -> orders.O_SHIPPRIORITY [always active]",
              " - {orders.O_CUSTKEY, orders.O_ORDERKEY} -> orders.O_ORDERDATE [always active]",
              " - {orders.O_CUSTKEY, orders.O_ORDERKEY} -> orders.O_SHIPPRIORITY [always active]",
              " - {orders.O_ORDERDATE, orders.O_ORDERKEY} -> orders.O_SHIPPRIORITY [always active]",
              " - {lineitem.L_ORDERKEY, orders.O_ORDERDATE, orders.O_SHIPPRIORITY} -> sum((lineitem.L_EXTENDEDPRICE * (1 - lineitem.L_DISCOUNT))) [always active]",
              "",
              "Interesting orders:",
              " - 1: sum((lineitem.L_EXTENDEDPRICE * (1 - lineitem.L_DISCOUNT))) DESC, orders.O_ORDERDATE ASC",
              " - 2: group orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY",
              " - 3: lineitem.L_ORDERKEY ASC [support order]",
              " - 4: lineitem.L_ORDERKEY DESC [support order]",
              " - 5: orders.O_ORDERKEY ASC [support order]",
              " - 6: orders.O_ORDERKEY DESC [support order]",
              " - 7: orders.O_ORDERDATE ASC, orders.O_ORDERKEY ASC [homogenized from other ordering]",
              " - 8: orders.O_ORDERDATE DESC, orders.O_ORDERKEY DESC [support order]",
              " - 9: orders.O_ORDERDATE DESC [support order]",
              " - 10: orders.O_ORDERDATE ASC, lineitem.L_ORDERKEY ASC, orders.O_SHIPPRIORITY ASC [homogenized from other ordering]",
              "",
              "NFSM for interesting orders, before pruning:",
              "digraph G {",
              "  s0 [label=\"()\"]",
              "  s0 -> s1 [label=\"ordering 1\"]",
              "  s0 -> s3 [label=\"ordering 3\"]",
              "  s0 -> s4 [label=\"ordering 4\"]",
              "  s0 -> s5 [label=\"ordering 5\"]",
              "  s0 -> s6 [label=\"ordering 6\"]",
              "  s0 -> s7 [label=\"ordering 7\"]",
              "  s0 -> s8 [label=\"ordering 8\"]",
              "  s0 -> s9 [label=\"ordering 9\"]",
              "  s0 -> s10 [label=\"ordering 10\"]",
              "  s1 [label=\"(sum((lineitem.L_EXTENDEDPRICE * (1 - lineitem.L_DISCOUNT))) DESC, orders.O_ORDERDATE ASC)\", peripheries=2]",
              "  s1 -> s11 [label=\"&epsilon;\"]",
              "  s2 [label=\"{orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}\", peripheries=2]",
              "  s2 -> s12 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s3 [label=\"(lineitem.L_ORDERKEY ASC)\"]",
              "  s3 -> s13 [label=\"&epsilon;\"]",
              "  s4 [label=\"(lineitem.L_ORDERKEY DESC)\"]",
              "  s4 -> s13 [label=\"&epsilon;\"]",
              "  s5 [label=\"(orders.O_ORDERKEY ASC)\"]",
              "  s5 -> s14 [label=\"&epsilon;\"]",
              "  s6 [label=\"(orders.O_ORDERKEY DESC)\"]",
              "  s6 -> s14 [label=\"&epsilon;\"]",
              "  s7 [label=\"(orders.O_ORDERDATE ASC, orders.O_ORDERKEY ASC)\"]",
              "  s7 -> s15 [label=\"&epsilon;\"]",
              "  s7 -> s16 [label=\"&epsilon;\"]",
              "  s8 [label=\"(orders.O_ORDERDATE DESC, orders.O_ORDERKEY DESC)\"]",
              "  s8 -> s15 [label=\"&epsilon;\"]",
              "  s8 -> s9 [label=\"&epsilon;\"]",
              "  s9 [label=\"(orders.O_ORDERDATE DESC)\"]",
              "  s9 -> s17 [label=\"&epsilon;\"]",
              "  s10 [label=\"(orders.O_ORDERDATE ASC, lineitem.L_ORDERKEY ASC, orders.O_SHIPPRIORITY ASC)\"]",
              "  s10 -> s2 [label=\"&epsilon;\"]",
              "  s10 -> s18 [label=\"&epsilon;\"]",
              "  s11 [label=\"(sum((lineitem.L_EXTENDEDPRICE * (1 - lineitem.L_DISCOUNT))) DESC)\"]",
              "  s12 [label=\"{orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}\"]",
              "  s12 -> s2 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s13 [label=\"{lineitem.L_ORDERKEY}\"]",
              "  s13 -> s14 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s14 [label=\"{orders.O_ORDERKEY}\"]",
              "  s14 -> s13 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s14 -> s15 [label=\"{orders.O_ORDERKEY} &rarr; orders.O_ORDERDATE\"]",
              "  s14 -> s19 [label=\"{orders.O_ORDERKEY} &rarr; orders.O_SHIPPRIORITY\"]",
              "  s15 [label=\"{orders.O_ORDERDATE, orders.O_ORDERKEY}\"]",
              "  s15 -> s20 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s15 -> s12 [label=\"{orders.O_ORDERKEY} &rarr; orders.O_SHIPPRIORITY\"]",
              "  s15 -> s12 [label=\"{orders.O_ORDERDATE, orders.O_ORDERKEY} &rarr; orders.O_SHIPPRIORITY\"]",
              "  s16 [label=\"(orders.O_ORDERDATE ASC)\"]",
              "  s16 -> s17 [label=\"&epsilon;\"]",
              "  s17 [label=\"{orders.O_ORDERDATE}\"]",
              "  s18 [label=\"(orders.O_ORDERDATE ASC, lineitem.L_ORDERKEY ASC)\"]",
              "  s18 -> s20 [label=\"&epsilon;\"]",
              "  s18 -> s16 [label=\"&epsilon;\"]",
              "  s19 [label=\"{orders.O_ORDERKEY, orders.O_SHIPPRIORITY}\"]",
              "  s19 -> s21 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s19 -> s12 [label=\"{orders.O_ORDERKEY} &rarr; orders.O_ORDERDATE\"]",
              "  s20 [label=\"{orders.O_ORDERDATE, lineitem.L_ORDERKEY}\"]",
              "  s20 -> s15 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s21 [label=\"{lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}\"]",
              "  s21 -> s19 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "}",
              "",
              "NFSM for interesting orders, after pruning:",
              "digraph G {",
              "  s0 [label=\"()\"]",
              "  s0 -> s1 [label=\"ordering 1\"]",
              "  s0 -> s3 [label=\"ordering 3\"]",
              "  s0 -> s4 [label=\"ordering 4\"]",
              "  s0 -> s5 [label=\"ordering 5\"]",
              "  s0 -> s6 [label=\"ordering 6\"]",
              "  s0 -> s7 [label=\"ordering 7\"]",
              "  s0 -> s8 [label=\"ordering 8\"]",
              "  s0 -> s10 [label=\"ordering 10\"]",
              "  s1 [label=\"(sum((lineitem.L_EXTENDEDPRICE * (1 - lineitem.L_DISCOUNT))) DESC, orders.O_ORDERDATE ASC)\", peripheries=2]",
              "  s2 [label=\"{orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}\", peripheries=2]",
              "  s3 [label=\"(lineitem.L_ORDERKEY ASC)\"]",
              "  s3 -> s13 [label=\"&epsilon;\"]",
              "  s4 [label=\"(lineitem.L_ORDERKEY DESC)\"]",
              "  s4 -> s13 [label=\"&epsilon;\"]",
              "  s5 [label=\"(orders.O_ORDERKEY ASC)\"]",
              "  s5 -> s14 [label=\"&epsilon;\"]",
              "  s6 [label=\"(orders.O_ORDERKEY DESC)\"]",
              "  s6 -> s14 [label=\"&epsilon;\"]",
              "  s7 [label=\"(orders.O_ORDERDATE ASC, orders.O_ORDERKEY ASC)\"]",
              "  s7 -> s15 [label=\"&epsilon;\"]",
              "  s8 [label=\"(orders.O_ORDERDATE DESC, orders.O_ORDERKEY DESC)\"]",
              "  s8 -> s15 [label=\"&epsilon;\"]",
              "  s10 [label=\"(orders.O_ORDERDATE ASC, lineitem.L_ORDERKEY ASC, orders.O_SHIPPRIORITY ASC)\"]",
              "  s10 -> s2 [label=\"&epsilon;\"]",
              "  s10 -> s18 [label=\"&epsilon;\"]",
              "  s12 [label=\"{orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}\"]",
              "  s12 -> s2 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s13 [label=\"{lineitem.L_ORDERKEY}\"]",
              "  s13 -> s14 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s14 [label=\"{orders.O_ORDERKEY}\"]",
              "  s14 -> s13 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s14 -> s15 [label=\"{orders.O_ORDERKEY} &rarr; orders.O_ORDERDATE\"]",
              "  s14 -> s19 [label=\"{orders.O_ORDERKEY} &rarr; orders.O_SHIPPRIORITY\"]",
              "  s15 [label=\"{orders.O_ORDERDATE, orders.O_ORDERKEY}\"]",
              "  s15 -> s20 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s15 -> s12 [label=\"{orders.O_ORDERKEY} &rarr; orders.O_SHIPPRIORITY\"]",
              "  s15 -> s12 [label=\"{orders.O_ORDERDATE, orders.O_ORDERKEY} &rarr; orders.O_SHIPPRIORITY\"]",
              "  s18 [label=\"(orders.O_ORDERDATE ASC, lineitem.L_ORDERKEY ASC)\"]",
              "  s18 -> s20 [label=\"&epsilon;\"]",
              "  s19 [label=\"{orders.O_ORDERKEY, orders.O_SHIPPRIORITY}\"]",
              "  s19 -> s21 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s19 -> s12 [label=\"{orders.O_ORDERKEY} &rarr; orders.O_ORDERDATE\"]",
              "  s20 [label=\"{orders.O_ORDERDATE, lineitem.L_ORDERKEY}\"]",
              "  s20 -> s15 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s21 [label=\"{lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}\"]",
              "  s21 -> s19 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "}",
              "",
              "DFSM for interesting orders:",
              "digraph G {",
              "  s0 [label=< () >]",
              "  s0 -> s1 [label=\"ordering 1\"]",
              "  s0 -> s2 [label=\"ordering 3\"]",
              "  s0 -> s3 [label=\"ordering 4\"]",
              "  s0 -> s4 [label=\"ordering 5\"]",
              "  s0 -> s5 [label=\"ordering 6\"]",
              "  s0 -> s6 [label=\"ordering 7\"]",
              "  s0 -> s7 [label=\"ordering 8\"]",
              "  s0 -> s8 [label=\"ordering 10\"]",
              "  s1 [label=< <b>(sum((lineitem.L_EXTENDEDPRICE * (1 - lineitem.L_DISCOUNT))) DESC, orders.O_ORDERDATE ASC)</b> >, peripheries=2]",
              "  s2 [label=< (lineitem.L_ORDERKEY ASC), {lineitem.L_ORDERKEY} >]",
              "  s2 -> s9 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s3 [label=< (lineitem.L_ORDERKEY DESC), {lineitem.L_ORDERKEY} >]",
              "  s3 -> s10 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s4 [label=< (orders.O_ORDERKEY ASC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERKEY}, {orders.O_ORDERDATE, orders.O_ORDERKEY}, {orders.O_ORDERKEY, orders.O_SHIPPRIORITY} >]",
              "  s4 -> s11 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s5 [label=< (orders.O_ORDERKEY DESC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERKEY}, {orders.O_ORDERDATE, orders.O_ORDERKEY}, {orders.O_ORDERKEY, orders.O_SHIPPRIORITY} >]",
              "  s5 -> s12 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s6 [label=< (orders.O_ORDERDATE ASC, orders.O_ORDERKEY ASC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERDATE, orders.O_ORDERKEY} >]",
              "  s6 -> s13 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s7 [label=< (orders.O_ORDERDATE DESC, orders.O_ORDERKEY DESC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERDATE, orders.O_ORDERKEY} >]",
              "  s7 -> s14 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s8 [label=< <b>{orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}</b>, (orders.O_ORDERDATE ASC, lineitem.L_ORDERKEY ASC, orders.O_SHIPPRIORITY ASC), (orders.O_ORDERDATE ASC, lineitem.L_ORDERKEY ASC), {orders.O_ORDERDATE, lineitem.L_ORDERKEY} >, peripheries=2]",
              "  s8 -> s15 [label=\"lineitem.L_ORDERKEY=orders.O_ORDERKEY\"]",
              "  s9 [label=< <b>{orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}</b>, (lineitem.L_ORDERKEY ASC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {lineitem.L_ORDERKEY}, {orders.O_ORDERKEY}, {orders.O_ORDERDATE, orders.O_ORDERKEY}, {orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERDATE, lineitem.L_ORDERKEY}, {lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY} >, peripheries=2]",
              "  s10 [label=< <b>{orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}</b>, (lineitem.L_ORDERKEY DESC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {lineitem.L_ORDERKEY}, {orders.O_ORDERKEY}, {orders.O_ORDERDATE, orders.O_ORDERKEY}, {orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERDATE, lineitem.L_ORDERKEY}, {lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY} >, peripheries=2]",
              "  s11 [label=< <b>{orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}</b>, (orders.O_ORDERKEY ASC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {lineitem.L_ORDERKEY}, {orders.O_ORDERKEY}, {orders.O_ORDERDATE, orders.O_ORDERKEY}, {orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERDATE, lineitem.L_ORDERKEY}, {lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY} >, peripheries=2]",
              "  s12 [label=< <b>{orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}</b>, (orders.O_ORDERKEY DESC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {lineitem.L_ORDERKEY}, {orders.O_ORDERKEY}, {orders.O_ORDERDATE, orders.O_ORDERKEY}, {orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERDATE, lineitem.L_ORDERKEY}, {lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY} >, peripheries=2]",
              "  s13 [label=< <b>{orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}</b>, (orders.O_ORDERDATE ASC, orders.O_ORDERKEY ASC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERDATE, orders.O_ORDERKEY}, {orders.O_ORDERDATE, lineitem.L_ORDERKEY} >, peripheries=2]",
              "  s14 [label=< <b>{orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}</b>, (orders.O_ORDERDATE DESC, orders.O_ORDERKEY DESC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERDATE, orders.O_ORDERKEY}, {orders.O_ORDERDATE, lineitem.L_ORDERKEY} >, peripheries=2]",
              "  s15 [label=< <b>{orders.O_ORDERDATE, lineitem.L_ORDERKEY, orders.O_SHIPPRIORITY}</b>, (orders.O_ORDERDATE ASC, lineitem.L_ORDERKEY ASC, orders.O_SHIPPRIORITY ASC), {orders.O_ORDERDATE, orders.O_ORDERKEY, orders.O_SHIPPRIORITY}, {orders.O_ORDERDATE, orders.O_ORDERKEY}, (orders.O_ORDERDATE ASC, lineitem.L_ORDERKEY ASC), {orders.O_ORDERDATE, lineitem.L_ORDERKEY} >, peripheries=2]",
              "}",
              "",
              "Enumerating subplans:",
              "",
              "Found node orders [rows=1480013]",
              " - using selectivity 0.500 (740006 rows) from range scan on index I_O_ORDERDATE to cover ((orders.O_ORDERDATE < DATE'1995-03-23'))",
              " - {INDEX_RANGE_SCAN, cost=469419.1, init_cost=0.0, rows=740006.0} [I_O_ORDERDATE range] is first alternative, keeping",
              " - {SORT, cost=1986222.5, init_cost=1986222.5, rows=740006.0, order=6} [I_O_ORDERDATE range, sort(7)] is potential alternative, keeping",
              " - {INDEX_RANGE_SCAN, cost=735826.4, init_cost=0.0, rows=740006.0, order=6} [I_O_ORDERDATE ordered range] is better than 1 others, replacing them",
              " - {INDEX_RANGE_SCAN, cost=735826.4, init_cost=0.0, rows=740006.0, order=7} [I_O_ORDERDATE ordered range] is not better than existing path {INDEX_RANGE_SCAN, cost=735826.4, init_cost=0.0, rows=740006.0, order=6}, discarding",
              " - {TABLE_SCAN, cost=159030.4, init_cost=0.0, rows=740006.0} is better than 1 others, replacing them",
              " - {SORT, cost=1675833.9, init_cost=1675833.9, rows=740006.0, order=6} [sort(7)] is not better than existing path {INDEX_RANGE_SCAN, cost=735826.4, init_cost=0.0, rows=740006.0, order=6}, discarding",
              " - {INDEX_SCAN, cost=159041.5, init_cost=0.0, rows=740006.0, order=4} [PRIMARY] is better than all previous alternatives, replacing all",
              " - PRIMARY is applicable for ref access",
              " - (lineitem.L_ORDERKEY = orders.O_ORDERKEY) is subsumed by ref access on orders.O_ORDERKEY",
              " - {EQ_REF, cost=1.0, init_cost=0.0, rows=0.5, parm={lineitem}, order=4} [PRIMARY] is potential alternative, keeping",
              " - {INDEX_SCAN, cost=159041.5, init_cost=0.0, rows=740006.0, order=5} [PRIMARY] is not better than existing path {INDEX_SCAN, cost=159041.5, init_cost=0.0, rows=740006.0, order=4}, discarding",
              " - PRIMARY is applicable for ref access",
              " - (lineitem.L_ORDERKEY = orders.O_ORDERKEY) is subsumed by ref access on orders.O_ORDERKEY",
              " - {EQ_REF, cost=1.0, init_cost=0.0, rows=0.5, parm={lineitem}, order=5} [PRIMARY] is not better than existing path {EQ_REF, cost=1.0, init_cost=0.0, rows=0.5, parm={lineitem}, order=4}, discarding",
              " - I_O_CUSTKEY is applicable for ref access (using 1/2 key parts only)",
              " - (customer.C_CUSTKEY = orders.O_CUSTKEY) is subsumed by ref access on orders.O_CUSTKEY",
              " - {REF, cost=9.9, init_cost=0.0, rows=5.0, parm={customer}} [I_O_CUSTKEY] is potential alternative, keeping",
              " - I_O_CUSTKEY is applicable for ref access",
              " - (lineitem.L_ORDERKEY = orders.O_ORDERKEY) is subsumed by ref access on orders.O_ORDERKEY",
              " - (customer.C_CUSTKEY = orders.O_CUSTKEY) is subsumed by ref access on orders.O_CUSTKEY",
              " - {EQ_REF, cost=0.9, init_cost=0.0, rows=0.0, parm={lineitem, customer}} [I_O_CUSTKEY] is potential alternative, keeping",
              " - {INDEX_SCAN, cost=1471652.9, init_cost=0.0, rows=740006.0, order=6} [I_O_ORDERDATE] is not better than existing path {INDEX_SCAN, cost=159041.5, init_cost=0.0, rows=740006.0, order=4}, discarding",
              " - {INDEX_SCAN, cost=1471652.9, init_cost=0.0, rows=740006.0, order=7} [I_O_ORDERDATE] is not better than existing path {INDEX_SCAN, cost=159041.5, init_cost=0.0, rows=740006.0, order=4}, discarding",
              " - current access paths for {orders}: {INDEX_SCAN, cost=159041.5, init_cost=0.0, rows=740006.0, order=4}, {EQ_REF, cost=1.0, init_cost=0.0, rows=0.5, parm={lineitem}, order=4}, {REF, cost=9.9, init_cost=0.0, rows=5.0, parm={customer}}, {EQ_REF, cost=0.9, init_cost=0.0, rows=0.0, parm={lineitem, customer}})",
              "",
              "Found node customer [rows=148384]",
              " - {TABLE_SCAN, cost=16664.6, init_cost=0.0, rows=14838.4} is first alternative, keeping",
              " - PRIMARY is applicable for ref access",
              " - (customer.C_CUSTKEY = orders.O_CUSTKEY) is subsumed by ref access on customer.C_CUSTKEY",
              " - {EQ_REF, cost=1.1, init_cost=0.0, rows=0.1, parm={orders}} [PRIMARY] is potential alternative, keeping",
              " - current access paths for {customer}: {TABLE_SCAN, cost=16664.6, init_cost=0.0, rows=14838.4}, {EQ_REF, cost=1.1, init_cost=0.0, rows=0.1, parm={orders}})",
              "",
              "Found sets {orders} and {customer}, connected by condition (customer.C_CUSTKEY = orders.O_CUSTKEY)",
              " - {HASH_JOIN, cost=256370.6, init_cost=18148.5, rows=74000.6, join_order=(orders,customer)} is first alternative, keeping",
              " - {SORT, cost=383468.5, init_cost=383468.5, rows=74000.6, order=6} [sort(7)] is potential alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=3457988047.9, init_cost=0.0, rows=74000.6, join_order=(customer,orders)} is potential alternative, keeping",
              " - {SORT, cost=3458115145.7, init_cost=3458115145.7, rows=74000.6, order=6} [sort(7)] is not better than existing path {SORT, cost=383468.5, init_cost=383468.5, rows=74000.6, order=6}, discarding",
              " - {NESTED_LOOP_JOIN, cost=13430134611.1, init_cost=0.0, rows=74000.6, join_order=(orders,customer), order=4} is potential alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=972735.6, init_cost=0.0, rows=74000.6, join_order=(orders,customer), order=4} is better than 2 others, replacing them",
              " - {NESTED_LOOP_JOIN, cost=164172.1, init_cost=0.0, rows=74000.6, join_order=(customer,orders)} is better than 1 others, replacing them",
              " - {SORT, cost=291270.0, init_cost=291270.0, rows=74000.6, order=6} [sort(7)] is better than 1 others, replacing them",
              " - {NESTED_LOOP_JOIN, cost=29935.4, init_cost=0.0, rows=0.0, join_order=(customer,orders), parm={lineitem}} is potential alternative, keeping",
              " - current access paths for {customer,orders}: {NESTED_LOOP_JOIN, cost=164172.1, init_cost=0.0, rows=74000.6, join_order=(customer,orders)}, {SORT, cost=291270.0, init_cost=291270.0, rows=74000.6, order=6}, {NESTED_LOOP_JOIN, cost=972735.6, init_cost=0.0, rows=74000.6, join_order=(orders,customer), order=4}, {NESTED_LOOP_JOIN, cost=29935.4, init_cost=0.0, rows=0.0, join_order=(customer,orders), parm={lineitem}})",
              "",
              "Found node lineitem [rows=5931117]",
              " - using selectivity 0.500 (2965558 rows) from range scan on index I_L_SHIPDATE to cover ((lineitem.L_SHIPDATE > DATE'1995-03-23'))",
              " - {INDEX_RANGE_SCAN, cost=3011791.2, init_cost=0.0, rows=2965558.0} [I_L_SHIPDATE range] is first alternative, keeping",
              " - {TABLE_SCAN, cost=648456.2, init_cost=0.0, rows=2965558.0} is better than previous {INDEX_RANGE_SCAN, cost=3011791.2, init_cost=0.0, rows=2965558.0}, replacing",
              " - {INDEX_SCAN, cost=648511.6, init_cost=0.0, rows=2965558.0, order=2} [PRIMARY] is better than previous {TABLE_SCAN, cost=648456.2, init_cost=0.0, rows=2965558.0}, replacing",
              " - PRIMARY is applicable for ref access (using 1/2 key parts only)",
              " - (lineitem.L_ORDERKEY = orders.O_ORDERKEY) is subsumed by ref access on lineitem.L_ORDERKEY",
              " - {REF, cost=1.4, init_cost=0.0, rows=2.0, parm={orders}, order=2} [PRIMARY] is potential alternative, keeping",
              " - {INDEX_SCAN, cost=648511.6, init_cost=0.0, rows=2965558.0, order=3} [PRIMARY] is not better than existing path {INDEX_SCAN, cost=648511.6, init_cost=0.0, rows=2965558.0, order=2}, discarding",
              " - PRIMARY is applicable for ref access (using 1/2 key parts only)",
              " - (lineitem.L_ORDERKEY = orders.O_ORDERKEY) is subsumed by ref access on lineitem.L_ORDERKEY",
              " - {REF, cost=1.4, init_cost=0.0, rows=2.0, parm={orders}, order=3} [PRIMARY] is not better than existing path {REF, cost=1.4, init_cost=0.0, rows=2.0, parm={orders}, order=2}, discarding",
              " - {INDEX_SCAN, cost=6502080.7, init_cost=0.0, rows=2965558.0, order=2} [I_L_ORDERKEY] is not better than existing path {INDEX_SCAN, cost=648511.6, init_cost=0.0, rows=2965558.0, order=2}, discarding",
              " - I_L_ORDERKEY is applicable for ref access (using 1/2 key parts only)",
              " - (lineitem.L_ORDERKEY = orders.O_ORDERKEY) is subsumed by ref access on lineitem.L_ORDERKEY",
              " - {REF, cost=5.4, init_cost=0.0, rows=2.0, parm={orders}, order=2} [I_L_ORDERKEY] is not better than existing path {REF, cost=1.4, init_cost=0.0, rows=2.0, parm={orders}, order=2}, discarding",
              " - {INDEX_SCAN, cost=6502080.7, init_cost=0.0, rows=2965558.0, order=3} [I_L_ORDERKEY] is not better than existing path {INDEX_SCAN, cost=648511.6, init_cost=0.0, rows=2965558.0, order=2}, discarding",
              " - I_L_ORDERKEY is applicable for ref access (using 1/2 key parts only)",
              " - (lineitem.L_ORDERKEY = orders.O_ORDERKEY) is subsumed by ref access on lineitem.L_ORDERKEY",
              " - {REF, cost=5.4, init_cost=0.0, rows=2.0, parm={orders}, order=3} [I_L_ORDERKEY] is not better than existing path {REF, cost=1.4, init_cost=0.0, rows=2.0, parm={orders}, order=2}, discarding",
              " - current access paths for {lineitem}: {INDEX_SCAN, cost=648511.6, init_cost=0.0, rows=2965558.0, order=2}, {REF, cost=1.4, init_cost=0.0, rows=2.0, parm={orders}, order=2})",
              "",
              "Found sets {lineitem} and {orders}, connected by condition (lineitem.L_ORDERKEY = orders.O_ORDERKEY)",
              " - {HASH_JOIN, cost=1281903.9, init_cost=233042.1, rows=1482778.0, join_order=(lineitem,orders)} is first alternative, keeping",
              " - {SORT, cost=4469857.5, init_cost=4469857.5, rows=1482778.0, order=13} [sort(7)] is potential alternative, keeping",
              " - {SORT, cost=4469857.5, init_cost=4469857.5, rows=1482778.0, order=15} [sort(10)] is not better than existing path {SORT, cost=4469857.5, init_cost=4469857.5, rows=1482778.0, order=13}, discarding",
              " - {NESTED_LOOP_JOIN, cost=691100399599.0, init_cost=0.0, rows=1482778.0, join_order=(lineitem,orders), order=9} is potential alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=699355700035.7, init_cost=0.0, rows=1482778.0, join_order=(orders,lineitem), order=11} is not better than existing path {NESTED_LOOP_JOIN, cost=691100399599.0, init_cost=0.0, rows=1482778.0, join_order=(lineitem,orders), order=9}, discarding",
              " - {NESTED_LOOP_JOIN, cost=1201520.6, init_cost=0.0, rows=1482778.0, join_order=(orders,lineitem), order=11} is better than all previous alternatives, replacing all",
              " - {NESTED_LOOP_JOIN, cost=3597316.3, init_cost=0.0, rows=1482778.0, join_order=(lineitem,orders), order=9} is not better than existing path {NESTED_LOOP_JOIN, cost=1201520.6, init_cost=0.0, rows=1482778.0, join_order=(orders,lineitem), order=11}, discarding",
              " - {NESTED_LOOP_JOIN, cost=3300762.5, init_cost=0.0, rows=10.0, join_order=(lineitem,orders), parm={customer}, order=9} is potential alternative, keeping",
              " - current access paths for {lineitem,orders}: {NESTED_LOOP_JOIN, cost=1201520.6, init_cost=0.0, rows=1482778.0, join_order=(orders,lineitem), order=11}, {NESTED_LOOP_JOIN, cost=3300762.5, init_cost=0.0, rows=10.0, join_order=(lineitem,orders), parm={customer}, order=9})",
              "",
              "Found sets {lineitem} and {customer,orders}, connected by condition (lineitem.L_ORDERKEY = orders.O_ORDERKEY)",
              " - {HASH_JOIN, cost=1127019.0, init_cost=171572.2, rows=148277.8, join_order=(lineitem,(customer,orders))} is first alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=508807824143.9, init_cost=0.0, rows=148277.8, join_order=(lineitem,(customer,orders)), order=9} is potential alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=69935719313.6, init_cost=0.0, rows=148277.8, join_order=((customer,orders),lineitem)} is potential alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=268420.0, init_cost=0.0, rows=148277.8, join_order=((customer,orders),lineitem)} is better than 2 others, replacing them",
              " - {HASH_JOIN, cost=1254116.9, init_cost=298670.0, rows=148277.8, join_order=(lineitem,(customer,orders))} is not better than existing path {NESTED_LOOP_JOIN, cost=268420.0, init_cost=0.0, rows=148277.8, join_order=((customer,orders),lineitem)}, discarding",
              " - {NESTED_LOOP_JOIN, cost=885723952263.1, init_cost=0.0, rows=148277.8, join_order=(lineitem,(customer,orders)), order=9} is not better than existing path {NESTED_LOOP_JOIN, cost=508807824143.9, init_cost=0.0, rows=148277.8, join_order=(lineitem,(customer,orders)), order=9}, discarding",
              " - {NESTED_LOOP_JOIN, cost=69935846411.5, init_cost=291270.0, rows=148277.8, join_order=((customer,orders),lineitem), order=13} is potential alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=395517.9, init_cost=291270.0, rows=148277.8, join_order=((customer,orders),lineitem), order=13} is better than 1 others, replacing them",
              " - {HASH_JOIN, cost=1935582.5, init_cost=980135.6, rows=148277.8, join_order=(lineitem,(orders,customer))} is not better than existing path {NESTED_LOOP_JOIN, cost=268420.0, init_cost=0.0, rows=148277.8, join_order=((customer,orders),lineitem)}, discarding",
              " - {NESTED_LOOP_JOIN, cost=2906649676018.4, init_cost=0.0, rows=148277.8, join_order=(lineitem,(orders,customer)), order=9} is not better than existing path {NESTED_LOOP_JOIN, cost=508807824143.9, init_cost=0.0, rows=148277.8, join_order=(lineitem,(customer,orders)), order=9}, discarding",
              " - {NESTED_LOOP_JOIN, cost=69936527877.1, init_cost=0.0, rows=148277.8, join_order=((orders,customer),lineitem), order=11} is better than 1 others, replacing them",
              " - {NESTED_LOOP_JOIN, cost=1076983.5, init_cost=0.0, rows=148277.8, join_order=((orders,customer),lineitem), order=11} is better than 1 others, replacing them",
              " - {NESTED_LOOP_JOIN, cost=88775730556.2, init_cost=0.0, rows=148277.8, join_order=(lineitem,(customer,orders)), order=9} is not better than existing path {NESTED_LOOP_JOIN, cost=1076983.5, init_cost=0.0, rows=148277.8, join_order=((orders,customer),lineitem), order=11}, discarding",
              " - current access paths for {lineitem,customer,orders}: {NESTED_LOOP_JOIN, cost=268420.0, init_cost=0.0, rows=148277.8, join_order=((customer,orders),lineitem)}, {NESTED_LOOP_JOIN, cost=1076983.5, init_cost=0.0, rows=148277.8, join_order=((orders,customer),lineitem), order=11}, {NESTED_LOOP_JOIN, cost=395517.9, init_cost=291270.0, rows=148277.8, join_order=((customer,orders),lineitem), order=13})",
              "",
              "Found sets {lineitem,orders} and {customer}, connected by condition (customer.C_CUSTKEY = orders.O_CUSTKEY)",
              " - {HASH_JOIN, cost=1378326.3, init_cost=18148.5, rows=148277.8, join_order=((orders,lineitem),customer)} is not better than existing path {NESTED_LOOP_JOIN, cost=268420.0, init_cost=0.0, rows=148277.8, join_order=((customer,orders),lineitem)}, discarding",
              " - {NESTED_LOOP_JOIN, cost=26911351289.9, init_cost=0.0, rows=148277.8, join_order=((orders,lineitem),customer), order=11} is not better than existing path {NESTED_LOOP_JOIN, cost=1076983.5, init_cost=0.0, rows=148277.8, join_order=((orders,customer),lineitem), order=11}, discarding",
              " - {NESTED_LOOP_JOIN, cost=20028865867.4, init_cost=0.0, rows=148277.8, join_order=(customer,(orders,lineitem))} is not better than existing path {NESTED_LOOP_JOIN, cost=268420.0, init_cost=0.0, rows=148277.8, join_order=((customer,orders),lineitem)}, discarding",
              " - {NESTED_LOOP_JOIN, cost=48978051014.6, init_cost=0.0, rows=148277.8, join_order=(customer,(lineitem,orders))} is not better than existing path {NESTED_LOOP_JOIN, cost=268420.0, init_cost=0.0, rows=148277.8, join_order=((customer,orders),lineitem)}, discarding",
              " - {NESTED_LOOP_JOIN, cost=2831950.2, init_cost=0.0, rows=148277.8, join_order=((orders,lineitem),customer), order=11} is not better than existing path {NESTED_LOOP_JOIN, cost=1076983.5, init_cost=0.0, rows=148277.8, join_order=((orders,customer),lineitem), order=11}, discarding",
              " - current access paths for {lineitem,customer,orders}: {NESTED_LOOP_JOIN, cost=268420.0, init_cost=0.0, rows=148277.8, join_order=((customer,orders),lineitem)}, {NESTED_LOOP_JOIN, cost=1076983.5, init_cost=0.0, rows=148277.8, join_order=((orders,customer),lineitem), order=11}, {NESTED_LOOP_JOIN, cost=395517.9, init_cost=291270.0, rows=148277.8, join_order=((customer,orders),lineitem), order=13})",
              "",
              "Enumerated 6 subplans keeping a total of 17 access paths, got 3 candidate(s) to finalize:",
              "Adding final predicates",
              " - {NESTED_LOOP_JOIN, cost=268420.0, init_cost=0.0, rows=148277.8, join_order=((customer,orders),lineitem)} is first alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=1076983.5, init_cost=0.0, rows=148277.8, join_order=((orders,customer),lineitem), order=11} is potential alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=395517.9, init_cost=291270.0, rows=148277.8, join_order=((customer,orders),lineitem), order=13} is potential alternative, keeping",
              "Applying aggregation for GROUP BY",
              "",
              "Estimating row count for aggregation on 3 terms.",
              "Adding prefix: [index: 'PRIMARY' on 'lineitem', fields: 'L_ORDERKEY']",
              "Adding prefix: [index: 'I_L_ORDERKEY' on 'lineitem', fields: 'L_ORDERKEY']",
              "Adding prefix: [index: 'I_O_ORDERDATE' on 'orders', fields: 'O_ORDERDATE']",
              "Choosing longest prefix [index: 'PRIMARY' on 'lineitem', fields: 'L_ORDERKEY'] with estimated distinct values: 1480007.0",
              "Shortening prefix [index: 'I_L_ORDERKEY' on 'lineitem', fields: 'L_ORDERKEY']",
              "  into  [index: 'I_L_ORDERKEY' on 'lineitem', fields: ''],",
              "  since field 'L_ORDERKEY' is already covered by an earlier estimate.",
              "Choosing longest prefix [index: 'I_O_ORDERDATE' on 'orders', fields: 'O_ORDERDATE'] with estimated distinct values: 2423.0",
              "Estimating 1216.6 distinct values for field 'O_SHIPPRIORITY' from table size.",
              "Estimating 1.0 distinct values for 0 non-field terms and 31975659423.1 in total.",
              " - {AGGREGATE, cost=552786.3, init_cost=537958.6, rows=45078.4} [sort(2)] is first alternative, keeping",
              " - {AGGREGATE, cost=552786.3, init_cost=537958.6, rows=45078.4, order=13} [sort(7)] is better than previous {AGGREGATE, cost=552786.3, init_cost=537958.6, rows=45078.4}, replacing",
              " - {AGGREGATE, cost=552786.3, init_cost=537958.6, rows=45078.4, order=15} [sort(10)] is not better than existing path {AGGREGATE, cost=552786.3, init_cost=537958.6, rows=45078.4, order=13}, discarding",
              " - {AGGREGATE, cost=1091811.3, init_cost=0.0, rows=45078.4, order=11} [sort elided] is potential alternative, keeping",
              " - {AGGREGATE, cost=410345.7, init_cost=291270.0, rows=45078.4, order=13} [sort elided] is better than 1 others, replacing them",
              "Applying sort for ORDER BY",
              " - {SORT, cost=414856.8, init_cost=414856.8, rows=10.0} is first alternative, keeping",
              " - {SORT, cost=1096322.4, init_cost=1096322.4, rows=10.0} is not better than existing path {SORT, cost=414856.8, init_cost=414856.8, rows=10.0}, discarding",
              "Final cost is 414856.8."
            ]
          }
        ]
      }
    },
    {
      "join_execution": {
        "select#": 1,
        "steps": [
          {
            "filesort_information": [
              {
                "direction": "asc",
                "expression": "`orders`.`O_ORDERDATE`"
              },
              {
                "direction": "asc",
                "expression": "`orders`.`O_ORDERKEY`"
              }
            ],
            "filesort_priority_queue_optimization": {
              "usable": false,
              "cause": "not applicable (no LIMIT)"
            },
            "filesort_execution": [
            ],
            "filesort_summary": {
              "memory_available": 262144,
              "key_size": 16,
              "row_size": 80,
              "max_rows_per_buffer": 3276,
              "num_rows_estimate": 74001,
              "num_rows_found": 146135,
              "num_initial_chunks_spilled_to_disk": 36,
              "peak_memory_used": 294912,
              "sort_algorithm": "std::stable_sort",
              "sort_mode": "<fixed_sort_key, packed_additional_fields>"
            }
          },
          {
            "sorting_table": "<temporary>",
            "filesort_information": [
              {
                "direction": "desc",
                "expression": "`revenue`"
              },
              {
                "direction": "asc",
                "expression": "`orders`.`o_orderdate`"
              }
            ],
            "filesort_priority_queue_optimization": {
              "limit": 10,
              "chosen": true
            },
            "filesort_execution": [
            ],
            "filesort_summary": {
              "memory_available": 262144,
              "key_size": 34,
              "row_size": 70,
              "max_rows_per_buffer": 11,
              "num_rows_estimate": 45078,
              "num_rows_found": 11356,
              "num_initial_chunks_spilled_to_disk": 0,
              "peak_memory_used": 858,
              "sort_algorithm": "std::sort",
              "unpacked_addon_fields": "using_priority_queue",
              "sort_mode": "<fixed_sort_key, additional_fields>"
            }
          }
        ]
      }
    }
  ]
}
MISSING_BYTES_BEYOND_MAX_MEM_SIZE: 0
          INSUFFICIENT_PRIVILEGES: 0
1 row in set (0.01 sec)

mysql> 











mysql> SELECT * FROM `information_schema`.`OPTIMIZER_TRACE`\G
*************************** 1. row ***************************
                            QUERY: select t1.* from NATION t1 ,NATION t2,NATION t3 where t1.N_REGIONKEY+t2.N_REGIONKEY=t3.N_REGIONKEY and t3.N_NATIONKEY=0
                            TRACE: {
  "steps": [
    {
      "join_preparation": {
        "select#": 1,
        "steps": [
          {
            "expanded_query": "/* select#1 */ select `t1`.`N_NATIONKEY` AS `N_NATIONKEY`,`t1`.`N_NAME` AS `N_NAME`,`t1`.`N_REGIONKEY` AS `N_REGIONKEY`,`t1`.`N_COMMENT` AS `N_COMMENT` from `nation` `t1` join `nation` `t2` join `nation` `t3` where (((`t1`.`N_REGIONKEY` + `t2`.`N_REGIONKEY`) = `t3`.`N_REGIONKEY`) and (`t3`.`N_NATIONKEY` = 0))"
          }
        ]
      }
    },
    {
      "join_optimization": {
        "select#": 1,
        "steps": [
          {
            "condition_processing": {
              "condition": "WHERE",
              "original_condition": "(((`t1`.`N_REGIONKEY` + `t2`.`N_REGIONKEY`) = `t3`.`N_REGIONKEY`) and (`t3`.`N_NATIONKEY` = 0))",
              "steps": [
                {
                  "transformation": "equality_propagation",
                  "resulting_condition": "(((`t1`.`N_REGIONKEY` + `t2`.`N_REGIONKEY`) = `t3`.`N_REGIONKEY`) and multiple equal(0, `t3`.`N_NATIONKEY`))"
                },
                {
                  "transformation": "constant_propagation",
                  "resulting_condition": "(((`t1`.`N_REGIONKEY` + `t2`.`N_REGIONKEY`) = `t3`.`N_REGIONKEY`) and multiple equal(0, `t3`.`N_NATIONKEY`))"
                },
                {
                  "transformation": "trivial_condition_removal",
                  "resulting_condition": "(((`t1`.`N_REGIONKEY` + `t2`.`N_REGIONKEY`) = `t3`.`N_REGIONKEY`) and multiple equal(0, `t3`.`N_NATIONKEY`))"
                }
              ]
            }
          },
          {
            "substitute_generated_columns": {
            }
          },
          [
            {
              "index": "PRIMARY",
              "usable": true,
              "key_parts": [
                "N_NATIONKEY"
              ]
            },
            {
              "index": "I_N_REGIONKEY",
              "usable": true,
              "key_parts": [
                "N_REGIONKEY",
                "N_NATIONKEY"
              ]
            }
          ],
          [
            {
              "index": "PRIMARY",
              "usable": true,
              "key_parts": [
                "N_NATIONKEY"
              ]
            },
            {
              "index": "I_N_REGIONKEY",
              "usable": true,
              "key_parts": [
                "N_REGIONKEY",
                "N_NATIONKEY"
              ]
            }
          ],
          {
            "join_optimizer": [
              "Join list after simplification:",
              "* t3  join_type=inner",
              "* t2  join_type=inner",
              "* t1  join_type=inner",
              "",
              "Made this relational tree; WHERE condition is (((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) and multiple equal(0, t3.N_NATIONKEY)):",
              "* Inner join [companion set 0xffff6cbfcf70] (flattened)",
              "  * t1 [companion set 0xffff6cbfcf70]",
              "  * t2 [companion set 0xffff6cbfcf70]",
              "  * t3 [companion set 0xffff6cbfcf70]",
              "",
              "Pushing conditions down.",
              "",
              "After pushdown; remaining WHERE conditions are (t3.N_NATIONKEY = 0), table filters are (none):",
              "* Inner join [companion set 0xffff6cbfcf70] (equijoin condition = ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY))",
              "  * Inner join [companion set 0xffff6cbfcf70] (no join conditions)",
              "    * t1 [companion set 0xffff6cbfcf70]",
              "    * t2 [companion set 0xffff6cbfcf70]",
              "  * t3 [companion set 0xffff6cbfcf70]",
              "",
              "Companion set: 0xffff6cbfcf70:{}",
              "Selectivity of join (none):",
              "Selectivity of join ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY):",
              " - fallback selectivity for ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) = 1",
              "",
              "Constructed hypergraph:",
              "digraph G {  # 2 edges",
              "  t1 -> t2 [label=\"(none) (1)\",arrowhead=none]",
              "  e2 [shape=circle,width=.001,height=.001,label=\"\"]",
              "  t1 -> e2 [arrowhead=none,label=\"\"]",
              "  t2 -> e2 [arrowhead=none,label=\"\"]",
              "  e2 -> t3 [label=\"((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) (1)\",arrowhead=none]",
              "}",
              "",
              " - capping selectivity to 0.04 since index is unique",
              " - fallback selectivity for (t3.N_NATIONKEY = 0) = 0.04",
              "Total eligibility set for (t3.N_NATIONKEY = 0): {t3}",
              "",
              "Found sargable condition (t3.N_NATIONKEY = 0)",
              "Found sargable join condition ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) on t3",
              " - fallback selectivity for ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) = 1",
              " - fallback selectivity for ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) = 1",
              "",
              "No interesting orders found. Not collecting functional dependencies.",
              "",
              "",
              "Enumerating subplans:",
              "",
              "Found node t3 [rows=25]",
              " - PRIMARY is applicable for ref access",
              " - (t3.N_NATIONKEY = 0) is subsumed by ref access on t3.N_NATIONKEY",
              " - {EQ_REF, cost=0.2, init_cost=0.0, rows=1.0} [PRIMARY] is first alternative, keeping",
              " - current access paths for {t3}: {EQ_REF, cost=0.2, init_cost=0.0, rows=1.0})",
              "",
              "Found node t2 [rows=25]",
              " - {TABLE_SCAN, cost=0.2, init_cost=0.0, rows=25.0} is first alternative, keeping",
              " - {INDEX_SCAN, cost=1.0, init_cost=0.0, rows=25.0} [I_N_REGIONKEY] is not better than existing path {TABLE_SCAN, cost=0.2, init_cost=0.0, rows=25.0}, discarding",
              " - current access paths for {t2}: {TABLE_SCAN, cost=0.2, init_cost=0.0, rows=25.0})",
              "",
              "Found node t1 [rows=25]",
              " - {TABLE_SCAN, cost=0.2, init_cost=0.0, rows=25.0} is first alternative, keeping",
              " - current access paths for {t1}: {TABLE_SCAN, cost=0.2, init_cost=0.0, rows=25.0})",
              "",
              "Found sets {t1} and {t2}, connected by condition (none)",
              " - {HASH_JOIN, cost=49.3, init_cost=2.8, rescan_cost=46.5, rows=625.0, join_order=(t1,t2)} is first alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=6.5, init_cost=0.0, rows=625.0, join_order=(t1,t2)} is better than previous {HASH_JOIN, cost=49.3, init_cost=2.8, rescan_cost=46.5, rows=625.0, join_order=(t1,t2)}, replacing",
              " - {NESTED_LOOP_JOIN, cost=6.5, init_cost=0.0, rows=625.0, join_order=(t2,t1)} is not better than existing path {NESTED_LOOP_JOIN, cost=6.5, init_cost=0.0, rows=625.0, join_order=(t1,t2)}, discarding",
              " - current access paths for {t1,t2}: {NESTED_LOOP_JOIN, cost=6.5, init_cost=0.0, rows=625.0, join_order=(t1,t2)})",
              "",
              "Found sets {t1,t2} and {t3}, connected by condition ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY)",
              " - {HASH_JOIN, cost=113.1, init_cost=0.3, rescan_cost=112.8, rows=625.0, join_order=((t1,t2),t3)} is first alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=225.2, init_cost=0.0, rows=625.0, join_order=((t1,t2),t3)} is potential alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=69.2, init_cost=0.0, rows=625.0, join_order=(t3,(t1,t2))} is better than all previous alternatives, replacing all",
              " - current access paths for {t1,t2,t3}: {NESTED_LOOP_JOIN, cost=69.2, init_cost=0.0, rows=625.0, join_order=(t3,(t1,t2))})",
              "",
              "Enumerated 5 subplans keeping a total of 5 access paths, got 1 candidate(s) to finalize:",
              "Adding final predicates",
              " - {NESTED_LOOP_JOIN, cost=69.2, init_cost=0.0, rows=625.0, join_order=(t3,(t1,t2))} is first alternative, keeping",
              "Final cost is 69.2."
            ]
          }
        ]
      }
    },
    {
      "join_execution": {
        "select#": 1,
        "steps": [
        ]
      }
    }
  ]
}
MISSING_BYTES_BEYOND_MAX_MEM_SIZE: 0
          INSUFFICIENT_PRIVILEGES: 0
1 row in set (0.00 sec)



















mysql> SELECT * FROM `information_schema`.`OPTIMIZER_TRACE`\G
*************************** 1. row ***************************
                            QUERY: select t1.* from NATION t1 ,NATION t2,NATION t3 where t1.N_REGIONKEY+t2.N_REGIONKEY=t3.N_REGIONKEY and t3.N_NATIONKEY=0 and t2.N_NATIONKEY=1
                            TRACE: {
  "steps": [
    {
      "join_preparation": {
        "select#": 1,
        "steps": [
          {
            "expanded_query": "/* select#1 */ select `t1`.`N_NATIONKEY` AS `N_NATIONKEY`,`t1`.`N_NAME` AS `N_NAME`,`t1`.`N_REGIONKEY` AS `N_REGIONKEY`,`t1`.`N_COMMENT` AS `N_COMMENT` from `nation` `t1` join `nation` `t2` join `nation` `t3` where (((`t1`.`N_REGIONKEY` + `t2`.`N_REGIONKEY`) = `t3`.`N_REGIONKEY`) and (`t3`.`N_NATIONKEY` = 0) and (`t2`.`N_NATIONKEY` = 1))"
          }
        ]
      }
    },
    {
      "join_optimization": {
        "select#": 1,
        "steps": [
          {
            "condition_processing": {
              "condition": "WHERE",
              "original_condition": "(((`t1`.`N_REGIONKEY` + `t2`.`N_REGIONKEY`) = `t3`.`N_REGIONKEY`) and (`t3`.`N_NATIONKEY` = 0) and (`t2`.`N_NATIONKEY` = 1))",
              "steps": [
                {
                  "transformation": "equality_propagation",
                  "resulting_condition": "(((`t1`.`N_REGIONKEY` + `t2`.`N_REGIONKEY`) = `t3`.`N_REGIONKEY`) and multiple equal(0, `t3`.`N_NATIONKEY`) and multiple equal(1, `t2`.`N_NATIONKEY`))"
                },
                {
                  "transformation": "constant_propagation",
                  "resulting_condition": "(((`t1`.`N_REGIONKEY` + `t2`.`N_REGIONKEY`) = `t3`.`N_REGIONKEY`) and multiple equal(0, `t3`.`N_NATIONKEY`) and multiple equal(1, `t2`.`N_NATIONKEY`))"
                },
                {
                  "transformation": "trivial_condition_removal",
                  "resulting_condition": "(((`t1`.`N_REGIONKEY` + `t2`.`N_REGIONKEY`) = `t3`.`N_REGIONKEY`) and multiple equal(0, `t3`.`N_NATIONKEY`) and multiple equal(1, `t2`.`N_NATIONKEY`))"
                }
              ]
            }
          },
          {
            "substitute_generated_columns": {
            }
          },
          [
            {
              "index": "PRIMARY",
              "usable": true,
              "key_parts": [
                "N_NATIONKEY"
              ]
            },
            {
              "index": "I_N_REGIONKEY",
              "usable": true,
              "key_parts": [
                "N_REGIONKEY",
                "N_NATIONKEY"
              ]
            }
          ],
          {
            "join_optimizer": [
              "Join list after simplification:",
              "* t3  join_type=inner",
              "* t2  join_type=inner",
              "* t1  join_type=inner",
              "",
              "Made this relational tree; WHERE condition is (((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) and multiple equal(0, t3.N_NATIONKEY) and multiple equal(1, t2.N_NATIONKEY)):",
              "* Inner join [companion set 0xffff6cbfd9e8] (flattened)",
              "  * t1 [companion set 0xffff6cbfd9e8]",
              "  * t2 [companion set 0xffff6cbfd9e8]",
              "  * t3 [companion set 0xffff6cbfd9e8]",
              "",
              "Pushing conditions down.",
              "",
              "After pushdown; remaining WHERE conditions are (t3.N_NATIONKEY = 0) AND (t2.N_NATIONKEY = 1), table filters are (none):",
              "* Inner join [companion set 0xffff6cbfd9e8] (equijoin condition = ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY))",
              "  * Inner join [companion set 0xffff6cbfd9e8] (no join conditions)",
              "    * t1 [companion set 0xffff6cbfd9e8]",
              "    * t2 [companion set 0xffff6cbfd9e8]",
              "  * t3 [companion set 0xffff6cbfd9e8]",
              "",
              "Companion set: 0xffff6cbfd9e8:{}",
              "Selectivity of join (none):",
              "Selectivity of join ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY):",
              " - fallback selectivity for ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) = 1",
              "",
              "Constructed hypergraph:",
              "digraph G {  # 2 edges",
              "  t1 -> t2 [label=\"(none) (1)\",arrowhead=none]",
              "  e2 [shape=circle,width=.001,height=.001,label=\"\"]",
              "  t1 -> e2 [arrowhead=none,label=\"\"]",
              "  t2 -> e2 [arrowhead=none,label=\"\"]",
              "  e2 -> t3 [label=\"((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) (1)\",arrowhead=none]",
              "}",
              "",
              " - capping selectivity to 0.04 since index is unique",
              " - fallback selectivity for (t3.N_NATIONKEY = 0) = 0.04",
              "Total eligibility set for (t3.N_NATIONKEY = 0): {t3}",
              " - capping selectivity to 0.04 since index is unique",
              " - fallback selectivity for (t2.N_NATIONKEY = 1) = 0.04",
              "Total eligibility set for (t2.N_NATIONKEY = 1): {t2}",
              "",
              "Found sargable condition (t3.N_NATIONKEY = 0)",
              "Found sargable condition (t2.N_NATIONKEY = 1)",
              "Found sargable join condition ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) on t3",
              " - fallback selectivity for ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) = 1",
              " - fallback selectivity for ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY) = 1",
              "",
              "No interesting orders found. Not collecting functional dependencies.",
              "",
              "",
              "Enumerating subplans:",
              "",
              "Found node t3 [rows=25]",
              " - PRIMARY is applicable for ref access",
              " - (t3.N_NATIONKEY = 0) is subsumed by ref access on t3.N_NATIONKEY",
              " - {EQ_REF, cost=0.2, init_cost=0.0, rows=1.0} [PRIMARY] is first alternative, keeping",
              " - current access paths for {t3}: {EQ_REF, cost=0.2, init_cost=0.0, rows=1.0})",
              "",
              "Found node t2 [rows=25]",
              " - PRIMARY is applicable for ref access",
              " - (t2.N_NATIONKEY = 1) is subsumed by ref access on t2.N_NATIONKEY",
              " - {EQ_REF, cost=0.2, init_cost=0.0, rows=1.0} [PRIMARY] is first alternative, keeping",
              " - current access paths for {t2}: {EQ_REF, cost=0.2, init_cost=0.0, rows=1.0})",
              "",
              "Found node t1 [rows=25]",
              " - {TABLE_SCAN, cost=0.2, init_cost=0.0, rows=25.0} is first alternative, keeping",
              " - current access paths for {t1}: {TABLE_SCAN, cost=0.2, init_cost=0.0, rows=25.0})",
              "",
              "Found sets {t1} and {t2}, connected by condition (none)",
              " - {HASH_JOIN, cost=4.8, init_cost=0.3, rescan_cost=4.5, rows=25.0, join_order=(t1,t2)} is first alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=6.5, init_cost=0.0, rows=25.0, join_order=(t1,t2)} is potential alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=0.5, init_cost=0.0, rows=25.0, join_order=(t2,t1)} is better than all previous alternatives, replacing all",
              " - current access paths for {t1,t2}: {NESTED_LOOP_JOIN, cost=0.5, init_cost=0.0, rows=25.0, join_order=(t2,t1)})",
              "",
              "Found sets {t1,t2} and {t3}, connected by condition ((t1.N_REGIONKEY + t2.N_REGIONKEY) = t3.N_REGIONKEY)",
              " - {HASH_JOIN, cost=5.1, init_cost=0.3, rescan_cost=4.8, rows=25.0, join_order=((t2,t1),t3)} is first alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=9.2, init_cost=0.0, rows=25.0, join_order=((t2,t1),t3)} is potential alternative, keeping",
              " - {NESTED_LOOP_JOIN, cost=3.2, init_cost=0.0, rows=25.0, join_order=(t3,(t2,t1))} is better than all previous alternatives, replacing all",
              " - current access paths for {t1,t2,t3}: {NESTED_LOOP_JOIN, cost=3.2, init_cost=0.0, rows=25.0, join_order=(t3,(t2,t1))})",
              "",
              "Enumerated 5 subplans keeping a total of 5 access paths, got 1 candidate(s) to finalize:",
              "Adding final predicates",
              " - {NESTED_LOOP_JOIN, cost=3.2, init_cost=0.0, rows=25.0, join_order=(t3,(t2,t1))} is first alternative, keeping",
              "Final cost is 3.2."
            ]
          }
        ]
      }
    },
    {
      "join_execution": {
        "select#": 1,
        "steps": [
        ]
      }
    }
  ]
}
MISSING_BYTES_BEYOND_MAX_MEM_SIZE: 0
          INSUFFICIENT_PRIVILEGES: 0
1 row in set (0.04 sec)

mysql> 