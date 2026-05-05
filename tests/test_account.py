"""Tests for account operations (balance and transfers)."""

import pytest
from banking.bank import BankSystem


@pytest.fixture
def bank():
    """Create a bank system with two users for transfer testing."""
    system = BankSystem()
    system.register_user("ahmed", "Ahmed123!")
    system.register_user("sara", "Sara5678!")
    return system


def _get_account_num(bank, username):
    """Helper to get account number for a user."""
    user = bank.get_user(username)
    return user.account_number


class TestViewBalance:
    """Test cases for the view balance feature."""

    def test_view_balance_existing_user(self, bank):
        """TC-12: Check balance of a registered user (initial balance = 1000)."""
        success, balance = bank.get_balance("ahmed")
        assert success is True
        assert balance == 1000.0

    def test_view_balance_nonexistent_user(self, bank):
        """TC-13: Check balance of a user that doesn't exist."""
        success, msg = bank.get_balance("unknown_user")
        assert success is False


class TestTransferMoney:
    """Test cases for the money transfer feature."""

    def test_transfer_valid(self, bank):
        """TC-14: Transfer a valid amount between two accounts."""
        to_acc = _get_account_num(bank, "sara")
        success, msg = bank.transfer("ahmed", to_acc, 200.0)
        assert success is True
        assert "successful" in msg.lower()

    def test_transfer_insufficient_funds(self, bank):
        """TC-15: Transfer more money than the sender has."""
        to_acc = _get_account_num(bank, "sara")
        success, msg = bank.transfer("ahmed", to_acc, 5000.0)
        assert success is False
        assert "Insufficient" in msg

    def test_transfer_negative_amount(self, bank):
        """TC-16: Transfer a negative amount."""
        to_acc = _get_account_num(bank, "sara")
        success, msg = bank.transfer("ahmed", to_acc, -100.0)
        assert success is False
        assert "greater than zero" in msg

    def test_transfer_zero_amount(self, bank):
        """TC-17: Transfer zero amount."""
        to_acc = _get_account_num(bank, "sara")
        success, msg = bank.transfer("ahmed", to_acc, 0)
        assert success is False
        assert "greater than zero" in msg

    def test_transfer_to_nonexistent_account(self, bank):
        """TC-18: Transfer to an account number that doesn't exist."""
        success, msg = bank.transfer("ahmed", "ACC9999", 100.0)
        assert success is False
        assert "not found" in msg.lower()

    def test_transfer_self_transfer(self, bank):
        """TC-19: Transfer money to the same account (self-transfer)."""
        own_acc = _get_account_num(bank, "ahmed")
        success, msg = bank.transfer("ahmed", own_acc, 100.0)
        assert success is False
        assert "same account" in msg.lower()

    def test_balance_after_transfer(self, bank):
        """TC-20: Verify both balances update correctly after transfer."""
        to_acc = _get_account_num(bank, "sara")
        bank.transfer("ahmed", to_acc, 300.0)

        _, sender_bal = bank.get_balance("ahmed")
        _, receiver_bal = bank.get_balance("sara")

        assert sender_bal == 700.0
        assert receiver_bal == 1300.0

    def test_transfer_exact_balance(self, bank):
        """TC-21: Transfer the exact full balance."""
        to_acc = _get_account_num(bank, "sara")
        success, msg = bank.transfer("ahmed", to_acc, 1000.0)
        assert success is True

        _, sender_bal = bank.get_balance("ahmed")
        assert sender_bal == 0.0
