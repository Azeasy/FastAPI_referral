from src.api import auth, referral, user
from fastapi import FastAPI

app = FastAPI(title="Referral System API", version="1.0")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(referral.router, prefix="/referrals", tags=["Referrals"])
app.include_router(user.router, prefix="/user", tags=["User"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Referral System API!"}
