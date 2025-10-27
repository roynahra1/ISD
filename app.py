from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
CORS(app)
# Serve the appointment form
@app.route("/appointment.html")
def serve_form():
    return render_template("appointment.html")  # Ensure this is in /templates

# MySQL connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="isd"
    )

# Book appointment
@app.route("/book", methods=["POST"])
def book_appointment():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        car_plate = data.get("car_plate")
        date = data.get("date")
        time = data.get("time")
        notes = data.get("notes", "")
        service_ids = data.get("service_ids", [])

        if not all([car_plate, date, time]) or not service_ids:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Validate date and time format
        try:
            appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
            appointment_time = datetime.strptime(time, "%H:%M").time()
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid date or time format"}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Check for time conflict (±30 minutes)
        cursor.execute("""
            SELECT Appointment_id FROM appointment
            WHERE Date = %s AND ABS(TIMESTAMPDIFF(MINUTE, Time, %s)) < 30
        """, (date, time))
        if cursor.fetchone():
            return jsonify({
                "status": "conflict",
                "message": f"Time slot too close to another appointment on {date}. Choose a time at least 30 minutes apart."
            }), 409

        # Insert appointment
        cursor.execute("""
            INSERT INTO appointment (Date, Time, Notes, Car_plate)
            VALUES (%s, %s, %s, %s)
        """, (date, time, notes, car_plate))
        appointment_id = cursor.lastrowid

        # Link services
        for sid in service_ids:
            cursor.execute("""
                INSERT INTO appointment_service (Appointment_id, Service_id)
                VALUES (%s, %s)
            """, (appointment_id, sid))

        conn.commit()
        return jsonify({
            "status": "success",
            "message": f"✅ Appointment booked for {car_plate} on {date} at {time}",
            "appointment_id": appointment_id
        }), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# Get client info by email
@app.route("/client", methods=["GET"])
def get_client():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT o.Owner_name AS name, c.Car_plate, c.Model, c.Year
            FROM owner o
            JOIN car c ON o.Owner_id = c.Owner_id
            WHERE o.Owner_email = %s
            ORDER BY c.Year DESC
            LIMIT 1
        """, (email,))
        row = cursor.fetchone()
        return jsonify(row or {}), 200

    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == "__main__":
    app.run(debug=True)