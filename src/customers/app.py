import typer
from rich import print
from rich.table import Table

from src.customers.models import Customer
from src.db_access import get_db_session

app = typer.Typer()


@app.command("list")
def list_customers():
    conn = get_db_session()
    customers = conn.query(Customer).all()
    customers_table = Table(title="Customers")
    customers_table.add_column("Id")
    customers_table.add_column("Name")
    customers_table.add_column("Company")
    customers_table.add_column("Contract")
    customers_table.add_column("Sales Rep")
    customers_table.add_column("Time Created")
    customers_table.add_column("Time Updated")

    for customer in customers:
        customers_table.add_row(
            str(customer.id),
            customer.name,
            customer.company.name,
            customer.contract.id if customer.contract else "",
            customer.sales_rep.name if customer.sales_rep else "",
            str(customer.time_created),
            str(customer.time_updated),
        )

    print(customers_table)
