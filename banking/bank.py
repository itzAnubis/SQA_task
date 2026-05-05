"""Main Bank System class - ties all modules together."""

from banking.models import User, Account
from banking.auth import authenticate_user, change_user_password, validate_password_complexity
from banking.account import get_account_balance, transfer_money, get_transaction_history


class BankSystem:
    """Main class that manages the banking system.

    Provides a simple interface for all banking operations:
    register, login, check balance, transfer money, view history,
    and change password.
    """

    def __init__(self):
        """Initialize the bank system with empty storage."""
        self._users = {}          # username -> User
        self._accounts = {}       # account_number -> Account
        self._transactions = []   # list of Transaction
        self._next_account = 1001 # auto-increment account numbers
        self._logged_in_user = None

    def register_user(self, username, password):
        """Register a new user and create their account.

        Args:
            username: desired username (must be unique)
            password: password (must meet complexity rules)

        Returns:
            tuple: (success, message)
        """
        if not username or username.strip() == "":
            return False, "Username cannot be empty"

        if username in self._users:
            return False, "Username already exists"

        # validate password
        is_valid, error_msg = validate_password_complexity(password)
        if not is_valid:
            return False, error_msg

        # create account number
        account_number = f"ACC{self._next_account}"
        self._next_account += 1

        # create user and account
        user = User(username=username, password=password, account_number=account_number)
        account = Account(account_number=account_number, owner_username=username, balance=1000.0)

        self._users[username] = user
        self._accounts[account_number] = account

        return True, f"Registration successful. Account number: {account_number}"

    def login(self, username, password):
        """Log in a user.

        Args:
            username: the username
            password: the password

        Returns:
            tuple: (success, message)
        """
        user = authenticate_user(self._users, username, password)
        if user is None:
            return False, "Invalid username or password"

        self._logged_in_user = user
        return True, f"Welcome, {username}!"

    def logout(self):
        """Log out the current user."""
        self._logged_in_user = None

    def get_balance(self, username):
        """Get account balance for a user.

        Args:
            username: the user whose balance to check

        Returns:
            tuple: (success, balance_or_error)
        """
        user = self._users.get(username)
        if user is None:
            return False, "User not found"

        return get_account_balance(self._accounts, user.account_number)

    def transfer(self, from_username, to_account_number, amount):
        """Transfer money from one user's account to another account.

        Args:
            from_username: the sender's username
            to_account_number: the receiver's account number
            amount: how much to transfer

        Returns:
            tuple: (success, message)
        """
        sender = self._users.get(from_username)
        if sender is None:
            return False, "Sender user not found"

        return transfer_money(
            self._accounts,
            self._transactions,
            sender.account_number,
            to_account_number,
            amount
        )

    def get_transaction_history(self, username):
        """Get transaction history for a user.

        Args:
            username: the user whose history to fetch

        Returns:
            list of Transaction objects (could be empty)
        """
        user = self._users.get(username)
        if user is None:
            return []

        return get_transaction_history(self._transactions, user.account_number)

    def change_password(self, username, old_password, new_password):
        """Change a user's password.

        Args:
            username: whose password to change
            old_password: current password
            new_password: new password

        Returns:
            tuple: (success, message)
        """
        return change_user_password(self._users, username, old_password, new_password)

    def get_user(self, username):
        """Get a user by username (for testing/internal use)."""
        return self._users.get(username)

    def get_account(self, account_number):
        """Get an account by number (for testing/internal use)."""
        return self._accounts.get(account_number)
