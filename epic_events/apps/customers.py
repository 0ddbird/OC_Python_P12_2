import typer
from rich import print
from rich.table import Table

from epic_events.auth.utils import ALL_AUTHENTICATED_USERS, allow_users
from epic_events.models import session
from epic_events.models.companies import get_or_create_company
from epic_events.models.customers import Customer
from epic_events.models.users import User, UserType

app = typer.Typer()


@app.command("list")
def list_customers():
    allow_users(ALL_AUTHENTICATED_USERS)
    customers = session.query(Customer).all()
    table = Table(title="Customers")
    columns = (
        "Id",
        "Name",
        "Company",
        "Sales Rep",
        "Time created",
        "Time updated",
    )

    for column in columns:
        table.add_column(column)

    for customer in customers:
        table.add_row(
            str(customer.id),
            customer.name,
            customer.company.name,
            str(customer.sales_rep.username) if customer.sales_rep.username else "",
            str(customer.time_created),
            str(customer.time_updated),
        )

    print(table)


@app.command("create")
def create_customer():
    allow_users([UserType.MANAGER, UserType.SALES_REP])
    name = typer.prompt("Name")
    company_name = typer.prompt("Company name")
    sales_rep_id = typer.prompt("Sales Rep ID")
    company = get_or_create_company(session, company_name)
    sales_rep = session.query(User).get(sales_rep_id)

    if sales_rep is None:
        typer.echo(f"SalesRep {sales_rep_id} not found.")
        raise typer.Exit(code=1)

    customer = Customer(
        name=name,
        company=company,
        sales_rep=sales_rep,
    )
    session.add(customer)
    session.commit()
    typer.echo(f"{customer} created.")


@app.command("update")
def update_customer():
    allow_users([UserType.MANAGER, UserType.SALES_REP])
    customer_id = typer.prompt("Customer ID")
    customer = session.query(Customer).get(customer_id)

    if customer is None:
        typer.echo(f"Customer {customer_id} not found")
        raise typer.Exit(code=1)

    name = typer.prompt("Name", default=customer.name)
    company_name = typer.prompt("Company name", default=customer.company.name)
    sales_rep_id = typer.prompt("Sales Rep ID", default=customer.sales_rep.id)
    company = get_or_create_company(session, company_name)
    sales_rep = session.query(User).get(sales_rep_id)

    if sales_rep is None:
        typer.echo(f"SalesRep {sales_rep_id} not found.")
        raise typer.Exit(code=1)

    customer.name = name
    customer.company = company
    customer.sales_rep = sales_rep
    session.commit()

    typer.echo(f"{customer} updated.")


@app.command("delete")
def delete_customer(customer_id: int):
    allow_users([UserType.MANAGER])
    customer = session.query(Customer).get(customer_id)

    if customer is None:
        typer.echo(f"Customer {customer_id} not found")
        raise typer.Exit(code=1)

    company = customer.company
    session.delete(customer)
    session.commit()

    remaining_customers = (
        session.query(Customer).filter_by(company_id=company.id).first()
    )
    if remaining_customers is None:
        session.delete(company)
        session.commit()

    typer.echo(f"Customer {customer_id} deleted")
