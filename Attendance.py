import sqlite3
import cv2
import face_recognition
import time
from datetime import datetime
import numpy as np

# Connect to SQLite database
conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
cursor = conn.cursor()

# Retrieve student records
cursor.execute("SELECT * FROM appdata_admission")
rows = cursor.fetchall()

# Initialize face encodings and names
known_face_encodings = []
known_face_names = []
ids = []

# Load student images
for row in rows:
    ids.append(row[0])  # Student ID
    known_face_names.append(row[1])  # Student Name
    image_path = "media/" + str(row[13])  # Image Path from Database

    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_face_encodings.append(encodings[0])
        else:
            print(f"Warning: No face detected in {image_path}")

    except Exception as e:
        print(f"Error loading image {image_path}: {e}")

# Set face match threshold
MATCH_THRESHOLD = 0.5

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame.")
        break

    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        name = "Unknown"
        id1 = None

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            best_match_distance = face_distances[best_match_index]

            if best_match_distance < MATCH_THRESHOLD:
                name = known_face_names[best_match_index]
                id1 = ids[best_match_index]

                dt = str(datetime.now())
                today_date = datetime.now().strftime("%Y-%m-%d")
                time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("SELECT * FROM appdata_settime")
                rec = cursor.fetchone()

                if rec:
                    db_time = datetime.strptime(str(rec[1]), "%Y-%m-%d %H:%M:%S")
                    time1 = datetime.strptime(str(time1), "%Y-%m-%d %H:%M:%S")

                    cursor.execute("SELECT * FROM appdata_admission WHERE id = ?", (id1,))
                    row = cursor.fetchone()

                    if row:
                        course = row[9]
                        deg = row[14]
                        dept = row[10]
                        batch = row[15]
                        print(course, ",", deg, ",", dept, ",", batch)

                        if db_time < time1:
                            print("Late Attendance - Not OK")
                        else:
                            print("On Time - OK")

                    cursor.execute("SELECT * FROM appdata_attendance WHERE admission_id = ? AND dt LIKE ?", 
                                   (id1, today_date + "%"))
                    existing_record = cursor.fetchone()

                    if existing_record:
                        print("Record already exists for today!")
                    else:
                        dt1 = today_date  # Ensure dt1 is properly stored
                        cursor.execute("INSERT INTO appdata_attendance (admission_id, dt, course, deg, dept, batch, dt1) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                                       (str(id1), dt, course, deg, dept, batch, dt1))
                        conn.commit()
                        print(f"Attendance marked for {name}.")

        # Draw rectangle around detected face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
conn.close()
