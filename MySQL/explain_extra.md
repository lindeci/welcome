
- [EXPLAIN Extra Information](#explain-extra-information)
  - [Backward index scan (JSON: backward\_index\_scan)](#backward-index-scan-json-backward_index_scan)
  - [Child of 'table' pushed join@1 (JSON: message text)](#child-of-table-pushed-join1-json-message-text)
  - [const row not found (JSON property: const\_row\_not\_found)](#const-row-not-found-json-property-const_row_not_found)
  - [Deleting all rows (JSON property: message)](#deleting-all-rows-json-property-message)
  - [Distinct (JSON property: distinct)](#distinct-json-property-distinct)
  - [FirstMatch(tbl\_name) (JSON property: first\_match)](#firstmatchtbl_name-json-property-first_match)
  - [Full scan on NULL key (JSON property: message)](#full-scan-on-null-key-json-property-message)
  - [Impossible HAVING (JSON property: message)](#impossible-having-json-property-message)
  - [Impossible WHERE (JSON property: message)](#impossible-where-json-property-message)
  - [Impossible WHERE noticed after reading const tables (JSON property: message)](#impossible-where-noticed-after-reading-const-tables-json-property-message)
  - [LooseScan(m..n) (JSON property: message)](#loosescanmn-json-property-message)
  - [No matching min/max row (JSON property: message)](#no-matching-minmax-row-json-property-message)
  - [no matching row in const table (JSON property: message)](#no-matching-row-in-const-table-json-property-message)
  - [No matching rows after partition pruning (JSON property: message)](#no-matching-rows-after-partition-pruning-json-property-message)
  - [No tables used (JSON property: message)](#no-tables-used-json-property-message)
  - [Not exists (JSON property: message)](#not-exists-json-property-message)
  - [Plan isn't ready yet (JSON property: none)](#plan-isnt-ready-yet-json-property-none)
  - [Range checked for each record (index map: N) (JSON property: message)](#range-checked-for-each-record-index-map-n-json-property-message)
  - [Recursive (JSON property: recursive)](#recursive-json-property-recursive)
  - [Rematerialize (JSON property: rematerialize)](#rematerialize-json-property-rematerialize)
  - [Scanned N databases (JSON property: message)](#scanned-n-databases-json-property-message)
  - [Select tables optimized away (JSON property: message)](#select-tables-optimized-away-json-property-message)
  - [Skip\_open\_table, Open\_frm\_only, Open\_full\_table (JSON property: message)](#skip_open_table-open_frm_only-open_full_table-json-property-message)
  - [Start temporary, End temporary (JSON property: message)](#start-temporary-end-temporary-json-property-message)
  - [unique row not found (JSON property: message)](#unique-row-not-found-json-property-message)
  - [Using filesort (JSON property: using\_filesort)](#using-filesort-json-property-using_filesort)
  - [Using index (JSON property: using\_index)](#using-index-json-property-using_index)
  - [Using index condition (JSON property: using\_index\_condition)](#using-index-condition-json-property-using_index_condition)
  - [Using index for group-by (JSON property: using\_index\_for\_group\_by)](#using-index-for-group-by-json-property-using_index_for_group_by)
  - [Using index for skip scan (JSON property: using\_index\_for\_skip\_scan)](#using-index-for-skip-scan-json-property-using_index_for_skip_scan)
  - [Using join buffer (Block Nested Loop), Using join buffer (Batched Key Access), Using join buffer (hash join) (JSON property: using\_join\_buffer)](#using-join-buffer-block-nested-loop-using-join-buffer-batched-key-access-using-join-buffer-hash-join-json-property-using_join_buffer)
  - [Using MRR (JSON property: message)](#using-mrr-json-property-message)
  - [Using sort\_union(...), Using union(...), Using intersect(...) (JSON property: message)](#using-sort_union-using-union-using-intersect-json-property-message)
  - [Using temporary (JSON property: using\_temporary\_table)](#using-temporary-json-property-using_temporary_table)
  - [Using where (JSON property: attached\_condition)](#using-where-json-property-attached_condition)
  - [Using where with pushed condition (JSON property: message)](#using-where-with-pushed-condition-json-property-message)
  - [Zero limit (JSON property: message)](#zero-limit-json-property-message)

# EXPLAIN Extra Information

The Extra column of EXPLAIN output contains additional information about how MySQL resolves the query. The following list explains the values that can appear in this column. Each item also indicates for JSON-formatted output which property displays the Extra value. For some of these, there is a specific property. The others display as the text of the message property.

If you want to make your queries as fast as possible, look out for Extra column values of Using filesort and Using temporary, or, in JSON-formatted EXPLAIN output, for using_filesort and using_temporary_table properties equal to true.

## Backward index scan (JSON: backward_index_scan)

The optimizer is able to use a descending index on an InnoDB table. Shown together with Using index. For more information, see Section 8.3.13, “Descending Indexes”.

## Child of 'table' pushed join@1 (JSON: message text)

This table is referenced as the child of table in a join that can be pushed down to the NDB kernel. Applies only in NDB Cluster, when pushed-down joins are enabled. See the description of the ndb_join_pushdown server system variable for more information and examples.

## const row not found (JSON property: const_row_not_found)

For a query such as SELECT ... FROM tbl_name, the table was empty.

## Deleting all rows (JSON property: message)

For DELETE, some storage engines (such as MyISAM) support a handler method that removes all table rows in a simple and fast way. This Extra value is displayed if the engine uses this optimization.

## Distinct (JSON property: distinct)

MySQL is looking for distinct values, so it stops searching for more rows for the current row combination after it has found the first matching row.

## FirstMatch(tbl_name) (JSON property: first_match)

The semijoin FirstMatch join shortcutting strategy is used for tbl_name.

## Full scan on NULL key (JSON property: message)

This occurs for subquery optimization as a fallback strategy when the optimizer cannot use an index-lookup access method.

## Impossible HAVING (JSON property: message)

The HAVING clause is always false and cannot select any rows.

## Impossible WHERE (JSON property: message)

The WHERE clause is always false and cannot select any rows.

## Impossible WHERE noticed after reading const tables (JSON property: message)

MySQL has read all const (and system) tables and notice that the WHERE clause is always false.

## LooseScan(m..n) (JSON property: message)

The semijoin LooseScan strategy is used. m and n are key part numbers.

## No matching min/max row (JSON property: message)

No row satisfies the condition for a query such as SELECT MIN(...) FROM ... WHERE condition.

## no matching row in const table (JSON property: message)

For a query with a join, there was an empty table or a table with no rows satisfying a unique index condition.

## No matching rows after partition pruning (JSON property: message)

For DELETE or UPDATE, the optimizer found nothing to delete or update after partition pruning. It is similar in meaning to Impossible WHERE for SELECT statements.

## No tables used (JSON property: message)

The query has no FROM clause, or has a FROM DUAL clause.

For INSERT or REPLACE statements, EXPLAIN displays this value when there is no SELECT part. For example, it appears for EXPLAIN INSERT INTO t VALUES(10) because that is equivalent to EXPLAIN INSERT INTO t SELECT 10 FROM DUAL.

## Not exists (JSON property: message)

MySQL was able to do a LEFT JOIN optimization on the query and does not examine more rows in this table for the previous row combination after it finds one row that matches the LEFT JOIN criteria. Here is an example of the type of query that can be optimized this way:
```sql
SELECT * FROM t1 LEFT JOIN t2 ON t1.id=t2.id
WHERE t2.id IS NULL;
```
Assume that t2.id is defined as NOT NULL. In this case, MySQL scans t1 and looks up the rows in t2 using the values of t1.id. If MySQL finds a matching row in t2, it knows that t2.id can never be NULL, and does not scan through the rest of the rows in t2 that have the same id value. In other words, for each row in t1, MySQL needs to do only a single lookup in t2, regardless of how many rows actually match in t2.

In MySQL 8.0.17 and later, this can also indicate that a WHERE condition of the form NOT IN (subquery) or NOT EXISTS (subquery) has been transformed internally into an antijoin. This removes the subquery and brings its tables into the plan for the topmost query, providing improved cost planning. By merging semijoins and antijoins, the optimizer can reorder tables in the execution plan more freely, in some cases resulting in a faster plan.

You can see when an antijoin transformation is performed for a given query by checking the Message column from SHOW WARNINGS following execution of EXPLAIN, or in the output of EXPLAIN FORMAT=TREE.
```
Note

An antijoin is the complement of a semijoin table_a JOIN table_b ON condition. The antijoin returns all rows from table_a for which there is no row in table_b which matches condition.
```
## Plan isn't ready yet (JSON property: none)

This value occurs with EXPLAIN FOR CONNECTION when the optimizer has not finished creating the execution plan for the statement executing in the named connection. If execution plan output comprises multiple lines, any or all of them could have this Extra value, depending on the progress of the optimizer in determining the full execution plan.

## Range checked for each record (index map: N) (JSON property: message)

MySQL found no good index to use, but found that some of indexes might be used after column values from preceding tables are known. For each row combination in the preceding tables, MySQL checks whether it is possible to use a range or index_merge access method to retrieve rows. This is not very fast, but is faster than performing a join with no index at all. The applicability criteria are as described in Section 8.2.1.2, “Range Optimization”, and Section 8.2.1.3, “Index Merge Optimization”, with the exception that all column values for the preceding table are known and considered to be constants.

Indexes are numbered beginning with 1, in the same order as shown by SHOW INDEX for the table. The index map value N is a bitmask value that indicates which indexes are candidates. For example, a value of 0x19 (binary 11001) means that indexes 1, 4, and 5 are considered.

## Recursive (JSON property: recursive)

This indicates that the row applies to the recursive SELECT part of a recursive common table expression. See Section 13.2.20, “WITH (Common Table Expressions)”.

## Rematerialize (JSON property: rematerialize)

Rematerialize (X,...) is displayed in the EXPLAIN row for table T, where X is any lateral derived table whose rematerialization is triggered when a new row of T is read. For example:

SELECT
...
FROM
t,
LATERAL (derived table that refers to t) AS dt
...

The content of the derived table is rematerialized to bring it up to date each time a new row of t is processed by the top query.

## Scanned N databases (JSON property: message)

This indicates how many directory scans the server performs when processing a query for INFORMATION_SCHEMA tables, as described in Section 8.2.3, “Optimizing INFORMATION_SCHEMA Queries”. The value of N can be 0, 1, or all.

## Select tables optimized away (JSON property: message)

The optimizer determined 1) that at most one row should be returned, and 2) that to produce this row, a deterministic set of rows must be read. When the rows to be read can be read during the optimization phase (for example, by reading index rows), there is no need to read any tables during query execution.

The first condition is fulfilled when the query is implicitly grouped (contains an aggregate function but no GROUP BY clause). The second condition is fulfilled when one row lookup is performed per index used. The number of indexes read determines the number of rows to read.

Consider the following implicitly grouped query:
```sql
SELECT MIN(c1), MIN(c2) FROM t1;
```
Suppose that MIN(c1) can be retrieved by reading one index row and MIN(c2) can be retrieved by reading one row from a different index. That is, for each column c1 and c2, there exists an index where the column is the first column of the index. In this case, one row is returned, produced by reading two deterministic rows.

This Extra value does not occur if the rows to read are not deterministic. Consider this query:
```sql
SELECT MIN(c2) FROM t1 WHERE c1 <= 10;
```
Suppose that (c1, c2) is a covering index. Using this index, all rows with c1 <= 10 must be scanned to find the minimum c2 value. By contrast, consider this query:
```sql
SELECT MIN(c2) FROM t1 WHERE c1 = 10;
```
In this case, the first index row with c1 = 10 contains the minimum c2 value. Only one row must be read to produce the returned row.

For storage engines that maintain an exact row count per table (such as MyISAM, but not InnoDB), this Extra value can occur for COUNT(*) queries for which the WHERE clause is missing or always true and there is no GROUP BY clause. (This is an instance of an implicitly grouped query where the storage engine influences whether a deterministic number of rows can be read.)

## Skip_open_table, Open_frm_only, Open_full_table (JSON property: message)

These values indicate file-opening optimizations that apply to queries for INFORMATION_SCHEMA tables.

- Skip_open_table: Table files do not need to be opened. The information is already available from the data dictionary.

- Open_frm_only: Only the data dictionary need be read for table information.

- Open_full_table: Unoptimized information lookup. Table information must be read from the data dictionary and by reading table files. 

## Start temporary, End temporary (JSON property: message)

This indicates temporary table use for the semijoin Duplicate Weedout strategy.

## unique row not found (JSON property: message)

For a query such as SELECT ... FROM tbl_name, no rows satisfy the condition for a UNIQUE index or PRIMARY KEY on the table.

## Using filesort (JSON property: using_filesort)

MySQL must do an extra pass to find out how to retrieve the rows in sorted order. The sort is done by going through all rows according to the join type and storing the sort key and pointer to the row for all rows that match the WHERE clause. The keys then are sorted and the rows are retrieved in sorted order. See Section 8.2.1.16, “ORDER BY Optimization”.

## Using index (JSON property: using_index)

The column information is retrieved from the table using only information in the index tree without having to do an additional seek to read the actual row. This strategy can be used when the query uses only columns that are part of a single index.

For InnoDB tables that have a user-defined clustered index, that index can be used even when Using index is absent from the Extra column. This is the case if type is index and key is PRIMARY.

Information about any covering indexes used is shown for EXPLAIN FORMAT=TRADITIONAL and EXPLAIN FORMAT=JSON. Beginning with MySQL 8.0.27, it is also shown for EXPLAIN FORMAT=TREE.

## Using index condition (JSON property: using_index_condition)

Tables are read by accessing index tuples and testing them first to determine whether to read full table rows. In this way, index information is used to defer (“push down”) reading full table rows unless it is necessary. See Section 8.2.1.6, “Index Condition Pushdown Optimization”.

## Using index for group-by (JSON property: using_index_for_group_by)

Similar to the Using index table access method, Using index for group-by indicates that MySQL found an index that can be used to retrieve all columns of a GROUP BY or DISTINCT query without any extra disk access to the actual table. Additionally, the index is used in the most efficient way so that for each group, only a few index entries are read. For details, see Section 8.2.1.17, “GROUP BY Optimization”.

## Using index for skip scan (JSON property: using_index_for_skip_scan)

Indicates that the Skip Scan access method is used. See Skip Scan Range Access Method.

## Using join buffer (Block Nested Loop), Using join buffer (Batched Key Access), Using join buffer (hash join) (JSON property: using_join_buffer)

Tables from earlier joins are read in portions into the join buffer, and then their rows are used from the buffer to perform the join with the current table. (Block Nested Loop) indicates use of the Block Nested-Loop algorithm, (Batched Key Access) indicates use of the Batched Key Access algorithm, and (hash join) indicates use of a hash join. That is, the keys from the table on the preceding line of the EXPLAIN output are buffered, and the matching rows are fetched in batches from the table represented by the line in which Using join buffer appears.

In JSON-formatted output, the value of using_join_buffer is always one of Block Nested Loop, Batched Key Access, or hash join.

Hash joins are available beginning with MySQL 8.0.18; the Block Nested-Loop algorithm is not used in MySQL 8.0.20 or later MySQL releases. For more information about these optimizations, see Section 8.2.1.4, “Hash Join Optimization”, and Block Nested-Loop Join Algorithm.

See Batched Key Access Joins, for information about the Batched Key Access algorithm.

## Using MRR (JSON property: message)

Tables are read using the Multi-Range Read optimization strategy. See Section 8.2.1.11, “Multi-Range Read Optimization”.

## Using sort_union(...), Using union(...), Using intersect(...) (JSON property: message)

These indicate the particular algorithm showing how index scans are merged for the index_merge join type. See Section 8.2.1.3, “Index Merge Optimization”.

## Using temporary (JSON property: using_temporary_table)

To resolve the query, MySQL needs to create a temporary table to hold the result. This typically happens if the query contains GROUP BY and ORDER BY clauses that list columns differently.

## Using where (JSON property: attached_condition)

A WHERE clause is used to restrict which rows to match against the next table or send to the client. Unless you specifically intend to fetch or examine all rows from the table, you may have something wrong in your query if the Extra value is not Using where and the table join type is ALL or index.

Using where has no direct counterpart in JSON-formatted output; the attached_condition property contains any WHERE condition used.

## Using where with pushed condition (JSON property: message)

This item applies to NDB tables only. It means that NDB Cluster is using the Condition Pushdown optimization to improve the efficiency of a direct comparison between a nonindexed column and a constant. In such cases, the condition is “pushed down” to the cluster's data nodes and is evaluated on all data nodes simultaneously. This eliminates the need to send nonmatching rows over the network, and can speed up such queries by a factor of 5 to 10 times over cases where Condition Pushdown could be but is not used. For more information, see Section 8.2.1.5, “Engine Condition Pushdown Optimization”.

## Zero limit (JSON property: message)

The query had a LIMIT 0 clause and cannot select any rows. 

