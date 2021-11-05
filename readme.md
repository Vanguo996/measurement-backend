
## 使用grpc以及protubuf传输来自测量仪器的数据

使用服务端流模式，在protubuf的rpc函数中返回值添加一个`stream`关键字

```
// 服务端流模式，在返回值前面加上一个 stream
  rpc GetStream(StreamRequestData) returns (stream StreamResponseData){}

  // 客户端流模式，在参数前面加上一个 stream
  rpc PutStream(stream StreamRequestData) returns (StreamResponseData){}
  // 双向流模式
  rpc AllStream(stream StreamRequestData) returns (stream StreamResponseData){}

```

通过proto工具生成代码


go:

```
protoc --go_out=plugins=grpc:pb -I . ./sweep.proto

```

python:

```
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I.. ../sweep.proto
```


## python-streaming-server

python部分结构：
```
├── py-server
│   ├── client.py
│   ├── config.py
│   ├── deploy-server.yaml
│   ├── Dockerfile
│   ├── mes
│   ├── __pycache__
│   ├── requirements.txt
│   ├── server.py
│   ├── sweep_pb2_grpc.py
│   ├── sweep_pb2.py
│   ├── sweep.py
│   ├── van-env
│   └── visa-driver
```

运行：
```
source van-env/bin/activate
python server.py
```


使用yield关键字在循环中返回数据

```python
yield response(result=measure_i_info)
```


## golang-client-for-python (also sever for react websockets)

golang部分项目结构
```
├── client.go
├── Dockerfile
├── go.mod
├── go.sum
├── pb
│   └── sweep.pb.go
├── readme.md
└── sweep.proto
```


在golang服务端中，从protubuf中拿到client
```golang
  conn, err := grpc.Dial(addr, grpc.WithInsecure())
	client := pb.NewInstrumentsControllerClient(conn)
```

client调用对应的接口：

```golang
res, err := client.IVSweepMode(context.Background(), req)

```





