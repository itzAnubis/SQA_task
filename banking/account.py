"""Account operations module - handles balance and transfers."""

from banking.models import Transaction, TransactionType
from datetime import datetime


def get_account_balance(accounts_db, account_number):
    """Get the balance of an account.

    Args:
        accounts_db: dictionary of account_number -> Account
        account_number: the account to look up

    Returns:
        tuple: (success, balance_or_error_message)
    """
    if not account_number or account_number.strip() == "":
        return False, "Account number cannot be empty"

    account = accounts_db.get(account_number)
    if account is None:
        return False, "Account not found"

    return True, account.balance


def transfer_money(accounts_db, transactions_list, from_account_num, to_account_num, amount):
    """Transfer money between two accounts.

    Args:
        accounts_db: dictionary of account_number -> Account
        transactions_list: list to append transaction records to
        from_account_num: sender's account number
        to_account_num: receiver's account number
        amount: the amount to transfer

    Returns:
        tuple: (success, message)
    """
    # validate account numbers are provided
    if not from_account_num or from_account_num.strip() == "":
        return False, "Sender account number is required"

    if not to_account_num or to_account_num.strip() == "":
        return False, "Receiver account number is required"

    # check self-transfer
    if from_account_num == to_account_num:
        return False, "Cannot transfer to the same account"

    # validate amount
    if not isinstance(amount, (int, float)):
        return False, "Transfer amount must be a number"

    if amount <= 0:
        return False, "Transfer amount must be greater than zero"

    # check accounts exist
    from_account = accounts_db.get(from_account_num)
    if from_account is None:
        return False, "Sender account not found"

    to_account = accounts_db.get(to_account_num)
    if to_account is None:
        return False, "Receiver account not found"

    # check sufficient balance
    if from_account.balance < amount:
        return False, "Insufficient funds"

    # perform transfer
    from_account.balance -= amount
    to_account.balance += amount

    # record the transaction
    transaction = Transaction(
        transaction_id=len(transactions_list) + 1,
        from_account=from_account_num,
        to_account=to_account_num,
        amount=amount,
        timestamp=datetime.now(),
        transaction_type=TransactionType.TRANSFER
    )
    transactions_list.append(transaction)

    return True, "Transfer successful"


def get_transaction_history(transactions_list, account_number):
    """Get transaction history for a specific account.

    Returns all transactions where the account was sender or receiver,
    ordered by timestamp (newest first).

    Args:
        transactions_list: list of all transactions
        account_number: the account to get history for

    Returns:
        list of Transaction objects
    """
    if not account_number:
        return []

    # filter transactions for this account
    history = [
        t for t in transactions_list
        if t.from_account == account_number or t.to_account == account_number
    ]

    # sort by timestamp, most recent first
    history.sort(key=lambda t: t.timestamp, reverse=True)

    return history
