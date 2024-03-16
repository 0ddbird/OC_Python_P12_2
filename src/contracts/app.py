import typer
from rich import print
from rich.table import Table

from src.contracts.models import Contract
from src.db_access import get_db_session

app = typer.Typer()


@app.command("list")
def list_contracts():
    conn = get_db_session()
    contracts = conn.query(Contract).all()
    contracts_table = Table(title="Contracts")
    contracts_table.add_column("Id")
    contracts_table.add_column("Company")
    contracts_table.add_column("Customer")
    contracts_table.add_column("Value")
    contracts_table.add_column("Amount Due")
    contracts_table.add_column("Sales Rep")
    contracts_table.add_column("Event")
    contracts_table.add_column("Signed")
    contracts_table.add_column("Time Created")
    contracts_table.add_column("Time Updated")

    for contract in contracts:
        contracts_table.add_row(
            str(contract.id),
            contract.customer.company.name,
            contract.customer.name,
            str(contract.value),
            str(contract.amount_due),
            contract.sales_rep.name,
            contract.event.name if contract.event else "",
            "Yes" if contract.signed else "No",
            str(contract.time_created),
            str(contract.time_updated),
        )

    print(contracts_table)
