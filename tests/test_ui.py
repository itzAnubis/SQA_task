"""Tests for the Flask web API / UI interface layer (TC-33 to TC-44)."""

import pytest
from app import app, bank
from banking.bank import BankSystem


@pytest.fixture(autouse=True)
def reset_bank():
    """Reset the bank system and Flask app state before each test."""
    # Replace the global bank instance with a fresh one
    import app as app_module
    app_module.bank = BankSystem()
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    yield


@pytest.fixture
def client():
    """Create a Flask test client."""
    with app.test_client() as c:
        yield c


def _register(client, username="ahmed", password="Ahmed123!"):
    """Helper to register a user via API."""
    return client.post("/api/register", json={
        "username": username,
        "password": password
    })


def _login(client, username="ahmed", password="Ahmed123!"):
    """Helper to login a user via API."""
    return client.post("/api/login", json={
        "username": username,
        "password": password
    })


class TestUIRegister:
    """Test cases for the registration API endpoint."""

    def test_register_success(self, client):
        """TC-33: Register via API returns success and account number."""
        resp = _register(client)
        data = resp.get_json()
        assert data["success"] is True
        assert "account_number" in data
        assert data["account_number"].startswith("ACC")

    def test_register_duplicate(self, client):
        """TC-34: Register with duplicate username via API fails."""
        _register(client)
        resp = _register(client)  # same username again
        data = resp.get_json()
        assert data["success"] is False
        assert "already exists" in data["message"].lower()


class TestUILogin:
    """Test cases for the login API endpoint."""

    def test_login_success(self, client):
        """TC-35: Login via API returns success."""
        _register(client)
        resp = _login(client)
        data = resp.get_json()
        assert data["success"] is True
        assert "Welcome" in data["message"]

    def test_login_wrong_password(self, client):
        """TC-36: Login with wrong password via API fails."""
        _register(client)
        resp = _login(client, password="WrongPass1")
        data = resp.get_json()
        assert data["success"] is False
        assert "Invalid" in data["message"]


class TestUIBalance:
    """Test cases for the balance API endpoint."""

    def test_get_balance(self, client):
        """TC-37: Get balance via API after login."""
        _register(client)
        _login(client)
        resp = client.get("/api/balance")
        data = resp.get_json()
        assert data["success"] is True
        assert data["balance"] == 1000.0

    def test_balance_unauthorized(self, client):
        """TC-43: Accessing balance without login returns unauthorized."""
        resp = client.get("/api/balance")
        assert resp.status_code == 401
        data = resp.get_json()
        assert data["success"] is False
        assert "Not logged in" in data["message"]


class TestUITransfer:
    """Test cases for the transfer API endpoint."""

    def test_transfer_success(self, client):
        """TC-38: Transfer via API succeeds."""
        _register(client, "ahmed", "Ahmed123!")
        _register(client, "sara", "Sara5678!")
        _login(client, "ahmed", "Ahmed123!")

        # Get sara's account number
        import app as app_module
        sara_acc = app_module.bank.get_user("sara").account_number

        resp = client.post("/api/transfer", json={
            "to_account": sara_acc,
            "amount": 200.0
        })
        data = resp.get_json()
        assert data["success"] is True
        assert "successful" in data["message"].lower()

    def test_transfer_insufficient(self, client):
        """TC-39: Transfer with insufficient funds via API fails."""
        _register(client, "ahmed", "Ahmed123!")
        _register(client, "sara", "Sara5678!")
        _login(client, "ahmed", "Ahmed123!")

        import app as app_module
        sara_acc = app_module.bank.get_user("sara").account_number

        resp = client.post("/api/transfer", json={
            "to_account": sara_acc,
            "amount": 5000.0
        })
        data = resp.get_json()
        assert data["success"] is False
        assert "Insufficient" in data["message"]


class TestUIHistory:
    """Test cases for the history API endpoint."""

    def test_get_history(self, client):
        """TC-40: Get transaction history via API."""
        _register(client, "ahmed", "Ahmed123!")
        _register(client, "sara", "Sara5678!")
        _login(client, "ahmed", "Ahmed123!")

        import app as app_module
        sara_acc = app_module.bank.get_user("sara").account_number

        client.post("/api/transfer", json={
            "to_account": sara_acc,
            "amount": 150.0
        })

        resp = client.get("/api/history")
        data = resp.get_json()
        assert data["success"] is True
        assert len(data["transactions"]) == 1
        assert data["transactions"][0]["amount"] == 150.0


class TestUIChangePassword:
    """Test cases for the change password API endpoint."""

    def test_change_password_success(self, client):
        """TC-41: Change password via API succeeds."""
        _register(client)
        _login(client)
        resp = client.post("/api/change-password", json={
            "old_password": "Ahmed123!",
            "new_password": "NewPass99!"
        })
        data = resp.get_json()
        assert data["success"] is True
        assert "successfully" in data["message"].lower()

    def test_register_weak_password(self, client):
        """TC-44: Register with weak password via API fails."""
        resp = _register(client, password="weak")
        data = resp.get_json()
        assert data["success"] is False
        assert "8 characters" in data["message"]


class TestUILogout:
    """Test cases for the logout API endpoint."""

    def test_logout_clears_session(self, client):
        """TC-42: Logout via API clears session."""
        _register(client)
        _login(client)

        # Should be able to get balance
        resp = client.get("/api/balance")
        assert resp.get_json()["success"] is True

        # Logout
        resp = client.post("/api/logout")
        assert resp.get_json()["success"] is True

        # Balance should now fail
        resp = client.get("/api/balance")
        assert resp.status_code == 401
