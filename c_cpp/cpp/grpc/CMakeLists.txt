# 设置 CMake 的最低版本
cmake_minimum_required(VERSION 3.8)

# 设置项目名称和编译器名称
project(write_personal_details C CXX)

# 包含 common.cmake 中的内容
include(cmake/common.cmake)

# 获取 helloworld.proto 文件的路径和名称
get_filename_component(hw_proto "addressbook.proto" ABSOLUTE)
get_filename_component(hw_proto_path "${hw_proto}" PATH)

# 生成源文件的路径和名称
set(hw_proto_srcs "${CMAKE_CURRENT_BINARY_DIR}/addressbook.pb.cc")
set(hw_proto_hdrs "${CMAKE_CURRENT_BINARY_DIR}/addressbook.pb.h")

# 使用 protoc 编译器生成 helloworld.proto 的 C++ 代码
add_custom_command(
  # 生成的文件
  OUTPUT "${hw_proto_srcs}" "${hw_proto_hdrs}"
  # 调用 protoc 命令。  在 add_custom_command 命令中，COMMAND 表示要执行的命令。
  COMMAND ${_PROTOBUF_PROTOC}
  # 参数
  ARGS # --grpc_out "${CMAKE_CURRENT_BINARY_DIR}"
    --cpp_out "${CMAKE_CURRENT_BINARY_DIR}"
    -I "${hw_proto_path}"
    --plugin=protoc-gen-grpc="${_GRPC_CPP_PLUGIN_EXECUTABLE}"   # _GRPC_CPP_PLUGIN_EXECUTABLE 是一个变量，表示用于生成 gRPC C++ 代码的 protoc 插件的可执行文件路径。在这个 CMakeLists.txt 文件中，这个变量的值是在调用 find_program() 函数时查找到的。在默认情况下，这个变量应该是 protoc-gen-grpc（如果已经在系统路径中），它是一个 protoc 插件，能够将 .proto 文件编译成用于生成 gRPC 代码的 C++ 代码。
    "${hw_proto}"
  # 依赖项
  DEPENDS "${hw_proto}"
)

# 将生成的 *.pb.h 文件包含在项目中
include_directories("${CMAKE_CURRENT_BINARY_DIR}")

# 使用 add_library() 函数，将编译生成的 C++ 代码作为源文件，生成静态库 hw_grpc_proto。
add_library(hw_grpc_proto
  ${hw_proto_srcs}
  ${hw_proto_hdrs}
)

# 将 hw_grpc_proto 静态库与 gRPC 和 Protobuf 库进行链接
# target_link_libraries() 函数本身并不会生成新的文件。它只是指示 CMake 将一个目标与其他库文件链接在一起，以便在最终生成的可执行文件或库文件中包含所需的符号和函数。
target_link_libraries(hw_grpc_proto
  ${_REFLECTION}    # ${_REFLECTION} 变量是一个 gRPC 提供的预定义变量，它表示 gRPC C++ 库中的反射代码
  ${_GRPC_GRPCPP}   # ${_GRPC_GRPCPP} 变量表示 gRPC C++ 库本身
  ${_PROTOBUF_LIBPROTOBUF}    # ${_PROTOBUF_LIBPROTOBUF} 变量表示 Protobuf 库。 这些变量都是在 CMake 文件中通过 find_package() 命令查找的。
)

# 创建可执行文件
foreach(_target
    write_personal_details
    read_personal_details)
  # 添加可执行文件
  add_executable(${_target} "${_target}.cc")
  # 链接库文件
  target_link_libraries(${_target}    # target_link_libraries() 函数用于将一个或多个库文件链接到指定的可执行文件或库文件中，以便在链接阶段将所需的函数和符号加入可执行文件或库文件中
    hw_grpc_proto   # 静态库，已在前面的代码段中定义
    absl::flags   # absl::flags 和 absl::flags_parse：这两个库文件来自于 Google 开源的库 Abseil，它们提供了命令行选项解析的功能。这两个库也需要被链接才能在程序中使用。
    absl::flags_parse
    ${_REFLECTION}
    ${_GRPC_GRPCPP}
    ${_PROTOBUF_LIBPROTOBUF}
  )
endforeach()