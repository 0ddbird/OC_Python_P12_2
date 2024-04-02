import typer
from rich import print
from rich.table import Table

from epic_events.models import session
from epic_events.models.contracts import Contract

app = typer.Typer()


@app.command("list")
def list_contracts():
    contracts = session.query(Contract).all()
    table = Table(title="Contracts")
    columns = (
        "Id",
        "Company",
        "Customer",
        "Value",
        "Amount Due",
        "Sales Rep",
        "Event",
        "Signed",
        "Time Created",
        "Time Updated",
    )

    for column in columns:
        table.add_column(column)

    for contract in contracts:
        table.add_row(
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

    print(table)


@app.command("create")
def create_contract():
    customer_id = typer.prompt("Customer ID")
    value = typer.prompt("Value", type=float)
    amount_due = typer.prompt("Amount Due", type=float)
    sales_rep_id = typer.prompt("Sales Rep ID")
    signed = typer.confirm("Signed")

    if amount_due > value:
        typer.echo("Amount due cannot be greater than value.")
        raise typer.Exit(code=1)

    if amount_due < 0 or value <= 0:
        typer.echo("Amount due and value cannot be negative.")
        raise typer.Exit(code=1)

    if amount_due == value and not signed:
        typer.echo("Contract must be signed if paid in full.")
        raise typer.Exit(code=1)

    contract = Contract(
        customer_id=customer_id,
        value=value,
        amount_due=amount_due,
        sales_rep_id=sales_rep_id,
        signed=signed,
    )

    session.add(contract)
    session.commit()
    typer.echo(f"Contract {contract.id} created.")
