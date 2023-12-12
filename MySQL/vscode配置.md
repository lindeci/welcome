
# tasks.json
```json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        /***
        {
            ""label"": ""lldb-ck-cmake"",
            ""type"": ""shell"",
            // 参数说明： CMAKE_BUILD_TYPE=Debug开启调试模式，没有这个参数则生成的二进制文件无法调试。
            // CMAKE_EXPORT_COMPILE_COMMANDS=YES,clangd插件用来在当前文件夹下生成索引跳转文件compile_commands.json的，如果增加或者减少代码行数这个参数必须加上，否则调试时断点会错位
            // -DENABLE_CCACHE=0 如果报相应错了就加上这个
            ""command"": ""cd ${workspaceFolder}/build; cmake ..  -DCMAKE_BUILD_TYPE=Debug  -DCMAKE_EXPORT_COMPILE_COMMANDS=YES"",
        },
        */
        // 修改文件后重新编译使用ninja即可，不需要重新cmake，可以将上面的task注释掉
        {
            "type": "shell",
            "label": "lldb-mysqld",
            /***
            ""dependsOn": "lldb-ck-cmake",//如果上面cmake的task被注释了，该段也注释一下
            */
            // -j N  表示并发执行的数量，一般配置自己系统的核心数即可，默认N=3
            // 如果要编译全部文件，则去除后面的clickhouse-server
            "command": "cd ${workspaceFolder}/build; make -j 32 -frtti mysqld"
        },
    ]
}
```
# lauch.json
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "miDebuggerPath": "/usr/bin/gdb",
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/build/runtime_output_directory/mysqld-debug",
            "args": [
                "--user=mysql",
                "--datadir=${workspaceFolder}/build/runtime_output_directory/../../data",
                "--socket=${workspaceFolder}/build/runtime_output_directory/../../data/mysql.sock.lock"
            ],
            "stopAtEntry": false,
            "cwd": "${fileDirname}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "set print pretty on",
                    "ignoreFailures": false
                }/*,
                {
                    "description": "Set Disassembly Flavor to Intel",
                    "text": "-gdb-set disassembly-flavor intel",
                    "ignoreFailures": true
                },
                {
                    "description": "Enable RTTI for gdb",
                    "text": "-rtti",
                    "ignoreFailures": true
                }*/
            ]
    }
    ]
}
```