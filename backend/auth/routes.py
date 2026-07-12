from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from database.connection import get_session
from database.models import User, Role
from auth.models import UserLogin, UserCreate, UserResponse, TokenResponse
from auth.service import authenticate_user, create_access_token, create_user

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_user(session, user_data.model_dump())

@router.get("/me", response_model=UserResponse)
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    from jose import JWTError, jwt
    try:
        payload = jwt.decode(token, "your-secret-key-change-in-production", algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = session.exec(select(User).where(User.email == email)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)
