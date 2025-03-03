import pytest
from fastapi import status
from sqlalchemy import select
from httpx import ASGITransport, AsyncClient

from src.db.session import get_db
from src.main import app
from src.models import User


@pytest.mark.asyncio
async def test_generate_referral_code_not_authorized(client):
    response = await client.post(
        "/referrals/code/",
        json={"expiry_in_days": 1}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_generate_referral_code(
        client, test_redis, create_test_user, user_token, db_session
):
    response = await client.post(
        "/referrals/code/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"expiry_in_days": 1},
    )

    assert response.status_code == status.HTTP_200_OK
    res = response.json()
    code = res.get('code')
    assert code
    user_id = int(test_redis.get(code))
    assert user_id == create_test_user.id
    cached_code = test_redis.get(create_test_user.id).decode('utf-8')
    assert cached_code == code


@pytest.mark.asyncio
async def test_register_with_referral_code(
        client, code, user_token, db_session
):
    response = await client.post(
        "/auth/register/",
        json={
            "email": "user9@example.com",
            "password": "string9",
            "referral_code": code,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    response = await client.post(
        "/referrals/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"expiry_in_days": 1},
    )


@pytest.mark.asyncio
async def test_register_with_invalid_referral_code(client):
    response = await client.post(
        "/auth/register/",
        json={
            "email": "user10@example.com",
            "password": "string10",
            "referral_code": "invalid_code",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("detail") == "Invalid referral code"


@pytest.mark.asyncio
async def test_login_with_valid_credentials(client, create_test_user):
    response = await client.post(
        "/auth/login/",
        json={
            "email": create_test_user.email,
            "password": "hashedpassword",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    res = response.json()
    assert "access_token" in res
    assert res["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_with_invalid_credentials(client):
    response = await client.post(
        "/auth/login/",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("detail") == "Invalid credentials"
