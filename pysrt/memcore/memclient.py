import asyncio
import json
import zmq


class MemClient:
    def __init__(self, ip='localhost', port=5556, sub_topic=''):
        self.ip = ip
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{self.ip}:{self.port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, sub_topic)

        self.data = None

    async def recv(self):
        string = self.socket.recv_string()
        self.data = json.loads(string)
        return self.data

    def close(self):
        self.socket.close()
        self.context.term()


async def main():
    mc = MemClient()
    while True:
        data = await mc.recv()
        print(data)


if __name__ == '__main__':
    mc = MemClient()
    asyncio.run(main())
