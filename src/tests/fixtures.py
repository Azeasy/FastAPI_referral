import uuid

import pytest_asyncio
from datetime import datetime, timedelta
from jose import jwt

from src.core.config import settings
from src.models.user import User
from src.core.security import ALGORITHM


@pytest_asyncio.fixture(scope="module")
async def create_test_user(db_session):
    user = User(email="test@example.com", hashed_password="hashedpassword")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="module")
async def user_token(create_test_user):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(create_test_user.id)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


@pytest_asyncio.fixture(scope="module")
async def code(test_redis, create_test_user):
    ref_code = str(uuid.uuid4())[:8]
    test_redis.set(ref_code, create_test_user.id)
    test_redis.set(str(create_test_user.id), ref_code)
    return ref_code
