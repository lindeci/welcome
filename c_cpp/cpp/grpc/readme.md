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