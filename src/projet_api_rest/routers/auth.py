from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from projet_api_rest.core.security import create_access_token
from projet_api_rest.database.connection import get_db
from projet_api_rest.schemas.auth import LoginRequest, TokenResponse
from projet_api_rest.schemas.user import UserCreate, UserResponse
from projet_api_rest.services.user_service import (
    authenticate_user,
    create_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        user = create_user(db, user_data)
        return user

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        user = authenticate_user(
            db,
            login_data.email,
            login_data.password,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        ) from error

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }