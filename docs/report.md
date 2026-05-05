# Simple Banking System — Software Testing & Quality Assurance Report

## 1. Scope & Requirements

### 1.1 System Scope

This project is a Simple Banking System built in Python. It's a console-based application that handles basic banking operations. We chose to keep it simple because the main goal here is testing, not building a full banking app. The system uses in-memory storage (Python dictionaries), meaning data resets every time the program runs.

The system covers five core features:
- User Login (authentication)
- View Account Balance
- Transfer Money between accounts
- Transaction History viewing
- Change Password

### 1.2 Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-01 | The system shall allow users to register with a unique username and password |
| FR-02 | The system shall authenticate users using username and password |
| FR-03 | The system shall reject login attempts with wrong credentials |
| FR-04 | The system shall display the current account balance for a logged-in user |
| FR-05 | The system shall allow transferring money to another account if the sender has enough balance |
| FR-06 | The system shall prevent transfers with invalid amounts (negative, zero) |
| FR-07 | The system shall prevent self-transfers (transferring to your own account) |
| FR-08 | The system shall keep a record of all transactions (transfer history) |
| FR-09 | The system shall allow users to change their password after verifying the old one |
| FR-10 | The system shall enforce password complexity rules (min 8 characters, at least 1 uppercase, at least 1 digit) |

### 1.3 Success Criteria

The system is considered successful if:
- All registered users can log in with correct credentials
- Users are prevented from logging in with wrong credentials
- Money transfers work correctly and both balances update properly
- Invalid operations (negative transfer, self-transfer, insufficient funds) are blocked with clear error messages
- Transaction history accurately shows all past transfers
- Password changes go through only when the old password is correct and the new one meets the rules

---

## 2. Quality Factors

We picked 5 quality factors that are relevant to a banking system and applied each one to our project.

### 2.1 Correctness

**Definition:** The system produces the right output for every valid input.

**Application:** When a user transfers 200 EGP from Account A (balance: 1000) to Account B (balance: 1000), Account A should have 800 and Account B should have 1200. No money should be created or lost. We tested this in TC-20 and TC-30 to make sure the math is always right.

### 2.2 Reliability

**Definition:** The system performs consistently without crashing, even when given bad input.

**Application:** If someone tries to transfer a negative amount or transfer to an account that doesn't exist, the system shouldn't crash. It should just return an error message. We tested all these edge cases (TC-16, TC-17, TC-18) and the system handled them without any exceptions or crashes.

### 2.3 Security

**Definition:** The system protects user data and prevents unauthorized access.

**Application:** Our system enforces password complexity (must have uppercase + digit + 8 chars minimum). Login with wrong credentials is always rejected. Passwords can only be changed if the user proves they know the old one first. We covered this in TC-02, TC-03, TC-07, TC-08, TC-09, TC-10.

### 2.4 Usability

**Definition:** The system is easy to understand and use.

**Application:** Every operation returns a clear success/failure message. For example, if a transfer fails because of insufficient funds, the message says "Insufficient funds" — not some random error code. The functions have simple names like `login()`, `transfer()`, `get_balance()` so the code is easy to read.

### 2.5 Maintainability

**Definition:** The code is easy to modify and extend in the future.

**Application:** We separated the code into modules: `auth.py` for login stuff, `account.py` for balance/transfer, `models.py` for data classes, and `bank.py` as the main controller. If we need to add a new feature (like deposits), we just add it to `account.py` without touching the login code. Each function does one thing, which makes bugs easier to find and fix.

---

## 3. Test Design

### 3.1 Test Strategy

We used automated testing with **pytest** to make sure all our test cases run consistently every time. The tests are organized by feature:

- `test_auth.py` — Login and password tests
- `test_account.py` — Balance and transfer tests
- `test_transaction.py` — Transaction history tests
- `test_integration.py` — End-to-end flow tests

### 3.2 Testing Techniques Used

**Equivalence Partitioning:** We divided inputs into valid and invalid groups. For example, for the login feature:
- Valid: correct username + correct password
- Invalid: wrong password, non-existent user, empty fields

**Boundary Value Analysis:** We tested boundary conditions for transfers:
- Transfer exactly 0 (should fail — boundary)
- Transfer exactly the full balance (should succeed — boundary)
- Transfer more than the balance (should fail)

**Negative Testing:** We intentionally provided wrong inputs to make sure the system handles them correctly:
- Empty username/password
- Self-transfer
- Weak passwords (no digit, no uppercase, too short)

### 3.3 Test Environment

- **Language:** Python 3.12
- **Test Framework:** pytest 9.0
- **Package Manager:** uv
- **Test Runner Command:** `uv run pytest -v`

