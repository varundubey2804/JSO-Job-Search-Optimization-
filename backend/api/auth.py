from fastapi import Header, HTTPException, Depends
from typing import Optional

def verify_token(authorization: Optional[str] = Header(None)):
    """
    Mock Access Policy Architecture (APA)
    Verifies that the incoming request has a valid token and role.
    """
    if not authorization:
        # In a real system, we would raise HTTP 401. 
        # For prototype simplicity and testing without a real frontend auth flow, 
        # we bypass strict auth if no header is present, or mock a user.
        return {"user_id": "mock_user_id", "role": "User"}
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    token = parts[1]
    
    # Mock Token Validation
    # In reality, verify JWT via pyjwt
    if token == "mock-admin-token":
        return {"user_id": "admin_123", "role": "Admin"}
    elif token == "mock-hr-token":
        return {"user_id": "hr_123", "role": "HR Consultant"}
    elif token == "mock-user-token":
        return {"user_id": "user_123", "role": "User"}
    elif token == "mock-licensing-token":
        return {"user_id": "license_123", "role": "Licensing Manager"}
    
    # Accept all tokens for the prototype ease of use
    return {"user_id": "guest", "role": "User"}

def require_role(allowed_roles: list):
    """
    Returns a dependency that checks if the user's role is in the allowed list.
    """
    def role_checker(user: dict = Depends(verify_token)):
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker
