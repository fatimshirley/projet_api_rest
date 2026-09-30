import bcrypt
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from projet_api_rest.core.config import settings


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError("Le mot de passe ne doit pas dépasser 72 octets.")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hash_bytes)


def create_access_token(
    user_id: int,
    expires_minutes: int = 60,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm="HS256",
    )


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise ValueError("Token invalide.")

        return int(user_id)

    except (JWTError, ValueError, TypeError) as error:
        raise ValueError("Token invalide ou expiré.") from error