from pydantic import BaseModel
from fastapi.params import Query, Annotated

from src.schemas.user import UserResponse


class ReferralCreate(BaseModel):
    expiry_in_days: Annotated[int, Query(ge=1, default=1)]


class ReferralCodeResponse(BaseModel):
    code: str


class ReferralCodeDeleteResponse(BaseModel):
    deleted: bool


class ReferralResponse(BaseModel):
    id: int
    referee: UserResponse | None = None

    class Config:
        from_attributes = True
