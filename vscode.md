
- [VSCode如何返回上一步](#vscode如何返回上一步)
- [大括号的折叠](#大括号的折叠)
  - [安装常见插件](#安装常见插件)

# VSCode如何返回上一步
在Windows中可以使用快捷键“Alt+←”实现  
在Linux中可以使用快捷键“Ctrl+Alt+ -”实现  
在Mac中可以使用快捷键“Ctrl + -”实现  

# 大括号的折叠
 Mac:Cmd + Option + 右方括号  
 Windows:Ctrl + Shift + 右方括号

## 安装常见插件
1. CMake
2. CMake Tools
3. Remote - SSH
4. C/C++ Themes
5. Chinese Language Pack for Visual Studio
6. C/C++ Extension pack
7. Markdown Editor
8. Markdown All in One
9. GDB Debugger - Beyond
10. C/C++
11. Code Runner
12. GitHub Copilot  //收费 $10/月
13. CodeGeeX
14. Makefile Tools
15. PDF Viewer


| 编号 | 插件名称                                       | 插件简介                                                     |
| ---- | ---------------------------------------------- | ------------------------------------------------------------ |
| 1    | CMake                                          | CMake 工程管理工具                                          |
| 2    | CMake Tools                                    | 为 CMake 提供更好的支持，包括自动补全、语法高亮、调试等功能 |
| 3    | Remote - SSH                                   | 支持通过 SSH 连接到远程主机进行开发和调试                   |
| 4    | C/C++ Themes                                   | 提供 C/C++ 语言的主题，美化代码界面                         |
| 5    | Chinese Language Pack for Visual Studio        | 提供中文语言包                                               |
| 6    | C/C++ Extension pack                           | 包括 C/C++ 开发所需的插件，如 IntelliSense、调试器、代码片段等 |
| 7    | Markdown Editor                                | Markdown 编辑器                                             |
| 8    | Markdown All in One                            | Markdown 编辑器增强，提供语法高亮、预览、TOC 生成等功能     |
| 9    | GDB Debugger - Beyond                          | 提供 GDB 调试器的增强功能，支持多线程调试等                 |
| 10   | C/C++                                         | 提供 C/C++ 开发所需的插件，如 IntelliSense、调试器、代码片段等 |
| 11   | Code Runner                                    | 可以直接在编辑器中运行代码                                   |
| 12   | GitHub Copilot                                 | 由 OpenAI 提供的 AI 代码助手，可以生成代码片段、自动补全等功能。收费 $10/月 |
| 13   | CodeGeeX                                       | 提供多种语言的代码片段和代码模板                             |
| 14   | Makefile Tools                                 | 提供 Makefile 的支持，可以自动构建项目                       |
| 15   | Graphviz Preview                               | dot文件的图形展示 


https://plantuml.com/zh/sequence-diagram
```sh
plantuml 的安装

apt install default-jdk
apt install graphviz graphviz-dev
# 本地渲染服务
docker run -d -p 8080:8080 plantuml/plantuml-server:jetty
# 然后在 /data/welcome/.vscode/settings.json 中配置
"plantuml.server": "http://容器的IP:8080",
"plantuml.render": "PlantUMLServer"
```