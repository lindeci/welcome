# -*- coding: utf-8 -*-

import contextvars
import threading

# 创建上下文变量
name = contextvars.ContextVar('name', default='Guest')

def greet():
    # 获取当前上下文中的name变量的值
    current_name = name.get()
    print(f"Hello, {current_name}!")

def change_name(new_name):
    # 设置新的name变量的值
    name.set(new_name)
    greet()

def worker():
    # 在新的线程中执行change_name函数
    change_name('Alice')

# 在默认上下文中执行greet函数
greet()  # 输出: Hello, Guest!

# 创建并启动新线程
thread = threading.Thread(target=worker)
thread.start()
thread.join()

# 再次在默认上下文中执行greet函数
greet()  # 输出: Hello, Guest!


'''
在上述示例中，我们创建了一个name的上下文变量，定义了greet()和change_name()函数，这些与之前的示例相同。然而，我们现在引入了一个新的线程worker()，其中调用了change_name()函数。这样，我们就在不同的线程中切换了上下文。

在主线程中，我们先调用了greet()函数，它在默认上下文中执行，并输出Hello, Guest!。然后，我们创建了一个新的线程，并启动它，其中新的线程会执行worker()函数。在worker()函数中，我们调用了change_name('Alice')来修改上下文中的name变量。接着，我们在该线程中调用greet()函数，输出Hello, Alice!。最后，我们再次在主线程中调用greet()函数，它会恢复默认上下文，并输出Hello, Guest!。

这个示例演示了在多线程环境中使用contextvars的上下文切换和隔离性。每个线程都有自己的上下文，可以在其中设置和获取不同的变量值，而不会相互干扰。这种隔离性和自动的上下文切换使得在并发编程中传递和管理上下文相关的数据变得更加可靠和方便。
'''