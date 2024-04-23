import os

import jwt
import typer
from rich import print

from epic_events.auth.storage import TokenStorage
from epic_events.models import session
from epic_events.models.users import User, UserType

storage = TokenStorage()

ALL_AUTHENTICATED_USERS = [user_type for user_type in UserType]


def generate_jwt(username: str) -> str:
    """
    Generates a JSON Web Token (JWT) for the given username.

    Args:
        username (str): The username for which the JWT is generated.

    Returns:
        str: The generated JWT.

    """
    return jwt.encode(
        {"username": username},
        os.getenv("SECRET_KEY"),
        algorithm="HS256",
    )


def decode_jwt(message: str) -> dict:
    """
    Decode a JSON Web Token (JWT) and return the user information.

    Args:
        message (str): The JWT to decode.

    Returns:
        dict: The decoded user information.

    Raises:
        ValueError: If the message is "No token stored".

    """
    if message == "No token stored":
        raise ValueError("You are not authenticated. Please login.")
    user = jwt.decode(
        message,
        os.getenv("SECRET_KEY"),
        algorithms=["HS256"],
    )
    return user


def get_current_user() -> User:
    """
    Retrieves the current user based on the token stored in the storage.

    Returns:
        The User object representing the current user.

    Raises:
        ValueError: If there is an error decoding the JWT token.
        typer.Exit: If the user is not found.
    """
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
    return user


def allow_users(authorized_user_types: list[UserType]) -> None:
    """
    Checks if the current user is authorized to access the system.

    Args:
        authorized_users (list[UserType]): A list of authorized user types.

    Raises:
        typer.Exit: If the current user is not found or not authorized.

    Returns:
        None
    """
    user = get_current_user()
    if not user:
        print("User not found")
        raise typer.Exit(code=1)

    if user.user_type == UserType.ADMIN.value:
        return

    if user.user_type not in [choice.value for choice in authorized_user_types]:
        print("User not authorized")
        raise typer.Exit(code=1)
