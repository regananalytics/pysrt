import json
from rich.progress import (
    Progress, 
    TextColumn, 
    BarColumn, 
    MofNCompleteColumn
)
import zmq

#  Socket to talk to server


print('\n\n')
with Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(bar_width=80),
    MofNCompleteColumn()
) as progress:
    hp = progress.add_task("[bold green]Character HP", total=1500)
    da_rank = progress.add_task("[bold green]DA Rank", total=5)
    da_score = progress.add_task("[bold green]DA Score", total=6000)
    while True:
        string = socket.recv_string()
        data = json.loads(string)
        progress.update(hp, completed=data['Player_HP']['Current_HP'], total=data['Player_HP']['Max_HP'])
        progress.update(da_rank, completed=data['DA']['DA_Rank'])
        progress.update(da_score, completed=data['DA']['DA_Score'])