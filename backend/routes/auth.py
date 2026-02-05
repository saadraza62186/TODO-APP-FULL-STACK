from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
import jwt
from datetime import datetime, timedelta
import hashlib
import uuid

from db import get_session
from models import User
from config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Authentication"])


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str
    name: str | None


def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def create_access_token(user_id: str, email: str) -> str:
    """Create JWT access token."""
    payload = {
        "user_id": user_id,
        "sub": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return token


@router.post("/auth/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def sign_up(request: SignUpRequest, session: Session = Depends(get_session)):
    """
    Register a new user.
    
    Args:
        request: Sign up request with email, password, and optional name
        session: Database session
        
    Returns:
        AuthResponse with access token and user info
        
    Raises:
        HTTPException 400: If email already exists
    """
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == request.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=request.email,
        name=request.name,
        password_hash=hash_password(request.password),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Generate token
    access_token = create_access_token(user.id, user.email)
    
    logger.info(f"New user registered: {user.email}")
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        name=user.name
    )


@router.post("/auth/signin", response_model=AuthResponse)
def sign_in(request: SignInRequest, session: Session = Depends(get_session)):
    """
    Sign in an existing user.
    
    Args:
        request: Sign in request with email and password
        session: Database session
        
    Returns:
        AuthResponse with access token and user info
        
    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Find user
    user = session.exec(
        select(User).where(User.email == request.email)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    password_hash = hash_password(request.password)
    if user.password_hash != password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate token
    access_token = create_access_token(user.id, user.email)
    
    logger.info(f"User signed in: {user.email}")
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        name=user.name
    )
