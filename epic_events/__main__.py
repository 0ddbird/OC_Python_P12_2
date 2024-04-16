import os
import socket

import sentry_sdk
import typer
from dotenv import load_dotenv
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

load_dotenv()

DSN = os.getenv("SENTRY_DSN")

sentry_sdk.init(dsn=DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0)

storage = TokenStorage()
app = typer.Typer()
app.add_typer(users_app, name="users")
app.add_typer(companies_app, name="companies")
app.add_typer(customers_app, name="customers")
app.add_typer(contracts_app, name="contracts")
app.add_typer(events_app, name="events")


@app.command()
def login() -> None:
    """
    Prompts the user for a username and password, checks if the user exists and the password is correct,
    generates a JWT token, and sends it to the storage.

    Raises:
        socket.error: If there is a socket connection failure.

    Returns:
        None
    """
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


@app.command("logout")
def logout() -> None:
    """
    Logs out the user by terminating the storage connection.

    Raises:
        socket.error: If the socket connection fails.
    """
    try:
        storage.terminate()
        typer.echo("Logout successful")
    except socket.error as e:
        typer.echo(f"Socket connection failed: {e}")


@app.command("whoami")
def get_auth_user():
    """
    Retrieves the authenticated user based on the decoded token.

    Returns:
        User: The authenticated user object.
    """
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


@app.command("error")
def trigger_error():
    print(1 / 0)


if __name__ == "__main__":
    app()
