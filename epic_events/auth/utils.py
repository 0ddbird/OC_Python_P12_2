import os

import jwt
import typer
from rich import print

from epic_events.auth.storage import TokenStorage
from epic_events.models import session
from epic_events.models.users import User, UserType

storage = TokenStorage()

ALL_AUTH_USER_TYPES = [user_type for user_type in UserType]


def generate_jwt(username: str):
    return jwt.encode(
        {"username": username},
        os.getenv("SECRET_KEY"),
        algorithm="HS256",
    )


def decode_jwt(message: str):
    if message == "No token stored":
        raise ValueError("You are not authenticated. Please login.")
    user = jwt.decode(
        message,
        os.getenv("SECRET_KEY"),
        algorithms=["HS256"],
    )
    return user


def get_current_user() -> User:
    token = storage.request_token()
    try:
        decoded = decode_jwt(token)
    except ValueError as e:
        print(e)
        raise typer.Exit(code=1)

    user = session.query(User).filter_by(username=decoded["username"]).first()
    if user is None:
        typer.echo("User not found")
        raise typer.Exit(code=1)
    else:
        return user


def allow_users(authorized_users: list[UserType]):
    user = get_current_user()
    if not user:
        print("User not found")
        raise typer.Exit(code=1)
    if user.user_type not in [choice.value for choice in UserType]:
        print("User not authorized")
        raise typer.Exit(code=1)
