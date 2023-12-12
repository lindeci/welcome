# Send_field
```cpp
class Send_field {
  public:
    const char *db_name; /**< 数据库名称 */
    const char *table_name; /**< 表名称 */
    const char *org_table_name; /**< 原始表名称 */
    const char *col_name; /**< 列名称 */
    const char *org_col_name; /**< 原始列名称 */
    ulong length; /**< 长度 */
    uint charsetnr; /**< 字符集编号 */
    uint flags; /**< 标志位 */
    uint decimals; /**< 小数位数 */
    enum_field_types type; /**< 字段类型枚举 */
    bool field; /**< 字段标志 */

    Send_field(void); /**< 构造函数 */
}
```