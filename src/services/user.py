import redis
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.schemas.user import UserCreate
from sqlalchemy.future import select
from passlib.hash import bcrypt

from src.services.referral import create_referral, get_user_from_referral_code


async def create_user(db: AsyncSession, cache:redis.Redis, user: UserCreate):
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail=str("User already exists"))

    hashed_password = bcrypt.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Registering a referral here
    if user.referral_code:
        user_id = await get_user_from_referral_code(cache, user.referral_code)
        await create_referral(db, user_id=db_user.id, referrer_id=user_id)

    return db_user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user and bcrypt.verify(password, user.hashed_password):
        return user
    return None
