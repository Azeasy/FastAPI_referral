from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.db.base import Base
from datetime import datetime


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referee_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    referrer = relationship('User', foreign_keys=[referrer_id], back_populates='referrals_made')
    referee = relationship('User', foreign_keys=[referee_id], back_populates='referrals_received')
