"""Authentication module - handles login and password operations."""

import re


def validate_password_complexity(password):
    """Check if a password meets the complexity requirements.

    Rules:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one digit
        - Cannot be empty or whitespace-only

    Returns:
        tuple: (is_valid, error_message)
    """
    if not password or password.strip() == "":
        return False, "Password cannot be empty"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"

    return True, ""


def authenticate_user(users_db, username, password):
    """Authenticate a user with username and password.

    Args:
        users_db: dictionary of username -> User objects
        username: the username to look up
        password: the password to check

    Returns:
        User object if successful, None otherwise
    """
    if not username or username.strip() == "":
        return None

    if not password or password.strip() == "":
        return None

    user = users_db.get(username)
    if user is None:
        return None

    if user.password != password:
        return None

    return user


def change_user_password(users_db, username, old_password, new_password):
    """Change a user's password.

    Args:
        users_db: dictionary of username -> User objects
        username: the user whose password to change
        old_password: current password for verification
        new_password: the new password to set

    Returns:
        tuple: (success, message)
    """
    # first verify the user exists and old password is correct
    user = authenticate_user(users_db, username, old_password)
    if user is None:
        return False, "Authentication failed - wrong username or password"

    # check that new password is different from old
    if old_password == new_password:
        return False, "New password must be different from old password"

    # validate new password complexity
    is_valid, error_msg = validate_password_complexity(new_password)
    if not is_valid:
        return False, error_msg

    # update the password
    user.password = new_password
    return True, "Password changed successfully"
