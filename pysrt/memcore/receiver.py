import json
from threading import Thread, Lock
import zmq

class MemReceiver(Thread):
    """Memory Receiver Thread Class
        The MemReceiver class is a thread that listens on a ZeroMQ PUB socket for new data.
        The data is stored in the _data attribute, and can be accessed using the data property which is thread-safe.
    """

    def __init__(self, host='localhost', port=5556, subs=''):
        super().__init__()
        self.host = host
        self.port = port
        self.subs = subs
        self.lock = Lock()
        self.context = None
        self.socket = None
        self._data = None
        self.stop_flag = False
        self._init_mq()

    def _init_mq(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:5556")
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.socket = socket

    def run(self):
        while not self.stop_flag:
            try:
                raw_msg = self.socket.recv_string(flags=zmq.NOBLOCK)
            except:
                continue
            msg = json.loads(raw_msg)
            with self.lock:
                self._data = msg
        self._stop()

    def stop(self):
        self.stop_flag = True
    
    @property
    def data(self):
        with self.lock:
            return self._data
    @data.setter
    def data(self, value):
        with self.lock:
            self._data = value

    def _stop(self):
        self.socket.close()


if __name__ == '__main__':
    import time
    receiver = MemReceiver()
    receiver.start()
    for i in range(5):
        print(receiver.data)
        time.sleep(1)
    receiver.stop()
    receiver.join()
    print('Done!')