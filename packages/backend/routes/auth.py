from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from backend.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, JWT_SECRET
from backend.services import d1
import jwt
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])

oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    return encoded_jwt

@router.get("/sign-up")
async def signup_oauth(request: Request):
    """
    Redirects to Google OAuth for registration.
    """
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI, state="signup")

@router.get("/sign-in")
async def signin_oauth(email: str, request: Request):
    """
    Checks if user exists, then redirects to Google OAuth for login.
    """
    user = await d1.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please sign up first.")
    
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI, state="login")

@router.get("/callback")
async def auth_callback(request: Request):
    """
    Handles Google OAuth callback.
    """
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info from Google")
    
    email = user_info.get('email')
    name = user_info.get('name')
    picture = user_info.get('picture')
    
    state = request.query_params.get('state')
    
    user = await d1.get_user_by_email(email)
    
    if state == "signup":
        if not user:
            user = await d1.create_user(email=email, full_name=name, picture=picture)
    elif state == "login":
        if not user:
            # This shouldn't happen if sign-in-oauth checked, but for safety:
            raise HTTPException(status_code=404, detail="User not found.")
    
    # Generate JWT
    access_token = create_access_token(data={"sub": user['id'], "email": user['email']})
    
    from fastapi.responses import JSONResponse
    
    response = JSONResponse(content={
        "message": "Authentication successful",
        "user": user
    })
    
    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days
        expires=7 * 24 * 60 * 60,
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
    )
    
    return response
