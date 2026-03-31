# 📚 Library Management System (FastAPI + PostgreSQL)

A backend system designed to streamline library operations for librarians while allowing students to interact with the system efficiently.

Built using **FastAPI** and **PostgreSQL**, this project simulates real-world library workflows including book issuing, returns, waitlists, and fine calculation.

---

## 🚀 Features

### 👤 Authentication & Roles

* JWT-based authentication
* Role-based access:

  * Librarian
  * Student

---

### 📖 Book Management (Librarian)

* Add, update, delete books
* Manage multiple copies
* Track availability

---

### 🔄 Issue & Return System

* Issue books with a **7-day return policy**
* Automatic due date calculation
* Return tracking
* Fine calculation: **₹5 per day (late returns)**

---

### ⏳ Waitlist System

* Students can join waitlist when book is unavailable
* Automatic allocation when a book is returned

---

### 🔍 Student Features

* View all books
* Check availability
* View expected return dates
* Request new books

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Authentication:** JWT (JSON Web Tokens)

---

## 📂 Project Structure

```
Library-MS/
│
├── App/
│   ├── api/
│   ├── core/
│   ├── crud/
│   ├── db/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── Docs/
├── .gitignore
├── README.md
└── LICENSE
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/SSRyadav-22/Library-MS.git
cd Library-MS
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file:

```
DATABASE_URL=your_postgres_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 5. Run the server

```bash
uvicorn App.main:app --reload
```

---

## 🔐 Authentication Flow

1. User logs in → receives JWT token
2. Token is used in headers:

```
Authorization: Bearer <token>
```

3. Backend validates token and role before allowing access

---

## 📌 API Modules

* `/auth` → Login & authentication
* `/books` → Book management
* `/issues` → Issue & return logic
* `/waitlist` → Queue system
* `/users` → User management

---

## ⚠️ Important Notes

* `.env` is not included for security reasons
* Fine calculation is enforced (₹5/day)
* System designed for real-world scalability

---

## 👨‍💻 Author

**S. Sai Rahual**

* AI & ML Engineering Student
* Backend & ML Developer

---

## ⭐ Future Improvements

* Email/notification system
* Admin dashboard UI
* Analytics & reporting
* Barcode/QR integration
