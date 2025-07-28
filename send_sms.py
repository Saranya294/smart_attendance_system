from supabase import create_client
from twilio.rest import Client
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# ✅ Twilio Config
TWILIO_ACCOUNT_SID =os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN =os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER =os.getenv('TWILIO_FROM_NUMBER')

# ✅ Supabase Config
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# ✅ Initialize Clients
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ✅ Get Today's Date
today_date = datetime.now().strftime("%Y-%m-%d")

# ✅ Fetch Students' Attendance Data
try:
    response = supabase_client.table("students").select("id, name, parent_phone, total_attendance, last_attendance_time").execute()
    students = response.data if response.data else []
except Exception as e:
    print("🚨 Error fetching data:", str(e))
    students = []

# ✅ Identify Absent Students & Notify Parents
for student in students:
    student_id = student["id"]
    name = student["name"]
    parent_phone = student["parent_phone"]
    last_attendance_time = student["last_attendance_time"]

    # Convert last attendance time to a datetime object
    try:
        last_attendance_date = datetime.fromisoformat(last_attendance_time).date()
    except Exception:
        print(f"❌ Invalid date format for {name}")
        continue

    # ✅ Check if the student is absent today
    if last_attendance_date < datetime.now().date():
        message_body = f"Dear Parent, your child {name} was absent on {today_date}. Please ensure their regular attendance."

        # ✅ Send SMS via Twilio
        try:
            message = twilio_client.messages.create(
                from_=TWILIO_FROM_NUMBER,
                body=message_body,
                to=f"+{parent_phone}"  # Ensure correct phone format
            )
            print(f"📩 SMS sent to {name}'s parent ({parent_phone}): {message.sid}")
        except Exception as e:
            print(f"❌ Failed to send SMS to {parent_phone}: {str(e)}")
