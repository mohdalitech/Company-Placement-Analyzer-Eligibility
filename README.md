# 🚀 Company Placement Eligibility Analyzer & Skill Assessment Suite

An interactive multi-page **Streamlit** web application integrated with a **MySQL** database designed to help university students check company placement eligibility, analyze resumes against target job requirements, and evaluate technical/aptitude skills through structured quizzes.

---

## 🌟 Key Features

1. **User Authentication & Onboarding (`app.py`)**
   * Support for **New User Registration** with unique ID generation and automated verification code delivery via WhatsApp (`pywhatkit).
   * Secure **Existing User Login** with session state persistence.

2. **Academic & Company Eligibility Checker (`academic.py`)**
   * Collects academic parameters (CGPA, percentage, backlogs, branch.
   * Evaluates student eligibility dynamically against top recruiters (TCS, Wipro, Infosys, Accenture, Google).

3. **Resume Parsing & Skill Gap Analysis (`profile.py`)**
   * PDF resume upload and text extraction using `pypdf`.
   * Regular Expression (`re`) pattern matching to automatically detect technical skills, certifications, projects, and technologies.
   * Compares student profiles with company requirements to identify missing skills, technologies, or projects.

4. **Multi-Tab Skill Assessment Quiz (`ques.py`)**
   * Interactive assessments categorized across 4 tabs: **Aptitude Assessment**, **Technical MCQs**, **Programming**, and **SQL Assessment**.
   * Instant response validation, score calculation out of 60, and detailed performance breakdown.

5. **Competitiveness & Placement Analytics (`analysis.py`)**
   * Comprehensive dashboard summarizing eligibility status, resume feedback, and quiz performance metrics.

---

## 🛠️ Tech Stack

* **Frontend & Framework:** : Streamlit
* **Database Management:** : MySQL
* **PDF Processing:** : pypdf
* **Automation & Messaging:** : pywhatkit
* **Text Processing:** Python Regular Expressions : re 

---
👨‍💻 Author

Mohd Ali

🌐 GitHub: https://github.com/mohdalitech
💼 LinkedIn: Mohd Ali
📧 Email: mohdalii1923@gmail.com

Contributions, issues, and feature requests are welcome!
