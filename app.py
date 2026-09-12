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


# =========================
# ADD CONTACT
# =========================

@app.route("/add_contact", methods=["POST"])
def add_contact():

    data = request.get_json() or {}

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()

    if not name or not phone:
        return jsonify({
            "success": False,
            "message": "Name and phone are required."
        }), 400

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


# =========================
# GET CONTACTS
# =========================

@app.route("/contacts")
def contacts():

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM contacts ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([
        {
            "id": row["id"],
            "name": row["name"],
            "phone": row["phone"]
        }
        for row in rows
    ])


# =========================
# DELETE CONTACT
# =========================

@app.route("/delete_contact/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):

    conn = get_db()

    cursor = conn.execute(
        "DELETE FROM contacts WHERE id = ?",
        (contact_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({
            "success": False,
            "message": "Contact not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Contact deleted successfully."
    })


# =========================
# SAVE SOS HISTORY
# =========================

@app.route("/save_history", methods=["POST"])
def save_history():

    data = request.get_json() or {}

    event = data.get("event", "SOS Activated")
    location = data.get("location", "")

    conn = get_db()

    conn.execute(
        """
        INSERT INTO emergency_history
        (event, location)
        VALUES (?, ?)
        """,
        (event, location)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Emergency history saved successfully."
    })


# =========================
# GET HISTORY
# =========================

@app.route("/history")
def history():

    conn = get_db()

    records = conn.execute(
        """
        SELECT * FROM emergency_history
        ORDER BY id DESC
        """
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


# =========================
# DELETE HISTORY
# =========================

@app.route("/delete_history/<int:history_id>", methods=["DELETE"])
def delete_history(history_id):

    conn = get_db()

    cursor = conn.execute(
        "DELETE FROM emergency_history WHERE id = ?",
        (history_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({
            "success": False,
            "message": "History record not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "History deleted successfully."
    })


# =========================
# INITIALIZE DATABASE
# =========================

init_db()


if __name__ == "__main__":
    app.run(debug=True)