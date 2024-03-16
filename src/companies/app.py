import typer
from rich import print
from rich.table import Table

from src.companies.models import Company
from src.db_access import get_db_session

app = typer.Typer()


@app.command("list")
def list_companies():
    conn = get_db_session()
    companies = conn.query(Company).all()
    companies_table = Table(title="Companies")
    companies_table.add_column("Id")
    companies_table.add_column("Name")
    companies_table.add_column("Customers")

    for company in companies:
        companies_table.add_row(
            str(company.id),
            company.name,
            ", ".join([customer.name for customer in company.customers]),
        )
    print(companies_table)
