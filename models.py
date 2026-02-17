from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
