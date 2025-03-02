from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.redis import get_cache
from src.services.referral import generate_referral_code, \
    get_referrals_by_user_id, get_referral_code_by_user_id, \
    delete_referral_code, get_referral_code_by_email
from src.schemas.referral import ReferralResponse, ReferralCreate, \
    ReferralCodeResponse, ReferralCodeDeleteResponse
from src.db.session import get_db
from src.services.auth import get_current_user
from src.models.user import User

router = APIRouter()


@router.get("/", response_model=list[ReferralResponse])
async def get_my_referrals(
        db:AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return await get_referrals_by_user_id(db, current_user.id)


@router.get("/get_by_id", response_model=list[ReferralResponse])
async def get_user_referrals_by_id(
        user_id: int,
        db:AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return await get_referrals_by_user_id(db, user_id)


@router.post("/code/", response_model=ReferralCodeResponse)
async def generate_my_referral_code(
        referral: ReferralCreate,
        current_user: User = Depends(get_current_user),
        cache = Depends(get_cache),
):
    return await generate_referral_code(cache, current_user.id, referral)


@router.get("/code/", response_model=ReferralCodeResponse)
async def get_my_referral_code(
        current_user: User = Depends(get_current_user),
        cache = Depends(get_cache),
):
    return await get_referral_code_by_user_id(cache, current_user.id)


@router.delete("/code/", response_model=ReferralCodeDeleteResponse)
async def delete_my_referral_code(
        current_user: User = Depends(get_current_user),
        cache = Depends(get_cache),
):
    return await delete_referral_code(cache, current_user.id)


@router.get("/code/get_by_email", response_model=ReferralCodeResponse)
async def get_user_referral_code_by_email(
        email: str,
        cache = Depends(get_cache),
        db = Depends(get_db)
):
    return await get_referral_code_by_email(db, cache, email)
