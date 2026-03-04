# QuizApp - Flask Quiz Platform

A web-based quiz platform built with **Flask** where users can create quizzes, add questions, attempt quizzes, and track their performance through an analytics dashboard.

---

## Features

- User authentication (Login / Logout)
- Create quizzes
- Add multiple-choice questions
- Attempt quizzes
- Score calculation
- Quiz attempt history
- Dashboard analytics
- Performance chart
- Delete quizzes
- Responsive UI

---

## Dashboard Analytics

The dashboard provides real-time analytics including:

- Total quizzes created
- Total quiz attempts
- Average score percentage
- Best score achieved
- Performance trend chart

---

## Tech Stack

### Backend
- Python
- Flask
- SQLAlchemy
- SQLite

### Frontend
- HTML
- CSS
- Bootstrap
- Chart.js

---

## Project Structure
quiz_app/
│
├── app/
│ ├── models.py
│ ├── routes.py
│ ├── init.py
│
├── templates/
│ ├── dashboard.html
│ ├── login.html
│ ├── quiz.html
│
├── static/
│ ├── css/
│ │ └── style.css
│
├── app.py
├── requirements.txt
└── README.md


---


---

## Installation

Installation and Running the Project

Follow the steps below to run the project locally.

1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
2. Move into the Project Folder
cd YOUR_REPOSITORY_NAME
3. Create a Virtual Environment (Optional but Recommended)

Windows:

python -m venv venv
venv\Scripts\activate

Mac/Linux:

python3 -m venv venv
source venv/bin/activate
4. Install Required Dependencies
pip install -r requirements.txt
5. Run the Application
python app.py
6. Open in Browser

Go to:

http://127.0.0.1:5000