from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshTokenRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth import AuthService, AuthenticationError, EmailAlreadyRegisteredError

router = APIRouter(prefix="/auth")
SessionDependency = Annotated[AsyncSession, Depends(get_db)]


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, session: SessionDependency) -> User:
    try:
        return await AuthService(session).register(payload.email, payload.password, payload.full_name)
    except EmailAlreadyRegisteredError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: SessionDependency) -> TokenResponse:
    try:
        return await AuthService(session).login(payload.email, payload.password)
    except AuthenticationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshTokenRequest, session: SessionDependency) -> TokenResponse:
    try:
        return await AuthService(session).refresh(payload.refresh_token)
    except AuthenticationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: RefreshTokenRequest, session: SessionDependency) -> Response:
    try:
        await AuthService(session).logout(payload.refresh_token)
    except AuthenticationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user
