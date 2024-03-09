import typer
from permissions.decorators import permissions_required


from src.db_access import get_db_session
from src.users.models import User, UserType

app = typer.Typer()


@permissions_required([UserType.ADMIN, UserType.MANAGER])
@app.command()
def create():
    username = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True)
    email = typer.prompt("Email")
    type_values = [user_type.value for user_type in UserType]
    type_value_options = "\n ".join(type_values)
    print(type_value_options)
    user_type = typer.prompt("Type", type=UserType, show_choices=True)

    conn = get_db_session()
    user = User(
        username=username,
        password=password,
        email=email,
        type=user_type.value,
    )
    conn.add(user)
    conn.commit()

    typer.echo(f"{user_type} {user.id} created")


@permissions_required([UserType.ADMIN, UserType.MANAGER])
@app.command()
def list():
    conn = get_db_session()
    users = conn.query(User).all()
    for user in users:
        typer.echo(f"Username: {user.username}")
