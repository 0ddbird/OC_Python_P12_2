import typer
from rich import print
from rich.table import Table

from epic_events.auth.utils import allowed_departments
from epic_events.models import session
from epic_events.models.companies import get_or_create_company
from epic_events.models.customers import Customer
from epic_events.models.users import User
from epic_events.models.departments import ALL, MANAGER, SALES

app = typer.Typer()


@app.command("list")
def list_customers():
    """
    Retrieve and display a list of customers.

    This function queries the database to retrieve all customers and displays them in a table format.
    The table includes columns for customer ID, name, company, sales representative, time created, and time updated.
    """
    allowed_departments(ALL)

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
    """
    Creates a new customer.

    This function prompts the user for the customer's name, company name, and sales rep ID.
    It then creates a new customer object and adds it to the session.

    Raises:
        typer.Exit: If the sales rep with the specified ID is not found.
    """
    allowed_departments([MANAGER, SALES])
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
    """
    Update a customer's information.

    This function allows users with ADMIN, MANAGER, or SALES_REP roles to update a customer's information.
    It prompts the user for the customer ID and retrieves the corresponding customer from the database.
    If the customer is not found, it raises an error and exits.
    It then prompts the user for the updated name, company name, and sales rep ID.
    It retrieves the company and sales rep from the database based on the provided information.
    If the sales rep is not found, it raises an error and exits.
    Finally, it updates the customer's name, company, and sales rep in the database and commits the changes.

    Raises:
        typer.Exit: If the customer or sales rep is not found.

    """
    allowed_departments([MANAGER, SALES])
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
    """
    Deletes a customer with the given customer_id.

    Args:
        customer_id (int): The ID of the customer to be deleted.
    """

    allowed_departments([MANAGER, SALES])
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
