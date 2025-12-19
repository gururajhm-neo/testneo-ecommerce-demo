from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User, UserRole
from schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from config import settings
import secrets

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token handling
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    user_id: int = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current admin user"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def get_current_moderator_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current moderator or admin user"""
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def register_user(db: Session, user_data: UserCreate) -> User:
    """Register a new user"""
    # Check if email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user - use User constructor which will hash the password
    # The User.__init__ expects 'password' (not password_hash) and will hash it
    # Convert schema UserRole enum to model UserRole enum
    from models.user import UserRole as ModelUserRole
    # Get the string value from the schema enum (e.g., "customer") and convert to model enum
    role_value = user_data.role.value if hasattr(user_data.role, 'value') else str(user_data.role)
    # Model UserRole enum: CUSTOMER = "customer", so we need to find by value
    # Find the enum member by its value
    user_role = None
    for role in ModelUserRole:
        if role.value == role_value.lower():
            user_role = role
            break
    if user_role is None:
        # Default to CUSTOMER if not found
        user_role = ModelUserRole.CUSTOMER
    
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,  # Pass plain password, User.__init__ will hash it
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role=user_role
    )
    # User.__init__ already sets email_verification_token via generate_verification_token()
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, user_data: UserLogin) -> TokenResponse:
    """Login user and return tokens"""
    try:
        user = authenticate_user(db, user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        # Normalise role to lowercase string for tokens and schema
        # Handle both enum objects and string values from database
        raw_role = getattr(user, "role", None)
        
        if raw_role is None:
            role_str = "customer"
        elif hasattr(raw_role, "value"):
            # It's an enum object, get its value
            role_str = str(raw_role.value).lower()
        elif hasattr(raw_role, "name"):
            # It's an enum but we got the name instead of value
            # Map enum names to values
            role_name = str(raw_role.name).upper()
            role_map = {
                "CUSTOMER": "customer",
                "ADMIN": "admin",
                "MODERATOR": "moderator",
                "SUPPORT": "support"
            }
            role_str = role_map.get(role_name, "customer")
        else:
            # It's a string or something else
            role_str = str(raw_role).lower()
        
        # Final normalization - ensure it's lowercase
        role_str = role_str.lower().strip()
        
        # Validate it's a valid role, default to customer if not
        valid_roles = ["customer", "admin", "moderator", "support"]
        if role_str not in valid_roles:
            print(f"Warning: Invalid role '{role_str}', defaulting to 'customer'")
            role_str = "customer"

        # Create tokens
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": role_str},
            expires_delta=access_token_expires,
        )

        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "email": user.email}
        )

        # Convert user to UserResponse - handle enum conversion safely
        from schemas.user import UserRole as SchemaUserRole

        # Ensure role_str is valid before creating enum (should already be validated above)
        if role_str not in ["customer", "admin", "moderator", "support"]:
            print(f"Warning: Invalid role '{role_str}', defaulting to 'customer'")
            role_str = "customer"
        
        try:
            schema_role = SchemaUserRole(role_str)
        except (ValueError, TypeError) as e:
            # Fallback to customer if something unexpected is stored
            print(f"Error creating SchemaUserRole from '{role_str}': {e}")
            schema_role = SchemaUserRole.CUSTOMER

        user_dict = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": schema_role,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "is_email_verified": user.is_email_verified,
            "created_at": user.created_at,
            "last_login": user.last_login,
        }
        user_response = UserResponse(**user_dict)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            refresh_token=refresh_token,
            user=user_response,
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the full error for debugging
        import traceback
        error_trace = traceback.format_exc()
        print(f"Login error in login_user: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}",
        )
