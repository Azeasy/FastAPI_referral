from pydantic import BaseModel

from src.models import User
from src.schemas.user import UserResponse


class ReferralCreate(BaseModel):
    expiry_in_days: int


class ReferralCodeResponse(BaseModel):
    code: str


class ReferralCodeDeleteResponse(BaseModel):
    deleted: bool


class ReferralResponse(BaseModel):
    id: int
    referee: UserResponse | None = None

    class Config:
        from_attributes = True
