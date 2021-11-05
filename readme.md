
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


## python-streaming-server

使用yield关键字在循环中返回数据

```python
yield response(result=measure_i_info)

```
## golang-client-for-python (sever for )


在golang服务端中，从protubuf中拿到客户端
```golang
  conn, err := grpc.Dial(addr, grpc.WithInsecure())
	client := pb.NewInstrumentsControllerClient(conn)
```

再调用对应的接口：

```golang
res, err := client.IVSweepMode(context.Background(), req)

```





