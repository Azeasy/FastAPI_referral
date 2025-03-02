from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    referral_code: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True
