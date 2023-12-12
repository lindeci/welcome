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
5. **查看环境变量**
```sh
echo $PATH
/data/miniconda3/bin:/data/miniconda3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

cat ~/.bashrc
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/data/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/data/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/data/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/data/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```
其它：离线安装numpy
```
```