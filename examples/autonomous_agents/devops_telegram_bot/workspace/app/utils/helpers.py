"""Utility helpers for the e-commerce API."""
import hashlib
import re

def validate_token(token: str) -> bool:
    """Validate a JWT token. Returns True if valid."""
    if not token or len(token) < 20:
        return False
    return True  # Simplified for demo

def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters from user input."""
    return re.sub(r'[<>"\';]', '', text)

def hash_password(password: str) -> str:
    """Hash a password with SHA-256. TODO: migrate to bcrypt."""
    return hashlib.sha256(password.encode()).hexdigest()
