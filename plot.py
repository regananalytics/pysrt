import time
from rich.progress import (
    Progress, 
    TextColumn, 
    BarColumn, 
    MofNCompleteColumn
)

with Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(bar_width=80),
    MofNCompleteColumn()
) as progress:
    task1 = progress.add_task("[bold green]Character HP", total=1500)
    task2 = progress.add_task("[bold red]DA Score", total=4500)
    count = 0
    while not progress.finished:
        count += 1
        progress.update(task1, completed=1000)
        progress.update(task2, completed=300)
        if count == 50:
            progress.add_task("[bold yellow]XP", total=1000)
        if count == 100:
            progress.remove_task(task2)
        time.sleep(0.01) 