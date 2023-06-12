'''
一系列高效的、可并行的、执行高性能数值运算的函数的接口
'''
import numpy as np

# 1. 创建数组
print("1. 创建数组")
array1 = np.array([1, 2, 3, 4, 5])
array2 = np.zeros((3, 3))
array3 = np.ones((2, 2))
array4 = np.random.rand(4, 4)

# 2. 数组形状操作
print("2. 数组形状操作")
print(array1.shape)
print(array2.reshape((9,)))

# 3. 数组索引和切片
print("3. 数组索引和切片")
print(array1[2])
print(array2[1, 2])
print(array3[:, 1])

# 4. 数组运算
print("4. 数组运算")
# array5 = array1 + array2
# array6 = array1 * array3

# 5. 数组拼接
print("5. 数组拼接")
# array7 = np.concatenate((array1, array2), axis=0)
# array8 = np.vstack((array1, array3))

# 6. 数组转置
print("6. 数组转置")
array9 = array1.transpose()
array10 = array2.T

# 7. 数组统计函数
print("7. 数组统计函数")
print(np.mean(array1))
print(np.max(array2))
print(np.sum(array3))

# 8. 数组排序
print("8. 数组排序")
array11 = np.sort(array1)
array12 = np.argsort(array1)

# 9. 数组形状修改
print("9. 数组形状修改")
array13 = np.resize(array1, (2, 3))
array14 = np.ravel(array2)

# 10. 数组去重
print("10. 数组去重")
array15 = np.unique(array1)

# 11. 数组堆叠
print("11. 数组堆叠")
# array16 = np.stack((array1, array2))

# 12. 数组迭代
print("12. 数组迭代")
for item in array1:
    print(item)

# 13. 数组复制
print("3. 数组复制")
array17 = array1.copy()

# 14. 数组元素判断
print("14. 数组元素判断")
print(np.isin(array1, [1, 2, 3]))

# 15. 数组形状转换
print("15. 数组形状转换")
array18 = np.reshape(array1, (5, 1))

# 16. 数组形状反转
print("16. 数组形状反转")
array19 = np.flip(array1)

# 17. 数组填充
print("17. 数组填充")
array20 = np.pad(array1, (2, 3), mode='constant', constant_values=0)

# 输出结果
print(array1)
print(array2)
print(array3)
print(array4)
# print(array5)
# print(array6)
# print(array7)
# print(array8)
print(array9)
print(array10)
print(array11)
print(array12)
print(array13)
print(array14)
print(array15)
# print(array16)
print(array17)
print(array18)
print(array19)
print(array20)