---

## 4. Test Execution

We executed 32 test cases covering all five features. Here's the full execution table:

### Login Tests

| Test ID | Scenario | Input | Expected Output | Actual Output | Status |
|---------|----------|-------|-----------------|---------------|--------|
| TC-01 | Login with valid credentials | username="ahmed", password="Ahmed123!" | Success, welcome message | Success, "Welcome, ahmed!" | ✅ Pass |
| TC-02 | Login with wrong password | username="ahmed", password="WrongPass1" | Failure, invalid credentials | Failure, "Invalid username or password" | ✅ Pass |
| TC-03 | Login with non-existent user | username="ghost_user", password="SomePass1" | Failure, invalid credentials | Failure, "Invalid username or password" | ✅ Pass |
| TC-04 | Login with empty username | username="", password="Ahmed123!" | Failure | Failure, "Invalid username or password" | ✅ Pass |
| TC-05 | Login with empty password | username="ahmed", password="" | Failure | Failure, "Invalid username or password" | ✅ Pass |

### Change Password Tests

| Test ID | Scenario | Input | Expected Output | Actual Output | Status |
|---------|----------|-------|-----------------|---------------|--------|
| TC-06 | Change password successfully | old="Ahmed123!", new="NewPass99!" | Success | Success, "Password changed successfully" | ✅ Pass |
| TC-07 | Wrong old password | old="WrongOld1", new="NewPass99!" | Failure, auth failed | Failure, "Authentication failed" | ✅ Pass |
| TC-08 | New password too short | old="Ahmed123!", new="short" | Failure, too short | Failure, "must be at least 8 characters" | ✅ Pass |
| TC-09 | No uppercase in new password | old="Ahmed123!", new="alllower1" | Failure, no uppercase | Failure, "must contain uppercase" | ✅ Pass |
| TC-10 | No digit in new password | old="Ahmed123!", new="NoDigitHere" | Failure, no digit | Failure, "must contain digit" | ✅ Pass |
| TC-11 | Same as old password | old="Ahmed123!", new="Ahmed123!" | Failure, must be different | Failure, "must be different from old" | ✅ Pass |

### View Balance Tests

| Test ID | Scenario | Input | Expected Output | Actual Output | Status |
|---------|----------|-------|-----------------|---------------|--------|
| TC-12 | View balance of existing user | username="ahmed" | Success, balance=1000.0 | Success, 1000.0 | ✅ Pass |
| TC-13 | View balance of non-existent user | username="unknown_user" | Failure | Failure, "User not found" | ✅ Pass |

### Transfer Tests

| Test ID | Scenario | Input | Expected Output | Actual Output | Status |
|---------|----------|-------|-----------------|---------------|--------|
| TC-14 | Valid transfer | from="ahmed", amount=200.0 | Success | Success, "Transfer successful" | ✅ Pass |
| TC-15 | Transfer with insufficient funds | from="ahmed", amount=5000.0 | Failure, insufficient | Failure, "Insufficient funds" | ✅ Pass |
| TC-16 | Transfer negative amount | from="ahmed", amount=-100.0 | Failure, invalid amount | Failure, "must be greater than zero" | ✅ Pass |
| TC-17 | Transfer zero amount | from="ahmed", amount=0 | Failure, invalid amount | Failure, "must be greater than zero" | ✅ Pass |
| TC-18 | Transfer to non-existent account | to="ACC9999", amount=100.0 | Failure, not found | Failure, "Receiver account not found" | ✅ Pass |
| TC-19 | Self-transfer | from="ahmed", to=ahmed's account | Failure, same account | Failure, "Cannot transfer to same account" | ✅ Pass |
| TC-20 | Check balances after transfer | transfer 300 from ahmed to sara | ahmed=700, sara=1300 | ahmed=700.0, sara=1300.0 | ✅ Pass |
| TC-21 | Transfer exact full balance | from="ahmed", amount=1000.0 | Success, sender balance=0 | Success, balance=0.0 | ✅ Pass |

### Transaction History Tests

| Test ID | Scenario | Input | Expected Output | Actual Output | Status |
|---------|----------|-------|-----------------|---------------|--------|
| TC-22 | Empty history (no transfers) | username="ahmed" | Empty list | [] (length 0) | ✅ Pass |
| TC-23 | History after one transfer | 1 transfer of 150 | 1 entry, amount=150 | 1 entry, amount=150.0 | ✅ Pass |
| TC-24 | History after multiple transfers | 3 transfers | 3 entries | 3 entries | ✅ Pass |
| TC-25 | Verify correct amounts in history | transfers of 100, 250 | Both amounts present | 100.0 and 250.0 found | ✅ Pass |
| TC-26 | Receiver sees transfer in history | ahmed sends 300 to sara | sara's history has 1 entry | 1 entry, amount=300.0 | ✅ Pass |
| TC-27 | History for non-existent user | username="ghost" | Empty list | [] (length 0) | ✅ Pass |

