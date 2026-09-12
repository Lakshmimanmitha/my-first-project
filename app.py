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

    # Emergency contacts table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    # Emergency history table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS emergency_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        return jsonify({
            "success": False,
            "message": "Name and phone are required."
        })

    conn = get_db()

    conn.execute(
        "INSERT INTO contacts (name, phone) VALUES (?, ?)",
        (name, phone)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Contact saved successfully."
    })


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
@app.route("/delete_contact/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    conn = get_db()

    contact = conn.execute(
        "SELECT * FROM contacts WHERE id = ?",
        (contact_id,)
    ).fetchone()

    if contact is None:
        conn.close()
        return jsonify({
            "success": False,
            "message": "Contact not found."
        }), 404

    conn.execute(
        "DELETE FROM contacts WHERE id = ?",
        (contact_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Contact deleted successfully."
    })


@app.route("/save_history", methods=["POST"])
def save_history():
    data = request.get_json()

    event = data.get("event", "SOS Activated")
    location = data.get("location", "")

    conn = get_db()

    conn.execute(
        "INSERT INTO emergency_history (event, location) VALUES (?, ?)",
        (event, location)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Emergency history saved successfully."
    })


@app.route("/history")
def history():
    conn = get_db()

    records = conn.execute(
        "SELECT * FROM emergency_history ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([
        {
            "id": record["id"],
            "event": record["event"],
            "location": record["location"],
            "created_at": record["created_at"]
        }
        for record in records
    ])


init_db()

if __name__ == "__main__":
    app.run(debug=True)