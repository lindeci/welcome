'''
问题：
让我们通过一个简单的线性回归问题来演示梯度下降的计算过程。假设我们有一组数据点 `(x, y)`，我们的目标是拟合一个线性模型 `y = mx + b`。

我们将使用平方误差损失函数来度量模型的预测值与真实值之间的差异，即损失函数为 `L = (y_pred - y)^2`。

现在，我们将使用梯度下降算法来找到最小化损失函数的参数 `m` 和 `b`。

假设我们的初始参数为 `m = 0` 和 `b = 0`，学习率（步长）为 `lr = 0.01`。

我们将迭代更新参数，直到达到停止条件（例如，达到最大迭代次数或损失函数的变化很小）。

1. 计算模型的预测值：
   ```
   y_pred = m * x + b
   ```

2. 计算损失函数：
   ```
   loss = (y_pred - y)^2
   ```

3. 计算参数 `m` 和 `b` 相对于损失函数的偏导数：
   ```
   d_m = 2 * (y_pred - y) * x
   d_b = 2 * (y_pred - y)
   ```

4. 更新参数 `m` 和 `b`：
   ```
   m = m - lr * d_m
   b = b - lr * d_b
   ```

5. 重复步骤 1-4 直到满足停止条件。

这是一个迭代的过程，我们通过不断调整参数的值来逐渐减小损失函数。每次迭代，参数根据梯度的方向和学习率进行更新。随着迭代的进行，我们期望损失函数逐渐减小，最终达到最优的参数值。

请注意，上述示例是一个简化的梯度下降计算过程，并且使用了单个数据点。在实际应用中，通常会使用多个数据点（批量梯度下降或小批量梯度下降）以及更复杂的模型和损失函数。
'''
import torch

# 输入数据
x = torch.tensor([1.0, 2.0, 3.0, 4.0])
y = torch.tensor([2.0, 4.0, 6.0, 8.0])

# 初始化参数
m = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)

# 学习率
lr = 0.01

# 迭代更新参数
for _ in range(10):
    # 计算模型的预测值
    y_pred = m * x + b
    
    # 计算损失函数
    loss = torch.mean((y_pred - y) ** 2)
    
    # 使用自动求导计算梯度
    loss.backward()
    print(loss)
    print(m.grad)
    print(b.grad)
    # 更新参数
    with torch.no_grad():
        m -= lr * m.grad
        b -= lr * b.grad
        print(m)
        print(b)
        
        # 清零梯度
        m.grad.zero_()
        b.grad.zero_()
        print(m.grad)
        print(b.grad)

# 输出最终的参数值
print("m:", m.item())
print("b:", b.item())