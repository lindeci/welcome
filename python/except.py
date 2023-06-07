try:
    # 可能引发异常的代码块
    file = open('file.txt', 'r')
    content = file.read()
    file.close()

    # 抛出异常
    if len(content) == 0:
        raise ValueError("文件内容为空")

    # 使用assert断言
    assert len(content) < 100, "文件内容过长"

except FileNotFoundError:
    print("文件未找到")

except ValueError as ve:
    print("值错误:", ve)

except AssertionError as ae:
    print("断言错误:", ae)

except Exception as e:
    print("发生了其他异常:", e)

else:
    # 没有发生任何异常时执行的代码块
    print("文件读取成功，内容为:", content)

finally:
    # 无论是否发生异常，都会执行的代码块
    print("异常处理结束")

# 使用with/as语句自动关闭文件
with open('another_file.txt', 'w') as another_file:
    another_file.write("写入文件的内容")