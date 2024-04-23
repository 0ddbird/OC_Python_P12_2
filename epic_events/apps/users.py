import typer
from rich import print
from rich.table import Table

from epic_events.auth.utils import (
    allowed_departments,
    get_current_user,
)
import sentry_sdk
from epic_events.models import session
from epic_events.models.users import User
from epic_events.models.departments import Department
from epic_events.models.departments import ALL, MANAGER

app = typer.Typer()


@app.command("list")
def list_users():
    """
    List all users in the system.

    This function retrieves all users from the database and displays them in a table format.
    The table includes columns for the user's ID, username, email, and user type.
    """

    allowed_departments(ALL)
    users = session.query(User).all()
    users_table = Table(title="Users")

    for column in ("Id", "Username", "Email", "Department"):
        users_table.add_column(column)

    for user in users:
        users_table.add_row(
            str(user.id), user.username, user.email, user.department.name
        )

    print(users_table)


@app.command("create")
def create_user():
    """
    Creates a new user based on user input.

    This function prompts the user to enter the username, password, email, and user type.
    It then creates a new user object based on the selected user type and adds it to the session.

    Raises:
        ValueError: If an invalid user type is selected.
    """

    allowed_departments([MANAGER])
    username = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True)
    email = typer.prompt("Email")

    user_data = {
        "username": username,
        "password": password,
        "email": email,
    }
    user = User(**user_data)
    session.add(user)
    session.commit()

    print("Departments:")
    departments = session.query(Department).all()
    departments = "\n".join([department.name for department in departments])
    print(departments)
    department = typer.prompt("Link user to department")

    sentry_sdk.capture_message(f"The User {user.id} has been created.")
    typer.echo(f"{user.id} created.")


@app.command("update")
def update_user():
    """
    Update user information.

    This function allows the user to update their own profile information or update other user profiles if they are an admin.

    Raises:
        typer.Exit: If the user is not authenticated or if the user ID is not found.

    """
    allowed_departments(ALL)
    request_user = get_current_user()
    if not request_user:
        raise typer.Exit(code=1)

    user_id = typer.prompt("User Id")
    user = session.query(User).get(user_id)

    if user is None:
        typer.echo(f"User {user_id} not found.")
        raise typer.Exit(code=1)

    is_different_user = user.id != request_user.id

    if is_different_user and not request_user.is_superuser:
        typer.echo("You can only update your own profile.")
        raise typer.Exit(code=1)

    username = typer.prompt("Username", default=user.username, type=str)
    password = typer.prompt("Password", default=user.password, hide_input=True)
    email = typer.prompt("Email", default=user.email, type=str)
    user.username = username
    user.set_password(password)
    user.email = email
    session.commit()
    # Logger dans Sentry
    typer.echo(f"User {user_id} updated")


@app.command("delete")
def delete_user(user_id: int):
    """
    Deletes a user with the given user_id.

    Args:
        user_id (int): The ID of the user to be deleted.

    Raises:
        typer.Exit: If the user with the given user_id is not found.

    """
    allowed_departments([UserType.ADMIN])
    user = session.query(User).get(user_id)

    if user is None:
        typer.echo(f"User {user_id} not found")
        raise typer.Exit(code=1)

    session.delete(user)
    session.commit()
    typer.echo(f"User {user_id} deleted")
