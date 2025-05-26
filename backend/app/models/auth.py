from pydantic import BaseModel
from datetime import date

class LoginRequest(BaseModel):
    """
    Request model for user login.

    Attributes:
        user_id (str): Unique identifier for the user.
        birthdate (date): User's birthdate in YYYY-MM-DD format (e.g., 2000-05-21).
    """
    user_id: str
    birthdate: date  # Pydantic will parse and validate this (format: YYYY-MM-DD)

class LoginResponse(BaseModel):
    """
    Response model for user login.
    """
    token: str
    user_id: str
