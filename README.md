# Sakartvelo — Spice Online Store

Sakartvelo is an e-commerce platform specializing in authentic, high-quality Georgian products including traditional spices, artisan cheeses, sauces, and natural wines. Built with a robust Django backend and a modern Bootstrap 4 user interface, the platform offers clean user authentication, streamlined catalog tracking, and scalable performance.

---

## 🚀 Technical Stack & Architecture

- **Backend Framework:** Django (Python 3.13+)
- **Frontend Engine:** HTML5, CSS3, JavaScript, Bootstrap 4
- **Code Linter / Quality Controls:** Flake8 Configuration Engine
- **Data Layer Management:** Django ORM with native relational integrity validations (`models.PROTECT`)

---

## 🛠️ Installation & Local Setup Guide

Follow these steps to spin up the local development engine:

### 1. Clone the Repository
```bash
git clone <repository-url>
cd sakartvelo-django
```

### 2. Configure Your Virtual Environment
```bash
# Create the local isolation box
python -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(If you are setting up a clean install, run `pip install django black flake8`)*

### 4. Database Initialization & Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser Account
```bash
python manage.py createsuperuser
```

### 6. Boot Up the Server
```bash
python manage.py runserver
```
Visit the running application at `http://127.0.0`.

---

## ⚙️ Development Standards & Linting

We enforce clean, readable Python code standards across our architecture via **Flake8**. Project configurations exclude vendor packages (`.venv`) and auto-generated code records (`migrations`).

To manually trigger code scanning routines across the project base, run:
```bash
flake8 .
```

---

## 🌿 Branching Strategy & Git Protocol

- **`main`**: Production-ready, stable releases.
- **`develop`**: Main integration sandbox branch for all functional additions.
- **Feature Branches:** Created from `develop` following the standard naming scheme `feature/your-feature-name`. All updates are integrated back via formal Pull Requests (PRs) into `develop`.

