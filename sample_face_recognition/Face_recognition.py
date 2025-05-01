import os
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import face_recognition
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FaceRecognitionSystem:
    def __init__(self, base_path='people', attendance_file='attendance.xlsx'):
        self.base_path = base_path
        self.attendance_file = attendance_file
        self.known_encodings = []
        self.known_names = []
        self.attendance_df = self._initialize_attendance()
        self.cap = None

    def _initialize_attendance(self):
        """Initialize or load the attendance DataFrame."""
        try:
            if os.path.exists(self.attendance_file):
                return pd.read_excel(self.attendance_file)
            return pd.DataFrame(columns=["Name", "Time"])
        except Exception as e:
            logging.error(f"Error initializing attendance: {e}")
            return pd.DataFrame(columns=["Name", "Time"])

    def load_known_faces(self):
        """Load known face encodings from the base directory."""
        try:
            for student_folder in os.listdir(self.base_path):
                student_path = os.path.join(self.base_path, student_folder)
                if os.path.isdir(student_path):
                    for image_name in os.listdir(student_path):
                        image_path = os.path.join(student_path, image_name)
                        try:
                            image = face_recognition.load_image_file(image_path)
                            face_encodings = face_recognition.face_encodings(image)

                            if len(face_encodings) == 1:  # Only use images with one face
                                encoding = face_encodings[0]
                                self.known_encodings.append(encoding)
                                self.known_names.append(student_folder)
                                logging.info(f"Successfully loaded face for {student_folder}")
                        except Exception as e:
                            logging.warning(f"Error processing image {image_path}: {e}")
                            continue
        except Exception as e:
            logging.error(f"Error loading known faces: {e}")

    def mark_attendance(self, name):
        """Mark attendance for a recognized person."""
        try:
            if name not in self.attendance_df['Name'].values:
                time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_entry = pd.DataFrame({'Name': [name], 'Time': [time_now]})
                self.attendance_df = pd.concat([self.attendance_df, new_entry], ignore_index=True)
                
                with pd.ExcelWriter(self.attendance_file, engine='openpyxl', mode='w') as writer:
                    self.attendance_df.to_excel(writer, index=False)
                
                logging.info(f'Attendance marked for {name}')
        except Exception as e:
            logging.error(f"Error marking attendance: {e}")

    def process_frame(self, frame):
        """Process a single frame for face recognition."""
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = self.known_names[best_match_index]
                    self.mark_attendance(name)

                    # Draw rectangle and label
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, name, (left, top - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 165, 255), 2)

            return frame
        except Exception as e:
            logging.error(f"Error processing frame: {e}")
            return frame

    def run(self):
        """Run the face recognition system."""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Could not open webcam")

            self.load_known_faces()
            logging.info("Starting face recognition system...")

            while True:
                ret, frame = self.cap.read()
                if not ret:
                    logging.error("Failed to grab frame")
                    break

                frame = self.process_frame(frame)
                cv2.imshow('Face Recognition', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except Exception as e:
            logging.error(f"Error in face recognition system: {e}")
        finally:
            if self.cap is not None:
                self.cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    face_system = FaceRecognitionSystem()
    face_system.run()















