"""Flask web server for the Simple Banking System.

Provides a REST-style JSON API on top of the existing BankSystem class
and serves the single-page frontend at the root URL.
"""

from flask import Flask, request, jsonify, session, render_template
from banking.bank import BankSystem

app = Flask(__name__)
app.secret_key = "sqa-banking-secret-key-2024"

# Single shared bank system instance (in-memory, resets on restart)
bank = BankSystem()

# Pre-populate 3 users for manual testing
bank.register_user("ahmed", "Ahmed123!")
bank.register_user("sara", "Sara5678!")
bank.register_user("khaled", "Khaled999!")


# --------------- API Endpoints ---------------

@app.route("/")
def index():
    """Serve the frontend single-page application."""
    return render_template("index.html")


@app.route("/api/register", methods=["POST"])
def register():
    """Register a new user.

    Expects JSON: { "username": str, "password": str }
    Returns JSON: { "success": bool, "message": str }
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    success, message = bank.register_user(username, password)

    if success:
        # Auto-login after registration
        session["username"] = username
        user = bank.get_user(username)
        return jsonify({
            "success": True,
            "message": message,
            "account_number": user.account_number
        })

    return jsonify({"success": False, "message": message})


@app.route("/api/login", methods=["POST"])
def login():
    """Log in a user.

    Expects JSON: { "username": str, "password": str }
    Returns JSON: { "success": bool, "message": str }
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    success, message = bank.login(username, password)

    if success:
        session["username"] = username
        user = bank.get_user(username)
        return jsonify({
            "success": True,
            "message": message,
            "account_number": user.account_number
        })

    return jsonify({"success": False, "message": message})


@app.route("/api/logout", methods=["POST"])
def logout():
    """Log out the current user."""
    session.pop("username", None)
    bank.logout()
    return jsonify({"success": True, "message": "Logged out"})


@app.route("/api/balance", methods=["GET"])
def balance():
    """Get balance for the logged-in user.

    Returns JSON: { "success": bool, "balance": float | "message": str }
    """
    username = session.get("username")
    if not username:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    success, result = bank.get_balance(username)

    if success:
        return jsonify({"success": True, "balance": result})
    return jsonify({"success": False, "message": result})


@app.route("/api/transfer", methods=["POST"])
def transfer():
    """Transfer money to another account.

    Expects JSON: { "to_account": str, "amount": float }
    Returns JSON: { "success": bool, "message": str }
    """
    username = session.get("username")
    if not username:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    data = request.get_json(silent=True) or {}
    to_account = data.get("to_account", "")
    amount = data.get("amount", 0)

    # Convert amount to float
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid amount"})

    success, message = bank.transfer(username, to_account, amount)
    return jsonify({"success": success, "message": message})


@app.route("/api/history", methods=["GET"])
def history():
    """Get transaction history for the logged-in user.

    Returns JSON: { "success": bool, "transactions": [...] }
    """
    username = session.get("username")
    if not username:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    transactions = bank.get_transaction_history(username)

    return jsonify({
        "success": True,
        "transactions": [
            {
                "id": t.transaction_id,
                "from_account": t.from_account,
                "to_account": t.to_account,
                "amount": t.amount,
                "type": t.transaction_type.value,
                "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            for t in transactions
        ]
    })


@app.route("/api/change-password", methods=["POST"])
def change_password():
    """Change the password for the logged-in user.

    Expects JSON: { "old_password": str, "new_password": str }
    Returns JSON: { "success": bool, "message": str }
    """
    username = session.get("username")
    if not username:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    data = request.get_json(silent=True) or {}
    old_password = data.get("old_password", "")
    new_password = data.get("new_password", "")

    success, message = bank.change_password(username, old_password, new_password)
    return jsonify({"success": success, "message": message})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
