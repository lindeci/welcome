- [给用户添加sudo权限](#给用户添加sudo权限)
  - [不需要密码，不需要编辑文件的办法](#不需要密码不需要编辑文件的办法)
  - [需要编辑文件的办法](#需要编辑文件的办法)
- [yum 源的 centos-release-scl-rh 包](#yum-源的-centos-release-scl-rh-包)
- [cp 时不需要提示](#cp-时不需要提示)

# 给用户添加sudo权限
```
userdel -r ldc # 此时会连用户组一起删除，如果不想删除用户组，则 userdel ldc

groupadd ldc
useradd ldc -g ldc
```
## 不需要密码，不需要编辑文件的办法
```
echo "ldc ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers.d/ldc
```

## 需要编辑文件的办法
```
visudo

##
## Allow root to run any commands anywhere
root    ALL=(ALL)       ALL
evoc    ALL=(ALL)       NOPASSWD:ALL
ldc     ALL=(ALL)       NOPASSWD: ALL
```

# yum 源的 centos-release-scl-rh 包
发现本地 yum 源没有 这些 rpm 包 devtoolset-11-gcc devtoolset-11-gcc-c++ devtoolset-11-binutils

解决方案：  
centos-release-scl-rh 是一个 RPM 包，它为 CentOS 系统提供了 Software Collections (SCL) 的 yum 配置和基本文档。

安装
```
yum install centos-release-scl-rh
```
```
yum install devtoolset-11-gcc
```

# cp 时不需要提示
```cpp
\cp a b
```