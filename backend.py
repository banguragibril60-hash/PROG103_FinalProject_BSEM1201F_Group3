import os
import json
import re
from datetime import datetime

# -----------------------------
# Data Storage Layer
# -----------------------------
queue = []
processed_patients = []
served_count = 0
current_patient = None
service_times = []

DATA_FILE = "clinic_records.json"

# -----------------------------
# File I/O Logic
# -----------------------------
def load_data(silent=False):
    """Load data from JSON file. Called silently on startup."""
    global queue, processed_patients, served_count
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                queue[:] = data.get("queue", [])
                processed_patients[:] = data.get("processed", [])
                served_count = data.get("served_count", 0)
            if not silent:
                return True, "Records loaded successfully!"
            return True, ""
        except Exception as e:
            if not silent:
                return False, f"Could not load previous data: {e}"
            return False, ""
    if not silent:
        return None, "No previous records found."
    return None, ""


def save_data():
    """Save current state to JSON file."""
    try:
        data = {
            "queue": queue,
            "processed": processed_patients,
            "served_count": served_count
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return True, "Records saved successfully!"
    except Exception as e:
        return False, f"Could not save data: {e}"


# -----------------------------
# Input Validation
# -----------------------------
def validate_name(name):
    if not name or len(name.strip()) < 3:
        return "Full Name must be at least 3 characters."
    if not re.match(r"^[a-zA-Z\s'-]+$", name):
        return "Name should contain only letters, spaces, hyphens and apostrophes."
    return None


def validate_dob(dob):
    if not dob:
        return "Date of Birth is required."
    try:
        date = datetime.strptime(dob, "%Y-%m-%d")
        if date > datetime.now():
            return "Date of Birth cannot be in the future."
    except ValueError:
        return "Date of Birth must be in YYYY-MM-DD format."
    return None


def validate_phone(phone, field_name="Phone Number"):
    if not phone:
        return f"{field_name} is required."
    cleaned = re.sub(r"[\s() -]", "", phone)
    if not re.match(r"^\+?\d{7,15}$", cleaned):
        return f"{field_name} must be 7-15 digits (optionally with +)."
    return None


def validate_email(email):
    if not email:
        return "Email is required."
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return "Invalid email format."
    return None


def validate_ticket(ticket):
    if not ticket:
        return "Ticket Number is required."
    if not re.match(r"^TKT-\d{4}-\d{3}$", ticket):
        return "Ticket should be in format TKT-YYYY-XXX"
    return None


def validate_emergency_phone(phone):
    return validate_phone(phone, "Emergency Contact Phone")


# Optional helper (useful for future Patients tab)
def get_all_patients():
    """Return combined queue + recent processed patients."""
    return queue + processed_patients[-10:]
