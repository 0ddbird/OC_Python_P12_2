import typer
from rich import print
from rich.table import Table
from sqlalchemy.exc import IntegrityError

from epic_events.auth.utils import ALL_AUTHENTICATED_USERS, allow_users
from epic_events.models import session
from epic_events.models.companies import Company
from epic_events.models.users import UserType

app = typer.Typer()


@app.command("list")
def list_companies():
    """
    Retrieve a list of companies and display them in a table format.
    """
    allow_users(ALL_AUTHENTICATED_USERS)
    companies = session.query(Company).all()
    companies_table = Table(title="Companies")
    columns = ("Id", "Name", "Customers")

    for column in columns:
        companies_table.add_column(column)

    for company in companies:
        companies_table.add_row(
            str(company.id),
            company.name,
            ", ".join([customer.name for customer in company.customers]),
        )

    print(companies_table)


@app.command("create")
def create_company():
    """
    Creates a new company.

    This function prompts the user for the company name and creates a new Company object with the provided name.
    The function then adds the company to the session and commits the changes to the database.

    If a company with the same name already exists, an IntegrityError is caught and the function rolls back the session.

    Raises:
        IntegrityError: If a company with the same name already exists in the database.
    """
    allow_users([UserType.ADMIN, UserType.MANAGER, UserType.SALES_REP])
    name = typer.prompt("Name")
    company = Company(name=name)

    try:
        session.add(company)
        session.commit()
        typer.echo(f"Company {company.id} created")
    except IntegrityError:
        session.rollback()
        typer.echo(f"Company {name} already exists")


@app.command("update")
def update_company():
    """
    Update the name of a company.

    This function allows users with ADMIN or MANAGER roles to update the name of a company.
    It prompts the user for the company ID and retrieves the corresponding company from the database.
    If the company is not found, it raises an error and exits.
    It then prompts the user for the new name and updates the company's name in the database.

    Raises:
        typer.Exit: If the company is not found.

    """
    allow_users([UserType.ADMIN, UserType.MANAGER])
    company_id = typer.prompt("Company ID")
    company = session.query(Company).get(company_id)

    if company is None:
        typer.echo(f"Company {company_id} not found")
        raise typer.Exit(code=1)

    name = typer.prompt("Name", default=company.name)
    company.name = name
    session.commit()


@app.command("delete")
def delete_company(company_id: int):
    """
    Deletes a company with the given company_id.

    Args:
        company_id (int): The ID of the company to be deleted.

    Raises:
        typer.Exit: If the company with the given company_id is not found.
    """
    allow_users([UserType.ADMIN, UserType.MANAGER])
    company = session.query(Company).get(company_id)

    if company is None:
        typer.echo(f"Company {company_id} not found")
        raise typer.Exit(code=1)

    session.delete(company)
    session.commit()
    typer.echo(f"Company {company_id} deleted")
