"""Data models for the banking system."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    """Types of transactions in the system."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"


@dataclass
class User:
    """Represents a bank user/customer."""
    username: str
    password: str
    account_number: str


@dataclass
class Account:
    """Represents a bank account."""
    account_number: str
    owner_username: str
    balance: float = 0.0


@dataclass
class Transaction:
    """Represents a single transaction record."""
    transaction_id: int
    from_account: str
    to_account: str
    amount: float
    timestamp: datetime = field(default_factory=datetime.now)
    transaction_type: TransactionType = TransactionType.TRANSFER
