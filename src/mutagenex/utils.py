import sys
import builtins

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


progress_bar = Progress(
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    BarColumn(),
    MofNCompleteColumn(),
    TextColumn("•"),
    TimeElapsedColumn(),
    TextColumn("•"),
    TimeRemainingColumn(),
)

def suppress_pymol_print(*args, **kwargs):
    # Se il messaggio proviene da PyMOL, non fare nulla
    if 'pymol' in sys.modules:
        return  # Ignora il print
    # Altrimenti, passa il print originale
    original_print(*args, **kwargs)


original_print = builtins.print
builtins.print = suppress_pymol_print
