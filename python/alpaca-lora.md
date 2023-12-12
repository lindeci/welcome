# alpaca-lora 使用
https://github.com/tloen/alpaca-lora/tree/main

# 环境准备
GPU计算型GN7, 8核32GB, 硬盘150G
Ubuntu Server 20.04 LTS 64位

## 安装网卡驱动
https://developer.nvidia.com/cuda-12-1-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=20.04&target_type=runfile_local
```
wget https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_530.30.02_linux.run
sudo sh cuda_12.1.0_530.30.02_linux.run
```
设置环境变量
```
export LD_LIBRARY_PATH=/usr/local/cuda/lib64
PATH=$PATH:/usr/local/cuda-12.1/bin
```
## 源码安装 bitsandbytes
https://github.com/TimDettmers/bitsandbytes
```sh
git clone https://github.com/timdettmers/bitsandbytes.git
cd bitsandbytes

# CUDA_VERSIONS in {110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 120}
# make argument in {cuda110, cuda11x, cuda12x}
# if you do not know what CUDA you have, try looking at the output of: python -m bitsandbytes
CUDA_VERSION=121 make cuda12x
python setup.py install
```

## 运行推理
```
pip install torch
pip install scipy
pip install fire
pip intall gradio
pip install transformers
pip install peft
pip install sentencepiece

python generate.py \
    --load_8bit \
    --base_model 'decapoda-research/llama-7b-hf' \
    --lora_weights 'tloen/alpaca-lora-7b'
```

## 页面访问
http://0.0.0.0:7860