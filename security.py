# ==========================================================
# 🔐 security.py
# ==========================================================

# Firebase
import firebase_admin
from firebase_admin import credentials, auth

# FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Database
from sqlalchemy.orm import Session
from database import get_db
from models import User, Consent, AuditLog

# Utils
from datetime import datetime


# ==========================================================
# 🔥 Initialize Firebase (Safe Initialization)
# ==========================================================
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)


# ==========================================================
# 🔐 Token Extractor
# ==========================================================
security = HTTPBearer()


# ==========================================================
# 📝 1️⃣ Audit Logging System
# ==========================================================
def log_action(
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int,
    db: Session
):
    log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        created_at=datetime.utcnow()
    )

    db.add(log)
    db.commit()


# ==========================================================
# 🔐 2️⃣ Get Current Authenticated User
# ==========================================================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme"
        )

    token = credentials.credentials

    try:
        decoded_token = auth.verify_id_token(token)

        email = decoded_token.get("email")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token (no email)"
            )

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not registered in system"
            )

        # 🔒 Automatic inactive account blocking
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        return user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


# ==========================================================
# 🔐 3️⃣ Role-Based Access Control
# ==========================================================
def require_role(role: str):
    def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:

        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: insufficient permissions"
            )

        return current_user

    return role_checker


# ==========================================================
# 🔐 4️⃣ Patient or Admin Enforcement
# ==========================================================
def enforce_patient_or_admin(
    patient_id: int,
    current_user: User
):

    if current_user.role == "admin":
        return True

    if current_user.role == "patient" and current_user.user_id == patient_id:
        return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied: not authorized for this patient"
    )


# ==========================================================
# 🔐 5️⃣ Doctor Consent Enforcement (Reusable Dependency)
# ==========================================================
from models import Doctor, Patient

def require_doctor_consent():
    def consent_checker(
        patient_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):

        # Only doctors allowed
        if current_user.role != "doctor":
            raise HTTPException(
                status_code=403,
                detail="Only doctors require consent validation"
            )

        # 🔹 Find doctor profile using user_id
        doctor = db.query(Doctor).filter(
            Doctor.user_id == current_user.user_id
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=403,
                detail="Doctor profile not found"
            )

        # 🔹 Check consent using doctor.doctor_id
        consent = db.query(Consent).filter(
            Consent.patient_id == patient_id,
            Consent.doctor_id == doctor.doctor_id,
            Consent.status == "ACTIVE"
        ).first()

        if not consent:
            raise HTTPException(
                status_code=403,
                detail="Consent not granted by patient"
            )

        return current_user

    return consent_checker