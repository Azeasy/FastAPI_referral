import redis
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid

from sqlalchemy.orm import joinedload

from src.core.config import settings
from src.models.referral import Referral
from src.models.user import User
from src.schemas.referral import ReferralResponse


async def generate_referral_code(cache: redis.Redis, user_id: int, referral) -> dict[str, str]:
    """
    Creates a unique referral code for a user. Only one active code per user is allowed.

    :param cache: Redis cache.
    :param user_id: ID of the user creating the referral code.
    :param referral: ReferralCreate object containing the referral details.
    :return: Newly created Referral code.
    """

    # Ensure the user has no existing active referral code
    result = cache.get(str(user_id))

    if result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Referral code already exists",
        )

    # Create a new referral code
    new_code = str(uuid.uuid4())[:8]  # Shorten UUID for readability
    expiry_days = referral.expiry_in_days or settings.REFERRAL_DEFAULT_EXPIRY_DAYS

    cache.set(str(user_id), new_code, ex=expiry_days * 86400)
    cache.set(str(new_code), user_id, ex=expiry_days * 86400)

    return {'code': new_code}


async def get_referral_code_by_user_id(cache: redis.Redis, user_id) -> dict[str, str]:
    """
    Creates a unique referral code for a user. Only one active code per user is allowed.

    :param cache: Redis cache.
    :param user_id: ID of the user creating the referral code.
    :return: Newly created Referral code.
    """

    # Ensure the user has no existing active referral code
    result = cache.get(str(user_id))

    if result:
        return {'code': result}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Referral code does not exists",
    )


async def get_referral_code_by_email(
        db: AsyncSession,
        cache: redis.Redis,
        email: str
) -> dict[str, str]:
    """
    Retrieves a referral code by the email of the referrer.

    :param db: Async database session.
    :param email: Email of the referrer.
    :return: Referral object if found, else None.
    """
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalars().first()
    if user:
        result = cache.get(str(user.id))

        if result:
            return {'code': result}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Referral code does not exists",
    )


async def delete_referral_code(cache: redis.Redis, user_id: int) -> dict[str, bool]:
    """
    Deletes the current active referral code of a user.

    :param db: Async database session.
    :param user_id: ID of the user.
    :return: True if a code was deleted, False otherwise.
    """
    return {
        'deleted': cache.delete(str(user_id))
    }


async def get_user_from_referral_code(cache:redis.Redis, code: str):
    if code:
        return cache.get(code)


async def create_referral(db: AsyncSession,
                          user_id: int, referrer_id: int):
    referral = Referral(referee_id=int(user_id), referrer_id=int(referrer_id))
    db.add(referral)
    await db.commit()
    await db.refresh(referral)

    return referral


async def get_referrals_by_user_id(db: AsyncSession, user_id: int):
    """
    Retrieves all users who have registered using a given user's referral code.

    :param db: Async database session.
    :param user_id: ID of the referrer.
    :return: List of referred users.
    """
    result = await db.execute(
        select(Referral).options(joinedload(Referral.referee))
        .where(Referral.referrer_id == user_id)
    )
    referrals = result.scalars().all()
    return [ReferralResponse(
        id=referral.id,
        referrer_id=referral.referrer_id,
        referee=referral.referee
    ) for referral in referrals]
