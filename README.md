# Quiz Master - V1

## 📌 Project Overview
Quiz Master - V1 is a Flask-based multi-user exam preparation platform designed for students to practice quizzes while an admin (Quiz Master) manages the questions and tracks user performance. This project is developed as part of the **Modern Application Development I** course.

## 🚀 Features
- **User Accounts**: Users can register, log in, and attempt quizzes.
- **Admin Panel**: The Quiz Master can create, edit, and delete quizzes.
- **Timed Quizzes**: Users must complete quizzes within a set time limit.
- **Score Tracking**: Users can view their quiz scores and progress.
- **Responsive UI**: Built with Jinja2, HTML, CSS, and Bootstrap for a smooth experience.
- **Database Storage**: SQLite is used to store users, quizzes, and scores.

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: Jinja2, HTML, CSS, Bootstrap
- **Database**: SQLite
- **Version Control**: Git & GitHub

## 🎯 Installation & Setup
### Prerequisites
Ensure you have **Python 3.7+** and **pip** installed on your system.

### Steps to Run the Project
1. **Clone the repository**
   ```bash
   git clone https://github.com/24f100556/Quiz-Master-V1-Mad-1.git
   cd quiz-master-v1
   ```
2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**
   ```bash
   python app.py or flask run
   ```
5. Open **http://127.0.0.1:5000/** in your browser.

## 📝 Usage Instructions
- **Users**: Sign up, log in, and start taking quizzes.
- **Admins**: Log in as an admin, manage quizzes, and track user scores.

<!-- ## 📌 Project Structure
```
quiz-master-v1/
│-- app.py           # Main application script
│-- templates/       # HTML templates (Jinja2)
│-- static/          # CSS, JS, and images
│-- database.db      # SQLite database
│-- requirements.txt # Dependencies
│-- README.md        # Project documentation
``` -->

## 🏆 Future Enhancements
- **Leaderboard for top users**
- **Multiple-choice and short-answer questions**
- **Export quiz results as PDF/CSV**
- **Mobile-friendly UI improvements**

<!-- ## 📜 License
This project is licensed under the MIT License.

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repo, create a new branch, and submit a pull request.

## 📩 Contact
For any queries, feel free to reach out or open an issue.