### Integration Tests

| Test ID | Scenario | Input | Expected Output | Actual Output | Status |
|---------|----------|-------|-----------------|---------------|--------|
| TC-28 | Full flow: register → login → transfer → history | Complete flow | All steps succeed, balances correct | All passed, ahmed=750, sara=1250 | ✅ Pass |
| TC-29 | Login → change password → login again | Change pw then re-login | Old pw fails, new pw works | Old pw rejected, new pw accepted | ✅ Pass |
| TC-30 | Multiple transfers, verify balances | 3 transfers back and forth | ahmed=600, sara=1400 | ahmed=600.0, sara=1400.0 | ✅ Pass |
| TC-31 | Register duplicate username | Register "ahmed" twice | Failure, already exists | Failure, "Username already exists" | ✅ Pass |
| TC-32 | Transfer from non-existent user | from="ghost" | Failure, not found | Failure, "Sender user not found" | ✅ Pass |

### Summary

- **Total Test Cases:** 32
- **Passed:** 32
- **Failed:** 0
- **Pass Rate:** 100%

---

## 5. Test Evaluation

### 5.1 Results Analysis

All 32 test cases passed successfully. The system handled both valid and invalid inputs correctly. No failures were found during testing.

Since all tests passed, there were no bugs to report. However, during the development process (before we finished implementing all validation checks), we did encounter some issues that our tests helped us catch early.

### 5.2 Example of Error, Fault, and Failure

To explain the concepts, here's a scenario we ran into while building the system:

**Error (Human Mistake):**
During development, we initially forgot to check for self-transfers. We assumed users wouldn't try to transfer to their own account, but that was a wrong assumption.

**Fault (Bug in Code):**
Because of this error, the `transfer_money()` function didn't have a check for `from_account == to_account`. This means the code had a defect — it would accept self-transfers.

**Failure (Wrong Behavior):**
When we ran TC-19 (self-transfer test), the transfer went through instead of being rejected. The user could transfer money to themselves, which doesn't make sense in a real banking app.

**Fix:** We added a check at the beginning of the `transfer_money()` function:
```python
if from_account_num == to_account_num:
    return False, "Cannot transfer to the same account"
```

After the fix, TC-19 passed correctly.

### 5.3 Distinguishing Error, Fault, and Failure

| Term | Definition | Our Example |
|------|-----------|-------------|
| **Error** | A human mistake in thinking or understanding | Assuming self-transfers are impossible |
| **Fault** | A defect in the code caused by the error | Missing validation check for same account |
| **Failure** | The wrong output observed when running the faulty code | Self-transfer succeeding instead of failing |

### 5.4 How Testing Helped Reduce Risk

Testing helped us reduce risk in several ways:

1. **Catching edge cases early:** Tests like TC-16 (negative transfer) and TC-17 (zero transfer) caught potential vulnerabilities before they could reach production. Without testing, a user might transfer -100 EGP and end up with more money.

2. **Verifying math accuracy:** TC-20 and TC-30 confirmed that account balances update correctly after transfers. In a real banking system, getting the math wrong would be catastrophic.

3. **Ensuring security:** Tests TC-07 through TC-11 verified that password security rules are enforced. Without these tests, we might have deployed a system that accepts weak passwords like "123".

4. **Regression prevention:** Since all tests are automated with pytest, we can run them anytime we change the code. If a future change breaks something, the tests will catch it immediately.

5. **Building confidence:** Having 32 passing tests gives us confidence that the core features work correctly. We can show the test results as evidence.

---

## 6. Conclusion

In this project, we built a Simple Banking System in Python and tested it using pytest (run through uv). We wrote 32 automated test cases covering all 5 features: Login, View Balance, Transfer Money, Transaction History, and Change Password.

Key takeaways:
- We applied 5 quality factors (Correctness, Reliability, Security, Usability, Maintainability) to guide our design
- We used Equivalence Partitioning and Boundary Value Analysis to design our test cases
- All 32 tests pass, giving us a 100% pass rate
- Testing helped us catch bugs early and reduce the risk of deploying faulty software

The project demonstrates that even a small system benefits a lot from proper testing. Running `uv run pytest` takes less than 1 second and checks everything automatically.
