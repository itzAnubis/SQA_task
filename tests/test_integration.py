"""Integration tests - end-to-end scenarios combining multiple features."""

import pytest
from banking.bank import BankSystem


@pytest.fixture
def bank():
    """Fresh bank system for each test."""
    return BankSystem()


class TestIntegration:
    """End-to-end integration test scenarios."""

    def test_full_flow_register_login_transfer_history(self, bank):
        """TC-28: Complete flow - register, login, transfer, check history."""
        # Register two users
        bank.register_user("ahmed", "Ahmed123!")
        bank.register_user("sara", "Sara5678!")

        # Login
        success, _ = bank.login("ahmed", "Ahmed123!")
        assert success is True

        # Transfer
        sara_acc = bank.get_user("sara").account_number
        success, _ = bank.transfer("ahmed", sara_acc, 250.0)
        assert success is True

        # Check history
        history = bank.get_transaction_history("ahmed")
        assert len(history) == 1
        assert history[0].amount == 250.0

        # Check balances
        _, ahmed_bal = bank.get_balance("ahmed")
        _, sara_bal = bank.get_balance("sara")
        assert ahmed_bal == 750.0
        assert sara_bal == 1250.0

    def test_login_change_password_login_again(self, bank):
        """TC-29: Login, change password, then login with new password."""
        bank.register_user("ahmed", "Ahmed123!")

        # Login with original password
        success, _ = bank.login("ahmed", "Ahmed123!")
        assert success is True

        # Change password
        success, _ = bank.change_password("ahmed", "Ahmed123!", "NewPass99!")
        assert success is True

        # Old password should no longer work
        success, _ = bank.login("ahmed", "Ahmed123!")
        assert success is False

        # New password should work
        success, _ = bank.login("ahmed", "NewPass99!")
        assert success is True

    def test_multiple_transfers_verify_balances(self, bank):
        """TC-30: Multiple transfers between users, verify final balances."""
        bank.register_user("ahmed", "Ahmed123!")
        bank.register_user("sara", "Sara5678!")

        ahmed_acc = bank.get_user("ahmed").account_number
        sara_acc = bank.get_user("sara").account_number

        # ahmed sends 200 to sara
        bank.transfer("ahmed", sara_acc, 200.0)
        # sara sends 100 back to ahmed
        bank.transfer("sara", ahmed_acc, 100.0)
        # ahmed sends 300 to sara
        bank.transfer("ahmed", sara_acc, 300.0)

        # ahmed: 1000 - 200 + 100 - 300 = 600
        # sara: 1000 + 200 - 100 + 300 = 1400
        _, ahmed_bal = bank.get_balance("ahmed")
        _, sara_bal = bank.get_balance("sara")
        assert ahmed_bal == 600.0
        assert sara_bal == 1400.0

    def test_register_duplicate_username(self, bank):
        """TC-31: Trying to register with an existing username should fail."""
        bank.register_user("ahmed", "Ahmed123!")
        success, msg = bank.register_user("ahmed", "OtherPass1!")
        assert success is False
        assert "already exists" in msg.lower()

    def test_transfer_from_nonexistent_user(self, bank):
        """TC-32: Transfer from a user that doesn't exist."""
        bank.register_user("sara", "Sara5678!")
        sara_acc = bank.get_user("sara").account_number

        success, msg = bank.transfer("ghost", sara_acc, 100.0)
        assert success is False
        assert "not found" in msg.lower()

    def test_three_way_transfer(self, bank):
        """TC-45: 3-way transfer (A -> B -> C)."""
        bank.register_user("ahmed", "Ahmed123!")
        bank.register_user("sara", "Sara5678!")
        bank.register_user("khaled", "Khaled999!")

        sara_acc = bank.get_user("sara").account_number
        khaled_acc = bank.get_user("khaled").account_number

        # Ahmed sends 500 to Sara
        success1, _ = bank.transfer("ahmed", sara_acc, 500.0)
        assert success1 is True

        # Sara sends 300 to Khaled
        success2, _ = bank.transfer("sara", khaled_acc, 300.0)
        assert success2 is True

        _, ahmed_bal = bank.get_balance("ahmed")
        _, sara_bal = bank.get_balance("sara")
        _, khaled_bal = bank.get_balance("khaled")

        assert ahmed_bal == 500.0   # 1000 - 500
        assert sara_bal == 1200.0   # 1000 + 500 - 300
        assert khaled_bal == 1300.0 # 1000 + 300

    def test_circular_transfer(self, bank):
        """TC-46: Circular transfer (A -> B -> C -> A)."""
        bank.register_user("ahmed", "Ahmed123!")
        bank.register_user("sara", "Sara5678!")
        bank.register_user("khaled", "Khaled999!")

        ahmed_acc = bank.get_user("ahmed").account_number
        sara_acc = bank.get_user("sara").account_number
        khaled_acc = bank.get_user("khaled").account_number

        bank.transfer("ahmed", sara_acc, 100.0)
        bank.transfer("sara", khaled_acc, 100.0)
        bank.transfer("khaled", ahmed_acc, 100.0)

        _, ahmed_bal = bank.get_balance("ahmed")
        _, sara_bal = bank.get_balance("sara")
        _, khaled_bal = bank.get_balance("khaled")

        # Balances should be unchanged
        assert ahmed_bal == 1000.0
        assert sara_bal == 1000.0
        assert khaled_bal == 1000.0
