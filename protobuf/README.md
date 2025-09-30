# Protocol Buffers for QuestNav

QuestNav uses Protocol Buffers to encode data transmitted over Network Tables. The proto files here are taken from the (QuestNav repo)[https://github.com/QuestNav/QuestNav/tree/main/protos]

To build the protos for python, install the protobuf compiler and run `protoc --python_out=./ *.proto`. Then you'll have to fix the imports in the generated python files by appending `protobuf.` to them. For example `import geometry2d_pb2 as geometry2d__pb2` becomes `import protobuf.geometry2d_pb2 as geometry2d__pb2`.