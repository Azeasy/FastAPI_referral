from fastapi import APIRouter, Depends
from src.models import User
from src.schemas.user import UserResponse
from src.services.auth import get_current_user

router = APIRouter()


@router.post("/me/", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
