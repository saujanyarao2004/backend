from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from security import require_role

from database import engine, Base, SessionLocal
import models
from models import User
from schemas import RegisterRequest
from security import hash_password, create_access_token, get_current_user


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


# ------------------ Register ------------------

@app.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = User(
        email=data.email,
        password_hash=data.password,   # hashing can be re-enabled later
        role="patient"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}


# ------------------ Login ------------------

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if user.password_hash != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ------------------ Protected Profile ------------------

@app.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role": current_user.role
    }

@app.get("/admin/users")
def get_all_users(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    return db.query(User).all()
