import supabase
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
# ✅ Supabase Config
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# ✅ Initialize Supabase Client
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🔗 Connecting to Supabase...")
print("🛠 Supabase URL:", SUPABASE_URL)
print("🔑 Supabase Key:", SUPABASE_KEY[:10] + "********")  # Hide for security

# ✅ Student Data with Parent Phone Numbers
students_data = [
    {
        "id": 1,
        "name": "std1",
        "major": "IT",
        "starting_year": 2021,
        "total_attendance": 7,
        "grade": "O",
        "year": 4,
        "last_attendance_time": "2023-01-10 12:30:00",
        "phone": "91**********",  # Student's Phone
        "parent_phone": "91**********"  # Parent's Phone
    },
    {
        "id": 2,
        "name": "std2",
        "major": "IT",
        "starting_year": 2020,
        "total_attendance": 0,
        "grade": "O",
        "year": 4,
        "last_attendance_time": "2023-01-10 11:30:00",
        "phone": "91**********",
        "parent_phone": "91**********"
    },
    {
        "id": 3,
        "name": "std3",
        "major": "IT",
        "starting_year": 2021,
        "total_attendance": 0,
        "grade": "O",
        "year": 4,
        "last_attendance_time": "2023-01-10 11:30:00",
        "phone": "91**********",
        "parent_phone": "91**********"
    },    
    {
        "id": 4,
        "name": "std4",
        "major": "IT",
        "starting_year": 2021,
        "total_attendance": 0,
        "grade": "O",
        "year": 4,
        "last_attendance_time": "2023-01-10 11:30:00",
        "phone": "91**********",
        "parent_phone": "91**********"
    }
]

# ✅ Insert Data into Supabase
try:
    response = supabase_client.table("students").upsert(students_data).execute()
    print("✅ Data Inserted Successfully!")
    
    if response.data:
        print("📦 Inserted Data:", response.data)  # Print response data

    if hasattr(response, 'error') and response.error:
        print("❌ Error:", response.error)

except Exception as e:
    print("🚨 Exception Occurred:", str(e))
