import Pyro4

@Pyro4.expose  # 暴露对象给远程调用
class MyServer(object):
    def __init__(self):
        self.name = "MyServer"
    def say_hello(self, name):
        return "Hello, {}! This func is {}.".format(name, self.name)

# 创建Pyro4的Daemon对象
daemon = Pyro4.Daemon(host="127.0.0.1", port=8000)

# 将远程对象注册到Pyro4的命名服务器中
obj_id = "my_custom_id"
uri = daemon.register(MyServer, obj_id)

# 打印远程对象的URI，客户端需要使用该URI进行访问
print("Server URI:", uri)

# 启动服务器，等待客户端调用
daemon.requestLoop()
