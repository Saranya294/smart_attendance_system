import cv2
import face_recognition
import pickle
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()
# ✅ Supabase Config
SUPABASE_URL = os.getenv('SUPABASE_URL ')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Importing the student images
folderPath = r'C:\Users\*****\OneDrive\Desktop\Smart-Attendance-Marking-System\Smart-Attendance-Marking-System\Images'
pathList = os.listdir(folderPath)  # List of images
imgList = []
studentIds = []

# Uploading images to Supabase Storage
bucket_name = "students-images"

for path in pathList:
    file_path = os.path.join(folderPath, path)
    imgList.append(cv2.imread(file_path))
    student_id = os.path.splitext(path)[0]
    studentIds.append(student_id)

    with open(file_path, "rb") as f:
        response = supabase.storage.from_(bucket_name).upload(path, f, {"content-type": "image/jpeg"})

    if response:
        print(f"Uploaded {path} to Supabase")

print(studentIds)

# Function to find encodings
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
        encode = face_recognition.face_encodings(img)[0]  # Extract face encoding
        encodeList.append(encode)
    return encodeList

print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

# Save encoding data to a pickle file
with open("EncodeFile.p", "wb") as file:
    pickle.dump(encodeListKnownWithIds, file)

print("File saved: EncodeFile.p")
