访问http://www.163.com为例，看下是DNS会进行哪些操作：  

主机名.次级域名.顶级域名.根域名

www.baidu.com.root

1. 首先查找电脑上的DNS缓存列表，如果有记录，那么直接返回对于IP地址，否则进行下一步；
2. 查找电脑上的HOST文件的映射关系，如果有记录，那么返回对于IP地址，否则进行下一步；
3. 查找互联网线路供应商的本地DNS服务器（即中国电信、中国移动或中国联通），本地DNS服务器先查找自己的缓存记录，如果有记录，那么返回对应IP地址，否则本地DNS服务器向根域名服务器发生请求；
4. 根域名服务器收到请求后，查看是.com顶级域名，于是返回.com顶级域名服务器的IP地址给到本地DNS服务器；
5. 本地DNS服务器收到回复后，向.com顶级域名服务器发起请求；
6. .com顶级域名服务器收到请求后，查看是.http://baidu.com次级域名，于是返回.http://baidu.com次级域名服务器的IP地址给到DNS服务器；
7. 本地DNS服务器收到回复后，向.http://baidu.com次级域名服务器发起请求；
8. .http://baidu.com次级域名服务器收到请求后，查看是自己管理的域名，于是查看域名和IP地址映射表，把http://www.baidu.com的IP地址返回给本地DNS服务器；
9. 本地DNS服务器收到回复后，向电脑回复域名对应IP地址，并把记录写入本地DNS服务器的缓存里；
10. 电脑收到回复后，使用IP地址访问网站，并把记录写入电脑DNS缓存中。

![](https://pic3.zhimg.com/v2-baaa52c463ce10522735c49a3239399a_b.jpg)