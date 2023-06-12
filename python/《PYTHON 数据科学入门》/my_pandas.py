'''
Pandas是一个用于数据操作和分析的Python库。它提供了灵活高效的数据结构，如DataFrame和Series，可以轻松处理和处理结构化数据。
'''
import pandas as pd

# 1. 创建一个空的DataFrame
df = pd.DataFrame()

# 2. 从列表创建DataFrame
data = [['Alice', 25], ['Bob', 30], ['Charlie', 35]]
df = pd.DataFrame(data, columns=['Name', 'Age'])

# 3. 从字典创建DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data)

# 4. 从CSV文件读取数据
df = pd.read_csv('python/data.csv')

# 5. 查看DataFrame的前几行
df.head()

# 6. 查看DataFrame的后几行
df.tail()

# 7. 查看DataFrame的统计信息
df.describe()

# 8. 列选择
df['Name']

# 9. 行选择
df.loc[0]

# 10. 条件筛选
df[df['Age'] > 30]

# 11. 添加新列
df['Gender'] = ['Female', 'Male', 'Male']

# 12. 删除列
# df.drop('Gender', axis=1, inplace=True)

# 13. 重命名列
df.rename(columns={'Name': 'Full Name'}, inplace=True)

# 14. 数据排序
df.sort_values('Age', ascending=False)

# 15. 缺失值处理
df.dropna()

# 16. 填充缺失值
df.fillna(0)

# 17. 数据分组
# df.groupby('Gender').mean()

# 18. 数据合并
df1 = pd.DataFrame({'A': ['A0', 'A1'], 'B': ['B0', 'B1']})
df2 = pd.DataFrame({'A': ['A2', 'A3'], 'B': ['B2', 'B3']})
pd.concat([df1, df2])

# 19. 数据透视表
# df.pivot_table(index='Name', columns='Age', values='Salary')

# 20. 数据保存到CSV文件
df.to_csv('python/output.csv', index=False)
