from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
import models
from models import User
from schemas import RegisterRequest
from security import get_current_user, require_role
from models import User, Patient, Doctor

app = FastAPI()

Base.metadata.create_all(bind=engine)


# ------------------ DB Dependency ------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ Root ------------------

@app.get("/")
def root():
    return {"message": "Backend is running successfully 🚀"}


# ------------------ Register (Optional - For local DB user creation) ------------------

from fastapi import HTTPException

@app.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    # 🔒 Check if user already exists
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create user
    user = User(
        email=data.email,
        password_hash=data.password,
        role=data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Automatically create profile based on role
    if user.role == "patient":
        patient = Patient(user_id=user.user_id)
        db.add(patient)

    elif user.role == "doctor":
        doctor = Doctor(user_id=user.user_id)
        db.add(doctor)

    db.commit()

    return {"message": "User registered successfully"}

# ------------------ Protected Profile ------------------

from security import log_action

@app.get("/profile")
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    log_action(
        user_id=current_user.user_id,
        action="VIEW",
        entity_type="PROFILE",
        entity_id=current_user.user_id,
        db=db
    )

    return {
        "email": current_user.email,
        "role": current_user.role
    }


# ------------------ Admin Only Route ------------------

@app.get("/admin/users")
def get_all_users(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    log_action(
        user_id=current_user.user_id,
        action="VIEW",
        entity_type="USER_LIST",
        entity_id=0,
        db=db
    )

    return db.query(User).all()

from models import AuditLog

@app.get("/admin/audit-logs")
def get_audit_logs(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    return db.query(AuditLog).all()


# ------------------ consent ------------------
from security import require_doctor_consent

@app.get("/patients/{patient_id}/records")
def get_patient_records(
    patient_id: int,
    current_user: User = Depends(require_doctor_consent())
):
    return {
        "message": f"Doctor {current_user.email} can access patient {patient_id} records"
    }