import typer
from rich import print
from rich.table import Table

from src.auth.utils import ALL_AUTH_USER_TYPES, get_authenticated_user, allow_users
from src.db_access import get_db_session
from src.users.models import User, UserType

app = typer.Typer()


@app.command("list")
def list_users():
    allow_users([UserType.ADMIN, UserType.MANAGER])
    conn = get_db_session()
    users = conn.query(User).all()

    users_table = Table(title="Users")
    users_table.add_column("Id")
    users_table.add_column("Username")
    users_table.add_column("Email")
    users_table.add_column("User type")
    for user in users:
        users_table.add_row(str(user.id), user.username, user.email, user.user_type)
    print(users_table)


@app.command("create")
def create_user():
    allow_users([UserType.ADMIN, UserType.MANAGER])
    username = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True)
    email = typer.prompt("Email")
    type_values = "\n ".join([user_type.value for user_type in UserType])
    print(type_values)
    user_type = typer.prompt("User type", type=UserType)

    conn = get_db_session()
    user = User(
        username=username,
        password=password,
        email=email,
        user_type=user_type.value,
    )
    conn.add(user)
    conn.commit()
    typer.echo(f"{user_type} {user.id} created")


@app.command("update")
def update_user():
    allow_users([ALL_AUTH_USER_TYPES])
    request_user = get_authenticated_user()
    if not request_user:
        raise typer.Exit(code=1)

    conn = get_db_session()
    user_id = typer.prompt("User Id")
    user_found = conn.query(User).get(user_id)

    if not user_found:
        typer.echo(f"User {user_id} not found")
        raise typer.Exit(code=1)

    is_different_user = user_found.id != request_user.id
    if is_different_user and request_user.user_type != UserType.ADMIN.value:
        typer.echo("You can only update your own profile")
        raise typer.Exit(code=1)

    username = typer.prompt("Username", default=user_found.username, type=str)
    password = typer.prompt("Password", default=user_found.password, hide_input=True)
    email = typer.prompt("Email", default=user_found.email, type=str)
    user_found.username = username
    user_found.set_password(password)
    user_found.email = email
    conn.commit()
    typer.echo(f"User {user_id} updated")


@app.command("delete")
def delete_user():
    allow_users([UserType.ADMIN])
    conn = get_db_session()
    user_id = typer.prompt("User Id")
    user_found = conn.query(User).get(user_id)
    if not user_found:
        typer.echo(f"User {user_id} not found")
        raise typer.Exit(code=1)
    conn.delete(user_found)
    conn.commit()
    typer.echo(f"User {user_id} deleted")
