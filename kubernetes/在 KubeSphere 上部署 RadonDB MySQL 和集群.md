# 安装 cert-manager 创建
官网： https://cert-manager.io/docs/installation/

cert-manager（https://cert-manager.io/）是 Kubernetes 原生的证书管理控制器。它可以帮助从各种来源颁发证书，例如 Let's Encrypt，HashiCorp Vault，Venafi，简单的签名密钥对或自签名。它将确保证书有效并且是最新的，并在证书到期前尝试在配置的时间续订证书。它大致基于 kube-lego 的原理，并从其他类似项目（例如 kube-cert-manager）中借鉴了一些智慧。

```sh
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.4/cert-manager.yaml
```