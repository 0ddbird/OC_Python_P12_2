import socket

import typer
from rich import print
from sqlalchemy.orm import joinedload

from epic_events.apps.companies import app as companies_app
from epic_events.apps.contracts import app as contracts_app
from epic_events.apps.customers import app as customers_app
from epic_events.apps.events import app as events_app
from epic_events.apps.users import app as users_app
from epic_events.auth.storage import TokenStorage
from epic_events.auth.utils import decode_jwt, generate_jwt
from epic_events.models import session
from epic_events.models.users import User

storage = TokenStorage()
app = typer.Typer()
app.add_typer(users_app, name="users")
app.add_typer(companies_app, name="companies")
app.add_typer(customers_app, name="customers")
app.add_typer(contracts_app, name="contracts")
app.add_typer(events_app, name="events")


@app.command()
def login():
    username = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True)
    user = (
        session.query(User)
        .options(joinedload("*"))
        .filter_by(username=username)
        .first()
    )
    if user is None or not user.check_password(password):
        typer.echo("Invalid username or password")
        return

    jwt = generate_jwt(username)
    try:
        storage.send_token(jwt)
        typer.echo("Login successful")
    except socket.error as e:
        typer.echo(f"Socket connection failed: {e}")


@app.command()
def logout():
    try:
        storage.terminate()
        typer.echo("Logout successful")
    except socket.error as e:
        typer.echo(f"Socket connection failed: {e}")


@app.command("user")
def get_auth_user():
    try:
        token = storage.request_token()
        decoded = decode_jwt(token)
    except socket.error as e:
        typer.echo(f"Socket connection failed: {e}")

    user = session.query(User).filter_by(username=decoded["username"]).first()
    if user is None:
        typer.echo("User not found")
    else:
        print(user.username)
        return user


if __name__ == "__main__":
    app()
