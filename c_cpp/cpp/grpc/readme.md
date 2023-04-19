- [官网学习](#官网学习)
  - [安装步骤](#安装步骤)
  - [Service definition](#service-definition)
  - [Unary RPC](#unary-rpc)
  - [Server streaming RPC](#server-streaming-rpc)
  - [Client streaming RPC](#client-streaming-rpc)
  - [Bidirectional streaming RPC](#bidirectional-streaming-rpc)
  - [Deadlines/Timeouts](#deadlinestimeouts)
  - [RPC termination](#rpc-termination)
  - [Cancelling an RPC](#cancelling-an-rpc)
  - [Metadata](#metadata)
  - [Channels](#channels)
  - [Protocol Buffers](#protocol-buffers)
  - [Generating Your Classes](#generating-your-classes)
- [本例子的编译、运行](#本例子的编译运行)

# 官网学习
[quickstart](https://grpc.io/docs/languages/cpp/quickstart/)

## 安装步骤
```shell
export MY_INSTALL_DIR=/data/.local
mkdir -p $MY_INSTALL_DIR
export PATH="$MY_INSTALL_DIR/bin:$PATH"

apt install -y cmake
apt install -y build-essential autoconf libtool pkg-config
git clone --recurse-submodules -b v1.54.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
cd grpc
mkdir -p cmake/build
pushd cmake/build

cmake -DgRPC_INSTALL=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DCMAKE_INSTALL_PREFIX=$MY_INSTALL_DIR \
      ../..

make -j 4
make install
popd
```

## Service definition  
Interface Definition Language (IDL) 

## Unary RPC

## Server streaming RPC
After sending all its messages, the server’s status details (status code and optional status message) and optional trailing metadata are sent to the client. 
## Client streaming RPC
The server responds with a single message (along with its status details and optional trailing metadata), typically but not necessarily after it has received all the client’s messages.

## Bidirectional streaming RPC

## Deadlines/Timeouts   

## RPC termination  

## Cancelling an RPC
Warning:  
Changes made before a cancellation are not rolled back.
## Metadata
## Channels
A gRPC channel provides a connection to a gRPC server on a specified host and port. 

## Protocol Buffers 
Protocol buffers provide a language-neutral, platform-neutral, extensible mechanism for serializing structured data in a forward-compatible and backward-compatible way. It’s like JSON, except it’s smaller and faster, and it generates native language bindings. You define how you want your data to be structured once, then you can use special generated source code to easily write and read your structured data to and from a variety of data streams and using a variety of languages.

Protocol buffers are a combination of the definition language (created in .proto files), the code that the proto compiler generates to interface with data, language-specific runtime libraries, and the serialization format for data that is written to a file (or sent across a network connection).

## Generating Your Classes
```shell
protoc --proto_path=IMPORT_PATH --cpp_out=DST_DIR --java_out=DST_DIR --python_out=DST_DIR --go_out=DST_DIR --ruby_out=DST_DIR --objc_out=DST_DIR --csharp_out=DST_DIR path/to/file.proto
```

```sh
protoc -I=$SRC_DIR --cpp_out=$DST_DIR $SRC_DIR/addressbook.proto

#This generates the following files in your specified destination directory:
#    addressbook.pb.h, the header which declares your generated classes.
#    addressbook.pb.cc, which contains the implementation of your classes.
```

# 本例子的编译、运行
```sh
# 添加cmake/common.cmake
# 编写CMakelitsts.txt
# 编译
mkdir build
cd bulid
cmake -DCMAKE_PREFIX_PATH=$MY_INSTALL_DIR ..
make
./write_personal_details  ../address_book.txt
```