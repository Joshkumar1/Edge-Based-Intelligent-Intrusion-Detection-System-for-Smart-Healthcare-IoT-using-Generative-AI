from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, get_db
from app.core.security import decode_access_token
from app.models.user import User

# Bearer security scheme - does not auto-raise so we can provide structured, precise 401 error details
http_bearer = HTTPBearer(auto_error=False)

# Role definitions
ROLE_ADMIN = "hospital_admin"
ROLE_OPERATOR = "security_operator"
ROLE_ANALYST = "security_analyst"
ROLE_BIOMED = "biomedical_engineer"
ROLE_AUDITOR = "read_only_auditor"

CONTAINMENT_PERMITTED_ROLES = {
    ROLE_ADMIN,
    ROLE_OPERATOR,
    ROLE_BIOMED,
    "admin"  # Support legacy admin role name
}

TRIAGE_PERMITTED_ROLES = {
    ROLE_ADMIN,
    ROLE_OPERATOR,
    ROLE_ANALYST,
    ROLE_BIOMED,
    "admin"
}


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
    db: Session = Depends(get_db)
) -> User:
    """
    Validates JWT Bearer token and resolves active user identity.
    Rejects missing, expired, or tampered tokens with HTTP 401.
    Never silently falls back to admin.
    """
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please supply a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = credentials.credentials.strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Empty or malformed Bearer token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        payload = decode_access_token(token)
        username: Optional[str] = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token validation failed: subject ('sub') claim missing.",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired. Please re-authenticate.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token signature verification failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User identity associated with token does not exist.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is deactivated. Contact hospital security administrator.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Verifies that the authenticated user account is active."""
    return current_user


def require_containment_privilege(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Authorization policy: restricts network containment & isolation operations
    strictly to hospital security operators, biomedical engineers, and admins.
    Rejects read-only or unauthorized users with HTTP 403.
    """
    if current_user.role not in CONTAINMENT_PERMITTED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"Access Denied: User '{current_user.username}' (role: '{current_user.role}') "
                f"lacks network containment authorization. "
                f"Permitted roles: {sorted(list(CONTAINMENT_PERMITTED_ROLES))}"
            )
        )
    return current_user


def require_triage_privilege(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Authorization policy: restricts alert status modifications and incident triage.
    """
    if current_user.role not in TRIAGE_PERMITTED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"Access Denied: User '{current_user.username}' (role: '{current_user.role}') "
                f"lacks incident triage authorization."
            )
        )
    return current_user
