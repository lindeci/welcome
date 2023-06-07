# 安装
参考官方文档：https://conda.io/projects/conda/en/stable/user-guide/install/index.html#
```
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
bash Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
重新打开终端
conda --version
conda list
conda init fish
重新打开终端
```
# 使用
1. **创建新环境**  
   ```
   conda create --name myenv python=X.X
   ```
2. **激活环境**  
     ```
     conda activate myenv
     ```
3. **安装其他包**
   ```
   conda install numpy pandas
   或者指定版本
   conda install "numpy>=1.19.0,<1.20.0"

   查看安装包列表
   conda list
   如果一些包无法通过conda安装，可以尝试使用pip安装：
   pip install python-etcd

   ```
4. **切换环境**
   ```
   conda deactivate
   ```
   然后，使用激活命令切换到另一个环境。
   ```
   conda activate anotherenv
   ```
其它：离线安装numpy
```
```