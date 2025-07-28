from dotenv import load_dotenv
import os
import cv2
import pickle
import cvzone
import face_recognition
import numpy as np
import requests
from datetime import datetime
from supabase import create_client

load_dotenv()
# Supabase setup
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load background and mode images
imgBackground = cv2.imread(r'C:\Users\**********\OneDrive\Desktop\Smart-Attendance-Marking-System\Smart-Attendance-Marking-System\Resources\background.png')
folderModePath = r'C:\Users\**********\OneDrive\Desktop\Smart-Attendance-Marking-System\Smart-Attendance-Marking-System\Resources\Modes'
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in os.listdir(folderModePath)]

# Load encodings
print("Loading Encode File...")
with open(r'C:\Users\**********\OneDrive\Desktop\Smart-Attendance-Marking-System\EncodeFile.p', 'rb') as file:
    encodeListKnown, studentIds = pickle.load(file)
print("Encode File Loaded...")

modeType = 0
counter = 0
id = -1
imgStudent = []
student_images = {}
studentInfo = {}

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror the camera
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

    if faceCurrFrame:
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            threshold = 0.5  # You can adjust if needed

            if faceDis[matchIndex] < threshold:
                id = studentIds[matchIndex]
                response = supabase.table("students").select("*").eq("id", id).execute()
                studentInfo = response.data[0] if response.data else None

                if not studentInfo:
                    print(f"Error: Student with ID {id} not found in Supabase.")
                    continue

                name = studentInfo['name'].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                cv2.putText(imgBackground, name, (x1, y2 + 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Smart Attendance System", imgBackground)
                    counter = 1
                    modeType = 1
                    cv2.waitKey(1)

            else:
                print("❌ Unknown Face Detected – Attendance Not Marked")
                modeType = 0  # fallback to default mode
                counter = 0
                cvzone.putTextRect(imgBackground, "Unknown Face", (275, 400), scale=1.5, thickness=2)
                continue

 
        if counter != 0:
            if counter == 1:
                try:
                    last_attendance_time = datetime.strptime(studentInfo['last_attendance_time'][:26], "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    last_attendance_time = datetime.strptime(studentInfo['last_attendance_time'][:19], "%Y-%m-%dT%H:%M:%S")
                secondsElapsed = (datetime.now() - last_attendance_time).total_seconds()

                if id not in student_images:
                    try:
                        response = supabase.storage.from_("students-images").create_signed_url(f"{id}.jpg", 3600)
                        if response and "signedURL" in response:
                            signed_url = response["signedURL"]
                            image_response = requests.get(signed_url)
                            if image_response.status_code == 200:
                                array = np.frombuffer(image_response.content, np.uint8)
                                student_images[id] = cv2.imdecode(array, cv2.IMREAD_COLOR)
                            else:
                                student_images[id] = np.zeros((216, 216, 3), dtype=np.uint8)
                        else:
                            student_images[id] = np.zeros((216, 216, 3), dtype=np.uint8)
                    except Exception as e:
                        print(f"Exception fetching image: {e}")
                        student_images[id] = np.zeros((216, 216, 3), dtype=np.uint8)

                imgStudent = student_images[id]
                today_date = datetime.now().date()

                try:
                    last_attendance_date = datetime.strptime(studentInfo['last_attendance_time'][:10], "%Y-%m-%d").date()
                except ValueError:
                    last_attendance_date = None

                if last_attendance_date != today_date:
                    studentInfo['total_attendance'] += 1
                    supabase.table("students").update({
                        "total_attendance": studentInfo['total_attendance'],
                        "last_attendance_time": datetime.now().isoformat()
                    }).eq("id", id).execute()
                    print(f"✅ Attendance marked for {studentInfo['name']}")
                else:
                    print(f"❌ Attendance already marked today for {studentInfo['name']}")
                    modeType = 3
                    counter = 0
                    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

            if modeType != 3:
                if 20 < counter < 40:
                    modeType = 2
                imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

                if counter <= 20:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    if imgStudent is not None:
                        imgStudent = cv2.resize(imgStudent, (216, 216))
                        imgBackground[175:175+216, 909:909+216] = imgStudent

                counter += 1
                if counter >= 40:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    cv2.imshow("Smart Attendance System", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Smart Attendance System", cv2.WND_PROP_VISIBLE) < 1:
        print("Closing Camera...")
        break

cap.release()
cv2.destroyAllWindows()
