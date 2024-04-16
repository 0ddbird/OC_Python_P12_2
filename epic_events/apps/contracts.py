import typer
from rich import print
from rich.table import Table
import decimal
from epic_events.models import session
from epic_events.models.contracts import Contract
import sentry_sdk

app = typer.Typer()


@app.command("list")
def list_contracts():
    """
    List all contracts in the database and display them in a table format.
    """
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
            contract.sales_rep.username,
            contract.event.name if contract.event else "",
            "Yes" if contract.signed else "No",
            str(contract.time_created),
            str(contract.time_updated),
        )

    print(table)


@app.command("create")
def create_contract():
    """Create a new contract.

    This function prompts the user for information to create a new contract and performs validation checks
    on the input values. If the input values are valid, a new contract is created and saved to the database.

    Raises:
        typer.Exit: Raised when the input values are invalid or the contract cannot be created.
    """
    customer_id = typer.prompt("Customer ID")
    value = typer.prompt("Value")
    amount_due = typer.prompt("Amount Due")
    sales_rep_id = typer.prompt("Sales Rep ID")
    is_signed = typer.confirm("Signed")

    try:
        amount_due = decimal.Decimal(amount_due)
        value = decimal.Decimal(value)
    except (decimal.InvalidOperation, ValueError):
        print("Invalid value or amount due.")
        raise typer.Exit(code=1)

    if amount_due > value:
        typer.echo("Amount due cannot be greater than value.")
        raise typer.Exit(code=1)

    if amount_due < 0 or value <= 0:
        typer.echo("Amount due and value cannot be negative.")
        raise typer.Exit(code=1)

    if amount_due == 0 and not is_signed:
        typer.echo("Contract must be signed if paid in full.")
        raise typer.Exit(code=1)

    contract = Contract(
        customer_id=customer_id,
        value=value,
        amount_due=amount_due,
        sales_rep_id=sales_rep_id,
        signed=is_signed,
    )

    session.add(contract)
    session.commit()

    if is_signed:
        sentry_sdk.capture_message(f"The Contract {contract.id} has been signed.")

    typer.echo(f"Contract {contract.id} created.")


@app.command("update")
def update_contract():
    """
    Update a contract with user-provided values.

    This function prompts the user to enter the contract ID and retrieves the corresponding contract from the database.
    It then prompts the user to enter the updated values for the contract, such as value, amount due, sales rep ID, and signed status.
    The function performs validation checks on the entered values and updates the contract in the database if the checks pass.

    Raises:
        typer.Exit: If the contract with the specified ID is not found, or if the entered values are invalid or do not meet the required conditions.

    """

    contract_id = typer.prompt("Contract ID")
    contract = session.query(Contract).get(contract_id)
    if not contract:
        typer.echo(f"Contract {contract_id} not found")
        raise typer.Exit(code=1)
    value = typer.prompt("Value", default=contract.value)
    amount_due = typer.prompt("Amount Due", default=contract.amount_due)
    sales_rep_id = typer.prompt("Sales Rep ID", default=contract.sales_rep.id)
    is_signed = typer.confirm("Signed", default=contract.signed)

    try:
        amount_due = decimal.Decimal(amount_due)
        value = decimal.Decimal(value)
    except (decimal.InvalidOperation, ValueError):
        print("Invalid value or amount due.")
        raise typer.Exit(code=1)

    if amount_due > value:
        typer.echo("Amount due cannot be greater than value.")
        raise typer.Exit(code=1)

    if amount_due < 0 or value <= 0:
        typer.echo("Amount due and value cannot be negative.")
        raise typer.Exit(code=1)

    if amount_due == 0 and not is_signed:
        typer.echo("Contract must be signed if paid in full.")
        raise typer.Exit(code=1)

    contract.value = value
    contract.amount_due = amount_due
    contract.sales_rep_id = sales_rep_id
    contract.signed = is_signed

    session.commit()

    if is_signed:
        sentry_sdk.capture_message(f"The Contract {contract.id} has been signed.")
    typer.echo(f"Contract {contract.id} updated.")


@app.command("delete")
def delete_contract(contract_id: int):
    """
    Deletes a contract with the given contract_id.

    Args:
        contract_id (int): The ID of the contract to be deleted.

    Raises:
        typer.Exit: If the contract with the given contract_id is not found.
    """

    contract = session.query(Contract).get(contract_id)

    if not contract:
        typer.echo(f"Contract {contract_id} not found")
        raise typer.Exit(code=1)

    event = contract.event
    if event:
        session.delete(event)

    session.delete(contract)
    session.commit()
    typer.echo(f"Contract {contract_id} deleted")
