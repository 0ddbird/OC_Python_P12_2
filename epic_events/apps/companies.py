import typer
from rich import print
from rich.table import Table
from sqlalchemy.exc import IntegrityError

from epic_events.auth.utils import allow_users
from epic_events.models import session
from epic_events.models.companies import Company
from epic_events.models.users import UserType

app = typer.Typer()


@app.command("list")
def list_companies():
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
    allow_users([UserType.ADMIN, UserType.MANAGER])
    company = session.query(Company).get(company_id)

    if company is None:
        typer.echo(f"Company {company_id} not found")
        raise typer.Exit(code=1)

    session.delete(company)
    session.commit()
    typer.echo(f"Company {company_id} deleted")
