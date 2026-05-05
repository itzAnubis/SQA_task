"""Tests for transaction history feature."""

import pytest
from banking.bank import BankSystem


@pytest.fixture
def bank():
    """Create a bank system with two users."""
    system = BankSystem()
    system.register_user("ahmed", "Ahmed123!")
    system.register_user("sara", "Sara5678!")
    return system


def _get_account_num(bank, username):
    """Helper to get account number for a user."""
    user = bank.get_user(username)
    return user.account_number


class TestTransactionHistory:
    """Test cases for the transaction history feature."""

    def test_empty_history(self, bank):
        """TC-22: View history when no transactions have been made."""
        history = bank.get_transaction_history("ahmed")
        assert len(history) == 0

    def test_history_after_one_transfer(self, bank):
        """TC-23: History should show one entry after one transfer."""
        to_acc = _get_account_num(bank, "sara")
        bank.transfer("ahmed", to_acc, 150.0)

        history = bank.get_transaction_history("ahmed")
        assert len(history) == 1
        assert history[0].amount == 150.0

    def test_history_after_multiple_transfers(self, bank):
        """TC-24: History should show all transfers for the user."""
        to_acc = _get_account_num(bank, "sara")
        bank.transfer("ahmed", to_acc, 100.0)
        bank.transfer("ahmed", to_acc, 200.0)
        bank.transfer("ahmed", to_acc, 50.0)

        history = bank.get_transaction_history("ahmed")
        assert len(history) == 3

    def test_history_correct_amounts(self, bank):
        """TC-25: Verify transaction amounts in history are accurate."""
        to_acc = _get_account_num(bank, "sara")
        bank.transfer("ahmed", to_acc, 100.0)
        bank.transfer("ahmed", to_acc, 250.0)

        history = bank.get_transaction_history("ahmed")
        amounts = [t.amount for t in history]
        assert 100.0 in amounts
        assert 250.0 in amounts

    def test_history_shows_for_receiver(self, bank):
        """TC-26: Receiver should also see the transfer in their history."""
        to_acc = _get_account_num(bank, "sara")
        bank.transfer("ahmed", to_acc, 300.0)

        sara_history = bank.get_transaction_history("sara")
        assert len(sara_history) == 1
        assert sara_history[0].amount == 300.0

    def test_history_nonexistent_user(self, bank):
        """TC-27: Getting history for non-existent user returns empty."""
        history = bank.get_transaction_history("ghost")
        assert len(history) == 0
