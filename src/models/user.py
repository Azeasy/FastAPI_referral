from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    referrals_made = relationship('Referral', foreign_keys='Referral.referrer_id', back_populates='referrer')
    referrals_received = relationship('Referral', foreign_keys='Referral.referee_id', back_populates='referee')
