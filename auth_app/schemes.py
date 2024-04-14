from typing import Optional

from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: int
    expires_at: int


class LoginPayload(BaseModel):
    email: str
    password: str


class SignupPayload(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str
    role: int = 1


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str]
