import grpc

import van_pb2 as pb2
import van_pb2_grpc as pb2_grpc

addr = "127.0.0.1:52002"

channel = grpc.insecure_channel(addr)

client = pb2_grpc.VanStub(channel=channel)
req = pb2.request(name="van", age=30)
response = client.HelloVan(req)
print(response.result)