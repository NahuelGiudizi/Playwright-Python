"""
User data models for AutomationExercise testing framework.
"""
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """User model."""
    name: str
    email: str
    password: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    address1: Optional[str] = ""
    address2: Optional[str] = ""
    country: Optional[str] = ""
    state: Optional[str] = ""
    city: Optional[str] = ""
    zipcode: Optional[str] = ""
    mobile_number: Optional[str] = ""


class LoginRequest(BaseModel):
    """Login request model."""
    email: str
    password: str


class LoginResponse(BaseModel):
    """Login response model."""
    responseCode: int
    message: str
    user: Optional[User] = None


class CreateAccountRequest(BaseModel):
    """Create account request model."""
    name: str
    email: str
    password: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    address1: Optional[str] = ""
    address2: Optional[str] = ""
    country: Optional[str] = ""
    state: Optional[str] = ""
    city: Optional[str] = ""
    zipcode: Optional[str] = ""
    mobile_number: Optional[str] = ""


class CreateAccountResponse(BaseModel):
    """Create account response model."""
    responseCode: int
    message: str
    user: Optional[User] = None


class DeleteAccountRequest(BaseModel):
    """Delete account request model."""
    email: str
    password: str


class DeleteAccountResponse(BaseModel):
    """Delete account response model."""
    responseCode: int
    message: str


class UpdateAccountRequest(BaseModel):
    """Update account request model."""
    name: str
    email: str
    password: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    address1: Optional[str] = ""
    address2: Optional[str] = ""
    country: Optional[str] = ""
    state: Optional[str] = ""
    city: Optional[str] = ""
    zipcode: Optional[str] = ""
    mobile_number: Optional[str] = ""


class UpdateAccountResponse(BaseModel):
    """Update account response model."""
    responseCode: int
    message: str
    user: Optional[User] = None


class UserDetailResponse(BaseModel):
    """User detail response model."""
    responseCode: int
    user: Optional[User] = None
