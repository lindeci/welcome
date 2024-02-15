
import gdb

class MysqlCommand(gdb.Command):
    def __init__(self):
        super(MysqlCommand, self).__init__("mysql", gdb.COMMAND_USER, prefix=True)

class BlockDisplay(gdb.Command):   # 继承gdb.Command
    def __init__(self):
        super(BlockDisplay, self).__init__("mysql block", gdb.COMMAND_USER)   # gdb.COMMAND_USER是GDB命令类型的一种，表示这个命令是用户自定义的命令
        self.printed_expression = {}
        self.printed_block = {}
        
    def invoke(self, arg, from_tty):
        if not arg:
            print("usage: mysql block [block]")
            return
        expr = gdb.parse_and_eval(arg)
        self.print_block(expr)
        
    def print_block(self, expr):
        self.printed_block[str(expr)] = True
        print(f"printed_block:{self.printed_block}")
        print(f"block       :{expr}\n"
            f"master      :{expr.dereference()['master']}\n"
            f"slave       :{expr.dereference()['slave']}\n"
            f"next        :{expr.dereference()['next']}\n"
            f"link_prev   :{expr.dereference()['link_prev'].dereference()}\n"
            f"link_nex    :{expr.dereference()['link_next']}")
        table = expr['m_table_list']['first']
        i = 0
        print("m_table_list:", end="");
        while True:
            print(table['table_name'].string(), end="")
            table = table['next_local']
            i = i + 1
            if (i >= expr['m_table_list']['elements']):
                break
            print(",", end="")
        print("")
        #dynamic_type = expr.dereference()['m_where_cond'].dynamic_type
        #print(expr.dereference()['m_where_cond'].cast(dynamic_type).dereference())
        if (expr.dereference()['master'] != 0x0):
            if (str(expr.dereference()['master']) not in self.printed_expression):
                self.print_expression(expr.dereference()['master'])
                
        if (expr.dereference()['slave'] != 0x0):
            if (str(expr.dereference()['slave']) not in self.printed_expression):
                self.print_expression(expr.dereference()['slave'])
                
        if (expr.dereference()['next'] != 0x0):
            if (str(expr.dereference()['next']) not in self.printed_block):
                self.print_block(expr.dereference()['next'])
                
        if (expr.dereference()['link_prev'] != 0x0 and expr.dereference()['link_prev'].dereference() != 0x0):
            if (str(expr.dereference()['link_prev'].dereference()) not in self.printed_block):
                self.print_block(expr.dereference()['link_prev'].dereference())
        #if (expr.dereference()['link_next'] != 0x0):
        #    if (expr.dereference()['link_next'] not in self.printed_block):
        #        self.print_block(expr.dereference()['link_next'])
        
    def print_expression(self, expr):
        self.printed_expression[str(expr)] = True
        print(f"printed_expression:{self.printed_expression}")
        print(f"expression  :{expr}\n"
            f"master      :{expr.dereference()['master']}\n"
            f"slave       :{expr.dereference()['slave']}\n"
            f"next        :{expr.dereference()['next']}\n"
            f"prev        :{expr.dereference()['prev']}")
        #print(expr.address, expr.dereference()['master'], expr.dereference()['slave'], expr.dereference()['next'], expr.dereference()['prev'])
   
MysqlCommand()
BlockDisplay()

"""
gdb.execute：这个函数可以执行一个GDB命令，并返回命令的输出。例如，gdb.execute("print i")会打印变量i的值。

gdb.selected_frame：这个函数返回当前选中的栈帧。你可以使用gdb.selected_frame().read_var("i")来读取当前栈帧中变量i的值。

gdb.selected_thread：这个函数返回当前选中的线程。

gdb.newest_frame和gdb.oldest_frame：这两个函数分别返回最新的栈帧和最旧的栈帧。

gdb.lookup_type：这个函数可以查找一个类型。例如，gdb.lookup_type("int")会返回int类型。

gdb.Breakpoint：这是一个类，你可以使用它来创建一个新的断点。例如，gdb.Breakpoint("main")会在main函数上创建一个断点。

-------------------

当然可以，以下是你提到的每个GDB Python API函数和类的简单介绍：

- `gdb.TYPE_CODE_PTR`：这是一个常量，表示指针类型的类型代码。

- `gdb.set_convenience_variables`：这个函数设置了一些方便的变量，这些变量可以在GDB表达式中使用。

- `gdb.Command('mysql', gdb.COMMAND_DATA, prefix=True)`：这行代码创建了一个新的GDB命令`mysql`，这个命令的类型是`gdb.COMMAND_DATA`，并且这个命令可以有前缀。

- `gdb.selected_thread()`：这个函数返回当前选中的线程。

- `gdb.execute('bt', False, True)`：这个函数执行一个GDB命令`bt`，并且这个命令的输出不会被显示出来，但是这个命令的结果会被返回。

- `gdb.error`：这是一个异常类，当GDB遇到错误时，会抛出这个异常。

- `gdb.lookup_global_symbol('Item_decimal::val_real()')`：这个函数查找一个全局符号`Item_decimal::val_real()`，并返回一个`gdb.Symbol`对象。

- `gdb.COMMAND_OBSCURE`：这是一个常量，表示一个命令的类型，这种类型的命令在`help`命令的输出中不会被列出。

- `gdb.parse_and_eval('end_of_list').address`：这行代码解析并执行一个表达式`end_of_list`，然后返回这个表达式的值的地址。

- `gdb.Value(alias).string()`：这行代码创建了一个新的`gdb.Value`对象，然后返回这个对象的字符串表示。

- `gdb.current_objfile()`：这个函数返回当前的目标文件。

- `gdb.printing.RegexpCollectionPrettyPrinter("mysqld")`：这行代码创建了一个新的正则表达式集合漂亮打印机，这个打印机的名字是`mysqld`。
"""


"""
    如果你想创建一个名为block的命令，且这个命令是mysql命令的一个子命令，
    你需要首先创建一个名为mysql的命令，然后将block命令作为mysql命令的一个子命令。
    你可以通过将prefix=True传递给gdb.Command的构造函数来创建一个可以有子命令的命令
"""