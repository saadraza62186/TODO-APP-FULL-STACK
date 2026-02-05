from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from config import settings
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Verify JWT token and extract user_id.
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        str: User ID from token
        
    Raises:
        HTTPException: If token is invalid, expired, or missing user_id
    """
    token = credentials.credentials
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        
        # Extract user_id
        user_id: str = payload.get("user_id") or payload.get("sub")
        
        if user_id is None:
            logger.warning("Token missing user_id")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.debug(f"Authenticated user: {user_id}")
        return user_id
        
    except ExpiredSignatureError:
        logger.warning("Expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (DecodeError, InvalidTokenError) as e:
        logger.warning(f"JWT validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error in auth: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def verify_user_access(user_id: str, current_user_id: str):
    """
    Verify that the authenticated user matches the requested user_id.
    
    Args:
        user_id: User ID from URL path
        current_user_id: User ID from JWT token
        
    Raises:
        HTTPException: If user IDs don't match
    """
    if user_id != current_user_id:
        logger.warning(f"User {current_user_id} attempted to access {user_id}'s data")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
        )
