from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.models.user import User
from app.schemas.auth import UserLogin, Token, UserOut

router = APIRouter()


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    
    # Auto-initialize admin user if db is fresh
    if not user and login_data.username == "admin" and login_data.password == "admin123":
        user = User(
            email="admin@hospital.org",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="Chief Biomedical Security Admin",
            role="hospital_admin"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(subject=user.username)
    return Token(
        access_token=access_token,
        user_role=user.role,
        username=user.username
    )


@router.get("/me", response_model=UserOut)
def get_current_user(db: Session = Depends(get_db)):
    # Default return for initial dev session
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        user = User(
            email="admin@hospital.org",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="Chief Biomedical Security Admin",
            role="hospital_admin"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
