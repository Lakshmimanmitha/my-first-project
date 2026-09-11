from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_contact", methods=["POST"])
def add_contact():
    data = request.get_json()

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()

    if not name or not phone:
        return jsonify({"success": False, "message": "Name and phone are required."})

    conn = get_db()

    conn.execute(
        "INSERT INTO contacts (name, phone) VALUES (?, ?)",
        (name, phone)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Contact saved successfully."})


@app.route("/contacts")
def contacts():
    conn = get_db()

    contacts = conn.execute(
        "SELECT * FROM contacts ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([
        {
            "id": contact["id"],
            "name": contact["name"],
            "phone": contact["phone"]
        }
        for contact in contacts
    ])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)