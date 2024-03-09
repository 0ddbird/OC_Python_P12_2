import socket

import typer
from sqlalchemy.orm import joinedload

from src.auth.storage import TokenStorage
from src.auth.utils import decode_jwt, generate_jwt
from src.db_access import get_db_session
from src.users.models import User
from src.users.app import app as users_app

storage = TokenStorage()
app = typer.Typer()
app.add_typer(users_app, name="users")


@app.command()
def login():
    username = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True)
    conn = get_db_session()
    user = (
        conn.query(User).options(joinedload("*")).filter_by(username=username).first()
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
    conn = get_db_session()
    user = conn.query(User).filter_by(username=decoded["username"]).first()
    if user is None:
        typer.echo("User not found")
    else:
        print(user.username)
        return user


if __name__ == "__main__":
    app()
