from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

users = {}
deposits = []
withdraws = []

# ================= UI =================
@app.route("/")
def home():
    return send_file("index.html")

@app.route("/admin")
def admin():
    return send_file("admin.html")

# ================= USERS =================
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]

    if email not in users:
        users[email] = {"balance": 0.0}

    return jsonify({"status": "ok", "user": users[email]})

@app.route("/user/<email>")
def get_user(email):
    return jsonify(users.get(email, {}))

# ================= DEPOSIT =================
@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.json

    deposits.append({
        "email": data["email"],
        "amount": data["amount"],
        "txid": data["txid"],
        "status": "pending"
    })

    return jsonify({"status": "ok"})

# ================= WITHDRAW =================
@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.json

    withdraws.append({
        "email": data["email"],
        "amount": data["amount"],
        "wallet": data["wallet"],
        "status": "pending"
    })

    return jsonify({"status": "ok"})

# ================= ADMIN DATA =================
@app.route("/admin/data")
def admin_data():
    return jsonify({
        "users": users,
        "deposits": deposits,
        "withdraws": withdraws
    })

# ================= ADD BALANCE =================
@app.route("/admin/add_balance", methods=["POST"])
def add_balance():
    data = request.json
    email = data["email"]
    amount = float(data["amount"])

    if email in users:
        users[email]["balance"] += amount
        return jsonify({"status": "ok"})

    return jsonify({"status": "error"})

# ================= APPROVE WITHDRAW =================
@app.route("/admin/approve_withdraw", methods=["POST"])
def approve_withdraw():
    i = data = request.json["index"]

    if i < len(withdraws):
        w = withdraws[i]
        email = w["email"]
        amount = float(w["amount"])

        if users[email]["balance"] >= amount:
            users[email]["balance"] -= amount
            withdraws[i]["status"] = "approved"
            return jsonify({"status": "ok"})

    return jsonify({"status": "error"})

# ================= APPROVE DEPOSIT =================
@app.route("/admin/approve_deposit", methods=["POST"])
def approve_deposit():
    i = request.json["index"]

    if i < len(deposits):
        d = deposits[i]
        email = d["email"]
        amount = float(d["amount"])

        users[email]["balance"] += amount
        deposits[i]["status"] = "approved"

        return jsonify({"status": "ok"})

    return jsonify({"status": "error"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
