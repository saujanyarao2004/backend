from security import hash_password, create_access_token

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
import models
from models import User
from security import hash_password

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Backend is running successfully 🚀"}

from schemas import RegisterRequest

@app.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = User(
            email=data.email,
            password_hash=data.password,   # temporarily no hashing
            role="patient"  # hardcoding for now
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException

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

from security import oauth2_scheme, verify_token

@app.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme)):
    email = verify_token(token)
    return {"message": f"Welcome {email}, this is your protected profile"}
