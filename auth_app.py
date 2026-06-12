from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)

# ---------------- MYSQL CONFIG ----------------
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""   # add password if any
app.config["MYSQL_DB"] = "ai_users"

mysql = MySQL(app)

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        name = data["name"]
        email = data["email"]
        password = bcrypt.generate_password_hash(
            data["password"]
        ).decode("utf-8")

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({
            "status": "success",
            "message": "Account created successfully!"
        })

    except Exception as e:
        print("REGISTER ERROR:", e)
        return jsonify({
            "status": "error",
            "message": "Registration failed"
        })


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT id, name, password FROM users WHERE email=%s",
        [email]
    )
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({
            "status": "error",
            "message": "Email not found"
        })

    if not bcrypt.check_password_hash(user[2], password):
        return jsonify({
            "status": "error",
            "message": "Incorrect password"
        })

    return jsonify({
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": user[0],
            "name": user[1],
            "email": email
        }
    })


# ---------------- LOGOUT (FRONTEND HANDLED) ----------------
@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({
        "status": "success",
        "message": "Logged out successfully"
    })


@app.route("/")
def home():
    return "Auth Backend Running Successfully!"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
