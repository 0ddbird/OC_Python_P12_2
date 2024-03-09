import typer
from src.auth.utils import decode_jwt
from src.auth.storage import TokenStorage
from src.db_access import get_db_session
from src.users.models import User, UserType


storage = TokenStorage()


class permissions_required:
    def __init__(self, authorized_users: list[UserType]):
        self.authorized_users: list[UserType] = authorized_users

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            user = self.get_authenticated_user()
            if user.type not in self.authorized_users:
                typer.echo("You do not have permission to do this")
            else:
                return func(*args, **kwargs)

        return wrapper

    def get_authenticated_user():
        token = storage.request_token()
        decoded = decode_jwt(token)
        conn = get_db_session()
        user = conn.query(User).filter_by(username=decoded["username"]).first()
        if user is None:
            typer.echo("User not found")
        else:
            return user
