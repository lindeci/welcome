- [新人学习建议](#新人学习建议)
- [计算机架构](#计算机架构)
- [安装](#安装)
- [核心功能](#核心功能)
- [张量](#张量)

# 新人学习建议
There are many resources available online to learn PyTorch. Here are some of the best resources to get started:

1. PyTorch Tutorials: This is the official PyTorch documentation that provides a quickstart guide to familiarize yourself with PyTorch concepts and modules. You can learn how to load data, build deep neural networks, train and save your models .

2. Zero to Mastery Learn PyTorch for Deep Learning: This is a free online book that provides a comprehensive guide to learning PyTorch. It covers everything from the basics of tensors and automatic differentiation to advanced topics like convolutional neural networks and generative adversarial networks .

3. Deep Neural Networks with PyTorch: This is a course on Coursera that teaches you how to develop deep learning models using PyTorch. The course covers different models starting off with fundamentals such as Linear Regression, and logistic/softmax regression .

I hope that helps! Let me know if you have any other questions.

Source: Conversation with Bing, 2023/6/7
(1) Welcome to PyTorch Tutorials — PyTorch Tutorials 2.0.1+cu117 documentation. https://pytorch.org/tutorials/.
(2) Deep Learning with PyTorch. https://pytorch.org/tutorials/beginner/nlp/deep_learning_tutorial.html.
(3) Zero to Mastery Learn PyTorch for Deep Learning. https://www.learnpytorch.io/.
(4) Deep Neural Networks with PyTorch | Coursera. https://www.coursera.org/learn/deep-neural-networks-with-pytorch.
(5) Learn the Basics — PyTorch Tutorials 2.0.0+cu117 documentation. https://pytorch.org/tutorials/beginner/basics/intro.html.

# 计算机架构
以下是对于给定计算机架构的简要说明和版本号：

| 架构    | 说明                           | 版本号  |
|---------|--------------------------------|---------|
| CUDA    | CUDA是NVIDIA开发的并行计算平台  | 11.7    |
| CUDA    | CUDA是NVIDIA开发的并行计算平台  | 11.8    |
| ROCm    | ROCm是AMD开发的并行计算平台     | 5.4.2   |
| CPU     | CPU指中央处理器，是计算机的核心  | -       |

请注意，CUDA和ROCm是并行计算平台，主要用于利用GPU进行高性能计算和加速。CUDA是NVIDIA的平台，而ROCm是AMD的平台。它们提供了编程模型和工具，使开发者能够利用GPU进行并行计算任务。

另一方面，CPU是计算机的中央处理器，是计算机系统的主要计算和控制单元。CPU负责执行计算机程序中的指令，并协调和管理计算机的各种组件。CPU的性能和架构对计算机系统的整体性能具有重要影响。

# 安装
https://pytorch.org/get-started/locally/
```
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```
# 核心功能
PyTorch 的核心是提供两个主要功能：
- n 维张量，类似于 NumPy，但可以在 GPU 上运行 
- 用于构建和训练神经网络的自动微分

# 张量
张量是 n 维数组，PyTorch 提供了许多在这些张量上进行操作的函数。 在幕后，张量可以跟踪计算图和梯度，但它们也可用作科学计算的通用工具。

