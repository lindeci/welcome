import Pyro4

# 获取服务器端的远程对象
server_uri = "PYRO:my_custom_id@127.0.0.1:8000"
server = Pyro4.Proxy(server_uri)

# 调用远程对象的方法
result = server.say_hello("John")

# 打印结果
print(result)
