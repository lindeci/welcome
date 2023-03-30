## fork子进程调试
默认情况下，父进程fork一个子进程，gdb只会继续调试父进程而不会管子进程的运行。
如果你想跟踪子进程进行调试，可以使用set follow-fork-mode mode来设置fork跟随模式。
set follow-fork-mode 所带的mode参数可以是以下的一种：
    parent
        gdb只跟踪父进程，不跟踪子进程，这是默认的模式。
    child
        gdb在子进程产生以后只跟踪子进程，放弃对父进程的跟踪。
    进入gdb以后，我们可以使用show follow-fork-mode来查看目前的跟踪模式。 

然而，有的时候，我们想同时调试父进程和子进程，以上的方法就不能满足了。Linux提供了set detach-on-fork mode命令来供我们使用。其使用的mode可以是以下的一种：
    on
        只调试父进程或子进程的其中一个(根据follow-fork-mode来决定)，这是默认的模式。
    off
        父子进程都在gdb的控制之下，其中一个进程正常调试(根据follow-fork-mode来决定)
    另一个进程会被设置为暂停状态。
    同样，show detach-on-fork显示了目前是的detach-on-fork模式