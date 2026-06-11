from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_database_session
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import TokenResponse
from app.security import get_password_hash, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_payload: UserCreate, db_session: AsyncSession = Depends(get_database_session)):
    query = select(UserModel).filter(UserModel.username == user_payload.username)
    result = await db_session.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya se encuentra registrado."
        )

    hashed_password = get_password_hash(user_payload.password)
    new_user = UserModel(
        username=user_payload.username,
        hashed_password=hashed_password
    )

    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    return new_user

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_database_session)
):
    query = select(UserModel).filter(UserModel.username == form_data.username)
    result = await db_session.execute(query)
    target_user = result.scalars().first()

    if not target_user or not verify_password(form_data.password, target_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de acceso invalidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject_identifier=target_user.username)
    return {"access_token": access_token, "token_type": "bearer"}