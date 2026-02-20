from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from database import Base
from sqlalchemy.sql import func


# -------------------- USERS TABLE --------------------

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(20), nullable=False)  # patient / doctor / admin
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


# -------------------- CONSENTS TABLE --------------------

class Consent(Base):
    __tablename__ = "consents"

    consent_id = Column(Integer, primary_key=True, index=True)

    # Both reference users table
    patient_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    status = Column(String(20), default="PENDING")  # PENDING / ACTIVE / REVOKED

    otp_code = Column(String(10))
    otp_expires_at = Column(TIMESTAMP)

    granted_at = Column(TIMESTAMP)
    revoked_at = Column(TIMESTAMP)
