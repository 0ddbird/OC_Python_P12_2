import os

import jwt


def generate_jwt(username: str):
    return jwt.encode(
        {"username": username},
        os.getenv("SECRET_KEY"),
        algorithm="HS256",
    )


def decode_jwt(token: str):
    user = jwt.decode(
        token,
        os.getenv("SECRET_KEY"),
        algorithms=["HS256"],
    )
    return user
