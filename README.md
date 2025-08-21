# Smart Attendance System with Face Recognition & SMS Alert

**Final Year Project**

---

## 🎯 Project Overview

A smart attendance system that automatically marks attendance using face recognition and sends SMS alerts when attendance is logged. Ideal for schools, colleges, and offices to reduce manual work and prevent proxy attendance.

---

## ✅ Features

* **Real-time Face Recognition** using webcam
* **Automatic Attendance Logging** in a secure database
* **Instant SMS Notifications** via Twilio
* **Reduced Human Error** and enhanced efficiency

---

## 🛠️ Architecture & Approach

1. **Face Detection & Recognition**

   * Capture live video via webcam
   * Use the `face_recognition` and OpenCV libraries to identify registered faces

2. **Backend & Storage**

   * Manage authenticated users and attendance logs using Supabase (includes secure database and file storage)

3. **SMS Alerts**

   * Send SMS notifications through Twilio API when students are absent

---

## 📈 Insights & Outcomes

* High accuracy in attendance detection
* Prevents fake or duplicate attendance
* Real-time alerts boost transparency for admins or parents
* Scalable structure → useful for multiple users or institutions

---

## ✅ Conclusion

This project demonstrates how AI-powered automation can streamline administrative tasks like attendance tracking. It offers hands‑on experience in integrating facial recognition, database backend, and SMS-based notification systems.

---

## 🔧 Tools & Technologies

| Component         | Technology / Library       |
| ----------------- | -------------------------- |
| Programming       | Python                     |
| Face Recognition  | OpenCV, `face_recognition` |
| Backend & Storage | Supabase                   |
| SMS Service       | Twilio API                 |
| Optional UI       | Tkinter or Streamlit       |

---

## 🛠️ Installation & Usage

1. **Clone the repository:**

```bash
git clone https://github.com/Saranya294/smart_attendance_system.git
cd smart_attendance_system
```

2. **Set up a virtual environment & install dependencies:**

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up Supabase backend:**

* Go to [https://supabase.io](https://supabase.io) and create a new project
* Create a table (e.g., `students`) with columns like `id`, `name`, `attendance`, `image`, `phone`
* Add your Supabase `URL`, `API key`, and `bucket name` to a `.env` file or config section

4. **Configure Twilio for SMS:**

* Register at [https://twilio.com](https://twilio.com)
* Get your Twilio `SID`, `Auth Token`, and `Phone Number`
* Add them to `.env`

5. **Add student face images:**

* Place images inside the `Images/` folder
* Make sure each file is named as per student ID or roll number

6. **Run the encoder to generate face encodings:**

```bash
python encodeGenerator.py
```

7. **Start attendance system:**

```bash
python main.py
```

8. **Admin login via UI (if using Streamlit or Tkinter):**

* Start the UI script (`admin.py` or `app.py`)
* Enter your admin credentials to begin the session

---

## 📂 Folder Structure (Example)

```
├── Images/                # Student face images
├── encodeGenerator.py     # Face encoding generator
├── main.py                # Main attendance logic
├── send_sms.py            # SMS sending logic
├── .env                   # Supabase and Twilio credentials
├── requirements.txt       # Python libraries
├── README.md              # Project documentation
```

---

## 📌 Configuration (.env format)

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_password
```
---

## 👩‍💻 Contributors

* **Saranya S** – [saranyasubiramani29@gmail.com](mailto:saranyasubiramani29@gmail.com)
* Other collaborators Poorani R and Yamuna D

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♀️ Contact

For questions, feedback, or contributions:
📧 **Email:** [saranyasubiramani29@gmail.com](mailto:saranyasubiramani29@gmail.com)
🔗 **GitHub:** [github.com/Saranya294](https://github.com/Saranya294)

---
## 🙏 Acknowledgement

This project was inspired by and adapted from the open-source project:  
[Smart-Attendance-Marking-System by Soumyadeep Mukherjee](https://github.com/SoumyadeepMukherjee/Smart-Attendance-Marking-System)  

We thank the original author for providing the base implementation, which helped us build and customize our final year project.

