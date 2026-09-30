from sqlalchemy import select
from sqlalchemy.orm import Session

from projet_api_rest.core.security import hash_password, verify_password
from projet_api_rest.models.user import User
from projet_api_rest.schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.scalar(
        select(User).where(User.email == user_data.email)
    )

    if existing_user:
        raise ValueError(
            "Un utilisateur avec cet email existe déjà."
        )

    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User:
    user = db.scalar(
        select(User).where(User.email == email)
    )

    if user is None:
        raise ValueError("Email ou mot de passe incorrect.")

    if not verify_password(password, user.password):
        raise ValueError("Email ou mot de passe incorrect.")

    return user