# 官方文档
ChatGLM2-6B 的部署与微调教程

https://www.heywhale.com/mw/project/64984a7b72ebe240516ae79c

# 快速部署
## 在上海5区申请竞价类型的GPU
## 恢复conda环境
```sh
lsblk
mount /dev/vdb /data
sudo su
vi ~/.bashrc

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
## 



# 安装依赖
```sh
pip install rouge_chinese nltk jieba datasets transformers[torch] -i https://pypi.douban.com/simple/
```

# 训练
```sh
torchrun --standalone \
    --nnodes=1 \
    --nproc-per-node=1 \
    main.py \
    --do_train \
    --train_file AdvertiseGen/train.json \
    --validation_file AdvertiseGen/dev.json \
    --preprocessing_num_workers 10 \
    --prompt_column content \
    --response_column summary \
    --overwrite_cache \
    --model_name_or_path /data/chatglm2-6b \
    --output_dir output/adgen-chatglm2-6b-pt-$PRE_SEQ_LEN-$LR \
    --overwrite_output_dir \
    --max_source_length 64 \
    --max_target_length 128 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 16 \
    --predict_with_generate \
    --max_steps 3000 \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 2e-2 \
    --pre_seq_len 128 \
    --quantization_bit 4

# 参数介绍
torchrun --standalone \  # 使用独立模式（非分布式）
    --nnodes=1 \  # 节点数量（此处为1个节点）
    --nproc-per-node=1 \  # 每个节点的进程数（每个节点有1个进程）
    main.py \  # 主要运行的Python脚本
    --do_train \  # 设置为进行训练模式
    --train_file AdvertiseGen/train.json \  # 训练数据文件的路径（JSON格式）
    --validation_file AdvertiseGen/dev.json \  # 验证数据文件的路径（JSON格式）
    --preprocessing_num_workers 10 \  # 数据预处理的工作进程数
    --prompt_column content \  # 指定输入数据（train.json和dev.json）中包含提示的列名，模型将根据这些提示生成响应。
    --response_column summary \  # 指定输入数据中包含与`--prompt_column`中的提示相对应的参考响应或目标摘要的列名。
    --overwrite_cache \  # 如果存在缓存数据，则覆盖现有缓存
    --model_name_or_path /data/chatglm2-6b \  # 预训练模型的名称或路径
    --output_dir output/adgen-chatglm2-6b-pt-$PRE_SEQ_LEN-$LR \  # 输出目录，保存训练模型和日志文件
    --overwrite_output_dir \  # 如果输出目录已存在，则覆盖现有目录
    --max_source_length 64 \  # 输入序列的最大长度限制
    --max_target_length 128 \  # 目标序列（生成响应）的最大长度限制
    --per_device_train_batch_size 1 \  # 每个设备的训练批量大小
    --per_device_eval_batch_size 1 \  # 每个设备的评估批量大小
    --gradient_accumulation_steps 16 \  # 梯度累积的步数
    --predict_with_generate \  # 在评估期间生成预测结果
    --max_steps 3000 \  # 训练的最大步数
    --logging_steps 10 \  # 记录日志的步数间隔
    --save_steps 1000 \  # 保存模型的步数间隔
    --learning_rate 2e-2 \  # 初始学习率
    --pre_seq_len 128 \  # 预先设定的序列长度
    --quantization_bit 4 \  # 每个量化参数的比特数
```

# 加速
在默认配置 quantization_bit=4、per_device_train_batch_size=1、gradient_accumulation_steps=16 下，INT4 的模型参数被冻结，一次训练迭代会以 1 的批处理大小进行 16 次累加的前后向传播，等效为 16 的总批处理大小，此时最低只需 6.7G 显存。若想在同等批处理大小下提升训练效率，可在二者乘积不变的情况下，加大 per_device_train_batch_size 的值，但也会带来更多的显存消耗，请根据实际情况酌情调整。