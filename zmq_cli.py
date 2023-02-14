import json
import zmq

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

class IGT_Struct:
    IGT_Running_Timer: float = 0.0
    IGT_Cutscene_Timer: float = 0.0
    IGT_Menu_Timer: float = 0.0
    IGT_Pause_Timer: float = 0.0

    def __init__(self, 
        IGT_Running_Timer: float, 
        IGT_Cutscene_Timer: float, 
        IGT_Menu_Timer: float, 
        IGT_Pause_Timer: float
    ):
        self.IGT_Running_Timer = IGT_Running_Timer
        self.IGT_Cutscene_Timer = IGT_Cutscene_Timer
        self.IGT_Menu_Timer = IGT_Menu_Timer
        self.IGT_Pause_Timer = IGT_Pause_Timer

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    @staticmethod
    def from_json(json_string):
        return json.loads(json_string, object_hook=lambda d: IGT_Struct(**d))


while True:
    string = socket.recv_string()
    print(string)