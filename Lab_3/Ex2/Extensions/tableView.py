from rich.console import Console
from rich.table import Table

def setColumnsWidth(table: Table, width: float) -> None:
    """
    Define a largura das colunas da tabela que será impressa.
    """
    for i, column in enumerate(table.columns):
        table.columns[i].width = width
        
def drawTable(tableBody: list[list[any]], Tableheader: list[str], TableTitle: str) -> None:
    """
    Recebe os dados de uma tabela qualquer e imprime os dados da mesmo de uma maneira personalizada.    
    """
    table = Table(title=TableTitle)

    for headerColumn in Tableheader:
        table.add_column(headerColumn)
    
    for bodyRow in tableBody:
        table.add_row(*bodyRow, style='bright_green')

    print()
    console = Console()
    setColumnsWidth(table, 12)
    table.columns[0].width = 18
    console.print(table)