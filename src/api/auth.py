from fastapi import APIRouter, Depends, HTTPException
from src.core.security import create_access_token
from src.db.redis import get_cache
from src.schemas.user import UserCreate, UserResponse
from src.services.user import create_user, authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db

router = APIRouter()


@router.post("/register/", response_model=UserResponse)
async def register_user(
        user: UserCreate,
        db: AsyncSession = Depends(get_db),
        cache = Depends(get_cache),
):
    db_user = await create_user(db, cache, user)
    return db_user


@router.post("/login/")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(db_user.id)
    return {"access_token": token, "token_type": "bearer"}
