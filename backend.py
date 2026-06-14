import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import backend

root = tk.Tk()
root.title("Clinic Queue System")
root.geometry("950x700")
root.configure(bg="#FAFAFA")

# -----------------------------
# Login System
# -----------------------------
logged_in = False
LOGIN_USERNAME = "Group3"
LOGIN_PASSWORD = "clinic123"

login_frame = tk.Frame(root, bg="#FAFAFA")
login_frame.pack(expand=True, fill="both")

tk.Label(login_frame, text="🔐 Clinic Queue System Login",
         font=("Arial", 18, "bold"), bg="#FAFAFA", fg="#0D47A1").pack(pady=40)

tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="#FAFAFA").pack(pady=5)
username_entry = tk.Entry(login_frame, font=("Arial", 12), width=30)
username_entry.pack(pady=5)

tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="#FAFAFA").pack(pady=5)
password_entry = tk.Entry(login_frame, font=("Arial", 12), width=30, show="*")
password_entry.pack(pady=5)

def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_btn.config(text="Hide")
    else:
        password_entry.config(show="*")
        show_btn.config(text="Show")

show_btn = tk.Button(login_frame, text="Show", command=toggle_password, width=8)
show_btn.pack(pady=5)

def attempt_login():
    global logged_in
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Login", "Please enter both username and password.")
        return

    if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
        logged_in = True
        login_frame.pack_forget()
        notebook.pack(expand=True, fill="both")
        refresh_patient_table()
        refresh_all_patients_table()
        update_display()
        messagebox.showinfo("Login Successful", "Welcome to the Clinic Queue System!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

tk.Button(login_frame, text="Login", command=attempt_login,
          bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=30)

# -----------------------------
# Icons
# -----------------------------
try:
    add_icon = tk.PhotoImage(file="icons/add.png")
    process_icon = tk.PhotoImage(file="icons/process.png")
    clear_icon = tk.PhotoImage(file="icons/clear.png")
    exit_icon = tk.PhotoImage(file="icons/exit.png")
    served_icon = tk.PhotoImage(file="icons/served.png")
    balance_icon = tk.PhotoImage(file="icons/balance.png")
    time_icon = tk.PhotoImage(file="icons/time.png")
    current_icon = tk.PhotoImage(file="icons/current.png")
except Exception:
    add_icon = process_icon = clear_icon = exit_icon = None
    served_icon = balance_icon = time_icon = current_icon = None

# -----------------------------
# Tabs
# -----------------------------
notebook = ttk.Notebook(root)

# === Dashboard Tab ===
dashboard_frame = tk.Frame(notebook, bg="#E3F2FD")
notebook.add(dashboard_frame, text="Dashboard")

served_label = tk.Label(dashboard_frame, image=served_icon, text="Today Served: 0", compound="top", bg="#E3F2FD", fg="#0D47A1", font=("Arial", 12, "bold"))
served_label.grid(row=0, column=0, padx=20, pady=20)

balance_label = tk.Label(dashboard_frame, image=balance_icon, text="Queue Balance: 0", compound="top", bg="#E3F2FD", fg="#0D47A1", font=("Arial", 12, "bold"))
balance_label.grid(row=0, column=1, padx=20, pady=20)

time_label = tk.Label(dashboard_frame, image=time_icon, text="Avg Service Time: --", compound="top", bg="#E3F2FD", fg="#0D47A1", font=("Arial", 12, "bold"))
time_label.grid(row=0, column=2, padx=20, pady=20)

current_label = tk.Label(dashboard_frame, image=current_icon, text="Current Served: None", compound="top", bg="#E3F2FD", fg="#0D47A1", font=("Arial", 12, "bold"))
current_label.grid(row=0, column=3, padx=20, pady=20)

# Patient Queue Table
tk.Label(dashboard_frame, text="Patients Queue - Select to Process", font=("Arial", 14, "bold"), bg="#E3F2FD").grid(row=1, column=0, columnspan=4, pady=10, sticky="w", padx=20)

cols = ("Ticket", "Full Name", "Status", "Priority", "Appointment Type")
patient_tree = ttk.Treeview(dashboard_frame, columns=cols, show="headings", height=12)
patient_tree.grid(row=2, column=0, columnspan=4, padx=20, pady=5, sticky="nsew")

for col in cols:
    patient_tree.heading(col, text=col)
    patient_tree.column(col, width=150, anchor="w")

tree_scroll = ttk.Scrollbar(dashboard_frame, orient="vertical", command=patient_tree.yview)
tree_scroll.grid(row=2, column=4, sticky="ns")
patient_tree.configure(yscrollcommand=tree_scroll.set)
dashboard_frame.grid_rowconfigure(2, weight=1)
dashboard_frame.grid_columnconfigure(0, weight=1)

def refresh_patient_table():
    for item in patient_tree.get_children():
        patient_tree.delete(item)
    for p in backend.queue:
        patient_tree.insert("", "end", values=(
            p.get("Ticket", ""), p.get("Full Name", ""), p.get("Status", "Waiting"),
            p.get("Priority", "Normal"), p.get("Appointment Type", "")
        ))

def process_selected_patient():
    selection = patient_tree.selection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a patient.")
        return
    item = patient_tree.item(selection[0])
    ticket = item['values'][0]
    patient = next((p for p in backend.queue if p.get("Ticket") == ticket), None)
    if not patient:
        messagebox.showerror("Error", "Patient not found.")
        return
    if messagebox.askyesno("Process", f"Process {patient['Full Name']}?"):
        backend.queue.remove(patient)
        backend.current_patient = patient["Full Name"]
        backend.processed_patients.append(patient)
        backend.served_count += 1
        try:
            check_in = datetime.strptime(patient["Check-In"], "%Y-%m-%d %H:%M:%S")
            duration = (datetime.now() - check_in).seconds
            backend.service_times.append(duration)
        except:
            pass
        backend.save_data()
        refresh_patient_table()
        refresh_all_patients_table()
        update_display()
        messagebox.showinfo("Success", f"Processed: {patient['Full Name']}")

tk.Button(dashboard_frame, image=process_icon, text="Process Selected Patient", compound="left", command=process_selected_patient,
          bg="#FF9800", fg="white", font=("Arial", 11, "bold")).grid(row=3, column=0, columnspan=4, pady=10)

# === Registration Tab (unchanged) ===
registration_frame = tk.Frame(notebook, bg="#F5F5F5")
reg_canvas = tk.Canvas(registration_frame, bg="#F5F5F5", highlightthickness=0)
reg_scrollbar = ttk.Scrollbar(registration_frame, orient="vertical", command=reg_canvas.yview)
reg_scrollable_frame = tk.Frame(reg_canvas, bg="#F5F5F5")

reg_scrollable_frame.bind("<Configure>", lambda e: reg_canvas.configure(scrollregion=reg_canvas.bbox("all")))
reg_canvas.create_window((0, 0), window=reg_scrollable_frame, anchor="nw")
reg_canvas.configure(yscrollcommand=reg_scrollbar.set)

reg_canvas.pack(side="left", fill="both", expand=True)
reg_scrollbar.pack(side="right", fill="y")

notebook.add(registration_frame, text="Registration")

def make_label(frame, text, row):
    tk.Label(frame, text=text, bg="#F5F5F5", fg="#212121", font=("Arial", 10)).grid(
        row=row, column=0, sticky="w", padx=10, pady=5)

row = 0
make_label(reg_scrollable_frame, "Full Name", row)
name_entry = tk.Entry(reg_scrollable_frame, width=40); name_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Date of Birth (YYYY-MM-DD)", row)
dob_entry = tk.Entry(reg_scrollable_frame, width=40); dob_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Gender", row)
gender_combo = ttk.Combobox(reg_scrollable_frame, values=["Male", "Female", "Other"], width=37, state="readonly")
gender_combo.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Phone Number", row)
phone_entry = tk.Entry(reg_scrollable_frame, width=40); phone_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Email Address", row)
email_entry = tk.Entry(reg_scrollable_frame, width=40); email_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Address", row)
address_entry = tk.Entry(reg_scrollable_frame, width=40); address_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Ticket Number", row)
ticket_entry = tk.Entry(reg_scrollable_frame, width=40); ticket_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Check-In Timestamp", row)
checkin_entry = tk.Entry(reg_scrollable_frame, width=40)
checkin_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
checkin_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Appointment Time (HH:MM)", row)
appt_entry = tk.Entry(reg_scrollable_frame, width=40); appt_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Appointment Type", row)
appt_type = ttk.Combobox(reg_scrollable_frame, values=["Fever", "Checkup", "Other"], width=37)
appt_type.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Purpose of Visit / Notes", row)
notes_text = tk.Text(reg_scrollable_frame, width=40, height=4)
notes_text.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Assigned Provider/Room", row)
provider_entry = tk.Entry(reg_scrollable_frame, width=40); provider_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Blood Type", row)
blood_type = ttk.Combobox(reg_scrollable_frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"], width=37)
blood_type.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Allergies", row)
allergies_entry = tk.Entry(reg_scrollable_frame, width=40); allergies_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Emergency Contact Name", row)
emergency_name = tk.Entry(reg_scrollable_frame, width=40); emergency_name.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Emergency Contact Phone", row)
emergency_phone = tk.Entry(reg_scrollable_frame, width=40); emergency_phone.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Queue Status", row)
status_entry = ttk.Combobox(reg_scrollable_frame, values=["Waiting", "In Progress", "Completed"], width=37)
status_entry.grid(row=row, column=1, pady=5); row += 1

make_label(reg_scrollable_frame, "Priority Level", row)
priority_entry = ttk.Combobox(reg_scrollable_frame, values=["Normal", "Urgent", "Emergency"], width=37)
priority_entry.grid(row=row, column=1, pady=5); row += 1

def auto_purpose(*args):
    purpose_map = {
        "Fever": "Patient presents with fever, possibly associated with infection or flu-like symptoms.",
        "Checkup": "Routine medical check-up and health assessment.",
        "Other": "Patient requires consultation for unspecified medical concern."
    }
    selected = appt_type.get()
    if selected in purpose_map:
        notes_text.delete("1.0", tk.END)
        notes_text.insert("1.0", purpose_map[selected])

appt_type.bind("<<ComboboxSelected>>", auto_purpose)

# -----------------------------
# Core Functions
# -----------------------------
def update_dashboard():
    balance_label.config(text=f"Queue Balance: {len(backend.queue)}")
    served_label.config(text=f"Today Served: {backend.served_count}")
    current_label.config(text=f"Current Served: {backend.current_patient if backend.current_patient else 'None'}")
    if backend.service_times:
        avg = sum(backend.service_times) / len(backend.service_times)
        time_label.config(text=f"Avg Service Time: {avg:.1f} sec")
    else:
        time_label.config(text="Avg Service Time: --")

def update_display():
    update_dashboard()
    refresh_patient_table()

def add_patient():
    errors = []
    err = backend.validate_name(name_entry.get())
    if err: errors.append(err)
    err = backend.validate_dob(dob_entry.get())
    if err: errors.append(err)
    err = backend.validate_phone(phone_entry.get())
    if err: errors.append(err)
    err = backend.validate_email(email_entry.get())
    if err: errors.append(err)
    err = backend.validate_ticket(ticket_entry.get())
    if err: errors.append(err)
    err = backend.validate_emergency_phone(emergency_phone.get())
    if err: errors.append(err)

    if errors:
        messagebox.showerror("Validation Error", "\n".join(errors))
        return

    patient = {
        "Full Name": name_entry.get().strip(),
        "DOB": dob_entry.get().strip(),
        "Gender": gender_combo.get(),
        "Phone": phone_entry.get().strip(),
        "Email": email_entry.get().strip().lower(),
        "Address": address_entry.get().strip(),
        "Ticket": ticket_entry.get().strip(),
        "Check-In": checkin_entry.get().strip(),
        "Appointment Time": appt_entry.get().strip(),
        "Appointment Type": appt_type.get(),
        "Purpose of Visit": notes_text.get("1.0", tk.END).strip(),
        "Provider": provider_entry.get().strip(),
        "Blood Type": blood_type.get(),
        "Allergies": allergies_entry.get().strip(),
        "Emergency Contact": emergency_name.get().strip(),
        "Emergency Phone": emergency_phone.get().strip(),
        "Status": status_entry.get() or "Waiting",
        "Priority": priority_entry.get() or "Normal"
    }

    backend.queue.append(patient)
    backend.save_data()
    update_display()
    refresh_all_patients_table()
    messagebox.showinfo("Success", f"Patient {patient['Full Name']} added successfully!")

def clear_form():
    name_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)
    gender_combo.set("")
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    ticket_entry.delete(0, tk.END)
    checkin_entry.delete(0, tk.END)
    checkin_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    appt_entry.delete(0, tk.END)
    appt_type.set("")
    notes_text.delete("1.0", tk.END)
    provider_entry.delete(0, tk.END)
    blood_type.set("")
    allergies_entry.delete(0, tk.END)
    emergency_name.delete(0, tk.END)
    emergency_phone.delete(0, tk.END)
    status_entry.set("Waiting")
    priority_entry.set("Normal")
    messagebox.showinfo("Clear Form", "Form cleared.")

def clear_queue():
    if messagebox.askyesno("Confirm", "Clear entire queue?"):
        backend.queue.clear()
        backend.current_patient = None
        backend.save_data()
        update_display()
        refresh_all_patients_table()
        messagebox.showinfo("Clear Queue", "Queue has been cleared.")

def exit_app():
    backend.save_data()
    if messagebox.askyesno("Exit", "Save and exit?"):
        root.destroy()

def save_data_bridge():
    success, msg = backend.save_data()
    if success:
        messagebox.showinfo("Save", "Records saved successfully!")
    else:
        messagebox.showerror("Save Error", msg)

# Registration Buttons
btn_row = row + 1
tk.Button(reg_scrollable_frame, image=add_icon, text="Add Patient", compound="left", command=add_patient,
          bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=btn_row, column=0, padx=10, pady=8)

tk.Button(reg_scrollable_frame, text="🧹 Clear Form", command=clear_form,
          bg="#9E9E9E", fg="white", font=("Arial", 10, "bold")).grid(row=btn_row + 1, column=0, padx=10, pady=8)

tk.Button(reg_scrollable_frame, text="💾 Save Records", command=save_data_bridge,
          bg="#2196F3", fg="white", font=("Arial", 10, "bold")).grid(row=btn_row + 1, column=1, padx=10, pady=8)

tk.Button(reg_scrollable_frame, image=clear_icon, text="Clear Queue", compound="left", command=clear_queue,
          bg="#F44336", fg="white", font=("Arial", 10, "bold")).grid(row=btn_row + 2, column=0, padx=10, pady=8)

tk.Button(reg_scrollable_frame, image=exit_icon, text="Exit", compound="left", command=exit_app,
          bg="#424242", fg="white", font=("Arial", 10, "bold")).grid(row=btn_row + 2, column=1, padx=10, pady=8)

# === Patients Tab ===
patients_frame = tk.Frame(notebook, bg="#F5F5F5")
notebook.add(patients_frame, text="Patients")

tk.Label(patients_frame, text="All Registered Patients", font=("Arial", 14, "bold"), bg="#F5F5F5").pack(pady=10)

# Updated Columns
all_cols = ("Ticket", "Full Name", "DOB", "Phone", "Registration Date", "Priority", "Appointment Type")
all_patients_tree = ttk.Treeview(patients_frame, columns=all_cols, show="headings", height=15)
all_patients_tree.pack(fill="both", expand=True, padx=20, pady=5)

for col in all_cols:
    all_patients_tree.heading(col, text=col)
    all_patients_tree.column(col, width=120, anchor="w")

all_scroll = ttk.Scrollbar(patients_frame, orient="vertical", command=all_patients_tree.yview)
all_scroll.pack(side="right", fill="y")
all_patients_tree.configure(yscrollcommand=all_scroll.set)

# Action Frame
action_frame = tk.Frame(patients_frame, bg="#F5F5F5")
action_frame.pack(pady=8)

def get_selected_patient():
    selection = all_patients_tree.selection()
    if not selection:
        messagebox.showwarning("Selection", "Please select a patient.")
        return None
    item = all_patients_tree.item(selection[0])
    ticket = item['values'][0]
    for p in backend.queue + backend.processed_patients:
        if p.get("Ticket") == ticket:
            return p
    return None

def view_patient():
    patient = get_selected_patient()
    if patient:
        details = "\n".join([f"{k}: {v}" for k, v in patient.items()])
        messagebox.showinfo("Patient Details", details)

def edit_patient():
    messagebox.showinfo("Edit", "Full Edit window coming in next update.")

def delete_patient():
    patient = get_selected_patient()
    if patient and messagebox.askyesno("Delete", f"Delete {patient.get('Full Name')}?"):
        if patient in backend.queue:
            backend.queue.remove(patient)
        elif patient in backend.processed_patients:
            backend.processed_patients.remove(patient)
        backend.save_data()
        refresh_all_patients_table()
        messagebox.showinfo("Deleted", "Patient record removed.")

tk.Button(action_frame, text="View", command=view_patient, bg="#2196F3", fg="white", width=8).pack(side="left", padx=5)
tk.Button(action_frame, text="Edit", command=edit_patient, bg="#FF9800", fg="white", width=8).pack(side="left", padx=5)
tk.Button(action_frame, text="Delete", command=delete_patient, bg="#F44336", fg="white", width=8).pack(side="left", padx=5)

def refresh_all_patients_table():
    for item in all_patients_tree.get_children():
        all_patients_tree.delete(item)
    all_patients = backend.queue + backend.processed_patients[-30:]
    for p in all_patients:
        reg_date = p.get("Check-In", "").split()[0] if p.get("Check-In") else "N/A"
        all_patients_tree.insert("", "end", values=(
            p.get("Ticket", ""),
            p.get("Full Name", ""),
            p.get("DOB", ""),
            p.get("Phone", ""),
            reg_date,
            p.get("Priority", "Normal"),
            p.get("Appointment Type", "")
        ))

def on_tab_change(event):
    tab_name = notebook.tab(notebook.select(), "text")
    if tab_name == "Dashboard":
        refresh_patient_table()
    elif tab_name == "Patients":
        refresh_all_patients_table()

notebook.bind("<<NotebookTabChanged>>", on_tab_change)

# Initial Load
backend.load_data(silent=True)
update_display()
refresh_all_patients_table()

root.mainloop()
