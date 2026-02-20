from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User


# 🔐 Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# 🔑 JWT settings
SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 🔑 Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 👤 Get current logged-in user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        db.close()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # 🔐 Role-based access control
def require_role(role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(
                status_code=403,
                detail="Access denied: insufficient permissions"
            )
        return current_user
    return role_checker

from models import Consent

def check_consent(patient_id: int, current_user: User, db: Session):

    # Only doctors require consent check
    if current_user.role != "doctor":
        raise HTTPException(
            status_code=403,
            detail="Only doctors can access patient records"
        )

    consent = db.query(Consent).filter(
        Consent.patient_id == patient_id,
        Consent.doctor_id == current_user.user_id,
        Consent.status == "ACTIVE"
    ).first()

    if not consent:
        raise HTTPException(
            status_code=403,
            detail="Consent required to access this patient's records"
        )

    return True
