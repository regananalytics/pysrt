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

    def _init_mq(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f'tcp://{self.host}:{self.port}')
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.subs)

    def run(self):
        self._init_mq()
        while not self.stop_flag:
            raw_msg = self.socket.recv_string()
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
        self.context.term()
