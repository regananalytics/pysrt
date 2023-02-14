import json
from rich.progress import (
    Progress, 
    TextColumn, 
    BarColumn, 
    MofNCompleteColumn
)
import zmq

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

print('\n\n')
with Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(bar_width=80),
    MofNCompleteColumn()
) as progress:
    task1 = progress.add_task("[bold green]Character HP", total=1500)
    task2 = progress.add_task("[bold red]DA Score", total=4500)
    while True:
        string = socket.recv_string()
        data = json.loads(string)
        progress.update(task1, completed=int(list(data.values())[0]))
        progress.update(task2, completed=int(list(data.values())[1]))