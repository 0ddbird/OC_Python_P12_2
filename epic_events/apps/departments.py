import typer
from rich import print
from rich.table import Table
from sqlalchemy.exc import IntegrityError

from epic_events.auth.utils import allowed_departments
from epic_events.models import session
from epic_events.models.departments import Department
from epic_events.models.departments import ALL

app = typer.Typer()


@app.command("list")
def list_departments():
    """
    Retrieve a list of departments and display them in a table format.
    """
    allowed_departments(ALL)
    departments = session.query(Department).all()
    departments_table = Table(title="departments")
    columns = ("Id", "Name", "Users")

    for column in columns:
        departments_table.add_column(column)

    for department in departments:
        departments_table.add_row(
            str(department.id),
            department.name,
            ", ".join([user.name for user in department.users]),
        )

    print(departments_table)


@app.command("create")
def create_department():
    """
    Creates a new department.

    This function prompts the user for the department name and creates a new Department object with the provided name.
    The function then adds the department to the session and commits the changes to the database.

    If a department with the same name already exists, an IntegrityError is caught and the function rolls back the session.

    Raises:
        IntegrityError: If a department with the same name already exists in the database.
    """
    allowed_departments([])
    name = typer.prompt("Name")
    department = Department(name=name)

    try:
        session.add(department)
        session.commit()
        typer.echo(f"Department {department.id} created")
    except IntegrityError:
        session.rollback()
        typer.echo(f"Department {name} already exists")


@app.command("update")
def update_department():
    """
    Update the name of a department.

    This function allows users with ADMIN or MANAGER roles to update the name of a department.
    It prompts the user for the department ID and retrieves the corresponding department from the database.
    If the department is not found, it raises an error and exits.
    It then prompts the user for the new name and updates the department's name in the database.

    Raises:
        typer.Exit: If the department is not found.

    """
    allowed_departments([])
    department_id = typer.prompt("Department ID")
    department = session.query(Department).get(department_id)

    if department is None:
        typer.echo(f"Department {department_id} not found")
        raise typer.Exit(code=1)

    name = typer.prompt("Name", default=department.name)
    department.name = name
    session.commit()


@app.command("delete")
def delete_department(department_id: int):
    """
    Deletes a department with the given department_id.

    Args:
        department_id (int): The ID of the department to be deleted.

    Raises:
        typer.Exit: If the department with the given department_id is not found.
    """
    allowed_departments([])
    department = session.query(Department).get(department_id)

    if department is None:
        typer.echo(f"Department {department_id} not found")
        raise typer.Exit(code=1)

    session.delete(department)
    session.commit()
    typer.echo(f"Department {department_id} deleted")
