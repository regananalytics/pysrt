from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text

print('\n\n')
console = Console(width=100, height=9)

# Main HUD
hud = Layout()

hud.split_column(
    Layout(name='upper', ratio=1),
    Layout(name='lower', ratio=2)
)

hud['upper'].split_row(
    Layout(Panel("IGT: 00:00:00", title_align="left"), name='time', ratio=1),
    Layout(name='spacer', ratio=2),
)

hud['lower'].split_column(
    Layout(Progress(), name='hp', ratio=1),
    Layout(name='da', ratio=1)
)

console.print(hud)