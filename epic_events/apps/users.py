import typer
from rich import print
from rich.table import Table

from epic_events.auth.utils import ALL_AUTH_USER_TYPES, allow_users, get_current_user
from epic_events.models import session
from epic_events.models.users import (
    Admin,
    Manager,
    SalesRep,
    SupportRep,
    User,
    UserType,
)

app = typer.Typer()


@app.command("list")
def list_users():
    allow_users([UserType.ADMIN, UserType.MANAGER])
    users = session.query(User).all()
    users_table = Table(title="Users")

    for column in ("Id", "Username", "Email", "User type"):
        users_table.add_column(column)

    for user in users:
        users_table.add_row(str(user.id), user.username, user.email, user.user_type)

    print(users_table)


@app.command("create")
def create_user():
    allow_users([UserType.ADMIN, UserType.MANAGER])
    username = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True)
    email = typer.prompt("Email")
    print("User types options:")
    type_values = "\n".join([user_type.value for user_type in UserType])
    print(type_values)
    user_type = typer.prompt("Choose user type", type=UserType)

    user_data = {
        "username": username,
        "password": password,
        "email": email,
        "user_type": user_type.value,
    }

    match user_type:
        case UserType.ADMIN:
            user = Admin(**user_data)
        case UserType.MANAGER:
            user = Manager(**user_data)
        case UserType.SALES_REP:
            user = SalesRep(**user_data)
        case UserType.SUPPORT_REP:
            user = SupportRep(**user_data)
        case _:
            raise ValueError("Invalid user type")

    session.add(user)
    session.commit()
    typer.echo(f"{user_type} {user.id} created.")


@app.command("update")
def update_user():
    allow_users([ALL_AUTH_USER_TYPES])
    request_user = get_current_user()
    if not request_user:
        raise typer.Exit(code=1)

    user_id = typer.prompt("User Id")
    user = session.query(User).get(user_id)

    if user is None:
        typer.echo(f"User {user_id} not found.")
        raise typer.Exit(code=1)

    is_different_user = user.id != request_user.id

    if is_different_user and request_user.user_type != UserType.ADMIN.value:
        typer.echo("You can only update your own profile.")
        raise typer.Exit(code=1)

    username = typer.prompt("Username", default=user.username, type=str)
    password = typer.prompt("Password", default=user.password, hide_input=True)
    email = typer.prompt("Email", default=user.email, type=str)
    user.username = username
    user.set_password(password)
    user.email = email
    session.commit()
    typer.echo(f"User {user_id} updated")


@app.command("delete")
def delete_user(user_id: int):
    allow_users([UserType.ADMIN])
    user = session.query(User).get(user_id)

    if user is None:
        typer.echo(f"User {user_id} not found")
        raise typer.Exit(code=1)

    session.delete(user)
    session.commit()
    typer.echo(f"User {user_id} deleted")
