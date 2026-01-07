# Student Database Management System (Django)

A role-based Student Database Management System built using **Django**, featuring secure authentication, authorization, and complete CRUD operations.  
Designed to demonstrate practical backend development skills using Python and Django.

---

## 🚀 Features

### 1. **Authentication**
- User registration  
- Secure login and logout  
- Password hashing (Django auth)  
- Session-based authentication  

### 2. **Role-Based Authorization**
- **Admin**
  - Add, update, and delete courses  
  - Manage student profiles  
  - Add, delete users   

- **Teacher**
  - Create courses  
  - Manage enrolled students  

- **Student**
  - View own profile  
  - View enrolled courses  

### 3. **CRUD Operations**
- **Students**  
- **Courses**  
- **Enrollments**  

All CRUD actions are controlled with proper permission checks.

---

## 🛠️ Tech Stack

- **Python 3**  
- **Django**  
- **SQLite / PostgreSQL (Optional)**  
- **HTML, CSS, JavaScript**  
- **Bootstrap**  
- **Git / GitHub**

---
## ▶️ Running the Project Locally

```bash
git clone https://github.com/your-username/student-dbms.git
cd student-dbms

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
