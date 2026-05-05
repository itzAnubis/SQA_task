# Simple Banking System — SQA Project

A Simple Banking System built in Python for our Software Testing & Quality Assurance course. The project demonstrates how to apply software testing concepts including test design, test execution, and test evaluation.

## Features

- **User Login** — Register and authenticate with username/password
- **View Account Balance** — Check current balance
- **Transfer Money** — Send money to another account
- **Transaction History** — View past transfers
- **Change Password** — Update password with security rules

## Project Structure

```
SQA_task/
├── banking/              # Source code
│   ├── models.py         # Data classes (User, Account, Transaction)
│   ├── auth.py           # Login & password logic
│   ├── account.py        # Balance & transfer logic
│   └── bank.py           # Main BankSystem class
├── tests/                # Automated test cases (32 tests)
│   ├── test_auth.py      # Login & password tests
│   ├── test_account.py   # Balance & transfer tests
│   ├── test_transaction.py  # Transaction history tests
│   └── test_integration.py  # End-to-end tests
├── docs/                 # Deliverables
│   ├── report.md         # Final report
│   └── test_cases.csv    # Test cases spreadsheet
├── pyproject.toml        # Project config
└── run_tests.sh          # Test runner script
```

## How to Run

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Run Tests

```bash
# Option 1: Using the script
bash run_tests.sh

# Option 2: Directly with uv
uv run pytest -v

# Generate HTML report
uv run pytest --html=report.html
```

### Example Output

```
tests/test_auth.py::TestLogin::test_login_valid_credentials PASSED
tests/test_auth.py::TestLogin::test_login_wrong_password PASSED
tests/test_account.py::TestTransferMoney::test_transfer_valid PASSED
...
============================== 32 passed in 0.03s ==============================
```

## Test Summary

| Category | Tests | Status |
|----------|-------|--------|
| Login | 5 | ✅ All Pass |
| Change Password | 6 | ✅ All Pass |
| View Balance | 2 | ✅ All Pass |
| Transfer Money | 8 | ✅ All Pass |
| Transaction History | 6 | ✅ All Pass |
| Integration | 5 | ✅ All Pass |
| **Total** | **32** | **100% Pass** |

## Tools Used

- **Python 3.12** — Programming language
- **pytest** — Test framework
- **uv** — Package manager & test runner
- **pytest-html** — HTML test report generation
