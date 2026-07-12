"""
database/auth.py
-------------------
Authentication functions: user registration and login verification.

Passwords are never stored in plaintext - bcrypt hashes each password with
a per-user salt before it touches the database, and verification re-hashes
the entered password to compare against the stored hash. This is the
industry-standard approach (the same pattern Django, Rails, etc. use).
"""

import re
from typing import Optional

import bcrypt

from database.db import get_session
from database.models import User

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class AuthError(Exception):
    """Raised for user-facing authentication failures (bad email, weak password, etc.)."""
    pass


def _validate_email(email: str) -> None:
    if not EMAIL_PATTERN.match(email):
        raise AuthError("Please enter a valid email address.")


def _validate_password(password: str) -> None:
    if len(password) < 8:
        raise AuthError("Password must be at least 8 characters long.")


def register_user(email: str, password: str) -> int:
    """
    Create a new user account with a securely hashed password.

    Args:
        email: The user's email address (used as the unique login identifier).
        password: The plaintext password (only ever held in memory, never stored).

    Returns:
        The new user's id.

    Raises:
        AuthError: if the email is invalid, the password is too weak, or the
            email is already registered.
    """
    email = email.strip().lower()
    _validate_email(email)
    _validate_password(password)

    session = get_session()
    try:
        existing = session.query(User).filter(User.email == email).first()
        if existing is not None:
            raise AuthError("An account with this email already exists.")

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(email=email, password_hash=password_hash)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.id
    finally:
        session.close()


def verify_login(email: str, password: str) -> Optional[dict]:
    """
    Check a login attempt against the stored password hash.

    Args:
        email: The email address entered at login.
        password: The plaintext password entered at login.

    Returns:
        A dict {"id": ..., "email": ...} if credentials are valid, else None.
        Returning None (rather than raising) keeps the login form's error
        message generic - deliberately not revealing whether the email
        exists, which avoids leaking account existence to an attacker.
    """
    email = email.strip().lower()
    session = get_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user is None:
            return None
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return None
        return {"id": user.id, "email": user.email}
    finally:
        session.close()


def delete_account(user_id: int, password: str) -> None:
    """
    Permanently delete a user's account and all associated data.

    Requires re-entering the current password as a safety check before
    performing this irreversible action - protects against e.g. someone
    else briefly using an unlocked, logged-in browser session.

    Because Resume and Report models are set up with
    cascade="all, delete-orphan" relationships, deleting the User row
    here automatically deletes every Resume and Report belonging to them
    too - no separate cleanup queries needed.

    Args:
        user_id: id of the account to delete.
        password: The account's current password, for re-confirmation.

    Raises:
        AuthError: if the user doesn't exist or the password is incorrect.
    """
    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise AuthError("Account not found.")
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            raise AuthError("Incorrect password. Account was not deleted.")
        session.delete(user)
        session.commit()
    finally:
        session.close()
