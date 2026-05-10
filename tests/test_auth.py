"""Tests for the authentication module (login & password change)."""

import pytest
from banking.bank import BankSystem


@pytest.fixture
def bank():
    """Create a bank system with a test user already registered."""
    system = BankSystem()
    system.register_user("ahmed", "Ahmed123!")
    system.register_user("sara", "Sara5678!")
    return system


# --- Login Tests ---

class TestLogin:
    """Test cases for the login feature."""

    def test_login_valid_credentials(self, bank):
        """TC-01: Login with correct username and password."""
        success, msg = bank.login("ahmed", "Ahmed123!")
        assert success is True
        assert "Welcome" in msg

    def test_login_wrong_password(self, bank):
        """TC-02: Login with wrong password should fail."""
        success, msg = bank.login("ahmed", "WrongPass1")
        assert success is False
        assert "Invalid" in msg

    def test_login_nonexistent_user(self, bank):
        """TC-03: Login with a username that doesn't exist."""
        success, msg = bank.login("ghost_user", "SomePass1")
        assert success is False
        assert "Invalid" in msg

    def test_login_empty_username(self, bank):
        """TC-04: Login with empty username."""
        success, msg = bank.login("", "Ahmed123!")
        assert success is False

    def test_login_empty_password(self, bank):
        """TC-05: Login with empty password."""
        success, msg = bank.login("ahmed", "")
        assert success is False


# --- Change Password Tests ---

class TestChangePassword:
    """Test cases for the change password feature."""

    def test_change_password_success(self, bank):
        """TC-06: Change password with valid old and new password."""
        success, msg = bank.change_password("ahmed", "Ahmed123!", "NewPass99!")
        assert success is True
        assert "successfully" in msg.lower()

        # verify login works with new password
        success2, _ = bank.login("ahmed", "NewPass99!")
        assert success2 is True

    def test_change_password_wrong_old(self, bank):
        """TC-07: Change password with wrong old password."""
        success, msg = bank.change_password("ahmed", "WrongOld1", "NewPass99!")
        assert success is False
        assert "Authentication failed" in msg

    def test_change_password_weak_new(self, bank):
        """TC-08: Change password to a weak password (too short)."""
        success, msg = bank.change_password("ahmed", "Ahmed123!", "short")
        assert success is False
        assert "8 characters" in msg

    def test_change_password_no_uppercase(self, bank):
        """TC-09: New password without uppercase letter."""
        success, msg = bank.change_password("ahmed", "Ahmed123!", "alllower1")
        assert success is False
        assert "uppercase" in msg

    def test_change_password_no_digit(self, bank):
        """TC-10: New password without any digit."""
        success, msg = bank.change_password("ahmed", "Ahmed123!", "NoDigitHere")
        assert success is False
        assert "digit" in msg

    def test_change_password_same_as_old(self, bank):
        """TC-11: New password same as old password."""
        success, msg = bank.change_password("ahmed", "Ahmed123!", "Ahmed123!")
        assert success is False
        assert "different" in msg.lower()

    def test_login_case_sensitive_password(self, bank):
        """TC-47: Password should be case sensitive."""
        success, msg = bank.login("ahmed", "ahmed123!")
        assert success is False
        assert "Invalid" in msg

    def test_login_case_sensitive_username(self, bank):
        """TC-48: Username should be case sensitive (if applicable) or test different casing."""
        success, msg = bank.login("Ahmed", "Ahmed123!")
        assert success is False
        assert "Invalid" in msg
