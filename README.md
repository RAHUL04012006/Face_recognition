# Face Recognition Attendance System

A real-time face recognition system that automatically marks attendance using webcam. The system detects faces, matches them against known faces, and maintains attendance records in an Excel file.

![Face Detection Screenshot](Screenshot%202025-04-25%20123440.png)

## Features

- Real-time face detection and recognition
- Automatic attendance marking with timestamps
- Excel-based attendance tracking
- Support for multiple face records per person
- Logging system for tracking operations and errors

## Prerequisites

- Python 3.x
- OpenCV
- face_recognition
- pandas
- numpy

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Install required packages:
```bash
pip install opencv-python face-recognition pandas numpy
```

## Project Structure

```
.
├── people/                     # Directory containing face images
│   ├── Person1/
│   │   └── person1.jpg
│   └── Person2/
│       └── person2.jpg
├── Face_recognition.py        # Main program file
├── attendance.xlsx            # Attendance record file
├── haarcascade_frontalface_default.xml
└── README.md
```

## Usage

1. Add person images:
   - Create a folder with the person's name under the `people` directory
   - Add clear face images of the person in their respective folder

2. Run the program:
```bash
python Face_recognition.py
```

3. Press 'q' to quit the application

![Recognition Demo](Screenshot%202025-04-25%20123629.png)

## Features Details

- **Face Detection**: Uses OpenCV for real-time face detection
- **Face Recognition**: Implements face_recognition library for accurate face matching
- **Attendance System**: Automatically records attendance with timestamps in Excel
- **Error Handling**: Comprehensive logging system for debugging
- **Multiple Face Support**: Can handle multiple faces in the frame

## Contributing

Feel free to fork the project and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
