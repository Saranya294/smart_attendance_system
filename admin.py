import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# ✅ Define the correct directory
PROJECT_DIR = r"your project directory"

# ✅ Admin Password
ADMIN_PASSWORD = "Admin@IT"

# ✅ Function to Validate Login
def check_login():
    if password_entry.get() == ADMIN_PASSWORD:
        login_window.destroy()  # Close login window
        open_attendance_ui()
    else:
        messagebox.showerror("Error", "Incorrect Password!")

# ✅ Function to Open Attendance UI
def open_attendance_ui():
    attendance_window = tk.Tk()
    attendance_window.title("Smart Attendance System")
    attendance_window.geometry("400x300")

    # ✅ Welcome Message
    tk.Label(attendance_window, text="Hello Admin 👋", font=("Arial", 14)).pack(pady=20)

    # ✅ Start Attendance Button
    def start_attendance():
        messagebox.showinfo("Attendance", "Starting attendance...")

        try:
            subprocess.run([
                r"C:\Users\*****\OneDrive\Desktop\Smart-Attendance-Marking-System\.venv\Scripts\python.exe",
                os.path.join(PROJECT_DIR, "main.py")
            ], check=True, cwd=PROJECT_DIR)

            messagebox.showinfo("Attendance", "Attendance Completed ✅")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to run attendance script!")

        attendance_window.destroy()
        open_send_sms_ui()  # ✅ Go to SMS UI

    tk.Button(attendance_window, text="📷 Start Attendance", font=("Arial", 12), command=start_attendance).pack(pady=10)

    # ✅ Function to open SMS UI
    def open_send_sms_ui():
        sms_window = tk.Tk()
        sms_window.title("Send Absence Notifications")
        sms_window.geometry("400x200")

        tk.Label(sms_window, text="Send Absence Notification?", font=("Arial", 12)).pack(pady=20)

        # ✅ Confirm Send SMS
        def send_sms():
            messagebox.showinfo("SMS", "Sending SMS to parents...")

            try:
                subprocess.run([
                    r"C:\Users\***\OneDrive\Desktop\Smart-Attendance-Marking-System\.venv\Scripts\python.exe",
                    os.path.join(PROJECT_DIR, "send_sms.py")
                ], check=True, cwd=PROJECT_DIR)

                messagebox.showinfo("SMS", "SMS Sent Successfully ✅")
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Failed to send SMS!")

            sms_window.destroy()

        tk.Button(sms_window, text="📩 Send SMS", font=("Arial", 12), command=send_sms).pack(pady=10)
        sms_window.mainloop()

    attendance_window.mainloop()

# ✅ Create Login UI
login_window = tk.Tk()
login_window.title("Admin Login")
login_window.geometry("300x200")

tk.Label(login_window, text="🔑 Enter Admin Password:", font=("Arial", 12)).pack(pady=10)
password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
password_entry.pack(pady=5)

tk.Button(login_window, text="Login", font=("Arial", 12), command=check_login).pack(pady=10)

# ✅ Start the main login loop
login_window.mainloop()
