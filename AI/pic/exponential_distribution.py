import numpy as np
import matplotlib.pyplot as plt

# 设置图表参数
fig, ax = plt.subplots()

# 生成指数分布数据
x = np.linspace(0, 5, 1000)
colors = ['blue', 'red', 'green']

for i in range(3):
    lambda_ = i + 1
    y = lambda_ * np.exp(-lambda_ * x)
    ax.plot(x, y, label=f'$\lambda$ = {lambda_}', color=colors[i])

# 设置 x 轴和 y 轴标签
ax.set_xlabel('Time (minutes)')
ax.set_ylabel('Probability density')

# 添加图例
ax.legend()

# 保存图表
plt.savefig('exponential_distribution.png')

