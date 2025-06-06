
# 🎓 CSULB WAIV SMS – Student Management System

A Django-based web application developed for **California State University, Long Beach** (CSULB) WAIV program to manage student cases, documentation, disability information, service logs, and reporting efficiently.

---

## 📚 Key Features

- Student profile and case management
- Upload and manage documents (e.g. IEPs, evaluations)
- Track disability information
- Monthly client service logs and reporting
- Role-based access for counselors and admins
- Export reports (CSV/Excel)
- Admin panel for easy data management

---

## 🚀 Getting Started

These instructions will help you set up the development environment on your local machine.

### ✅ Prerequisites

- Python 3.10+
- pip
- Git
- Virtualenv (recommended)
- Microsoft SQL Server
- Django

---

### ⚙️ Local Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/workability-sa1/waiv.git
cd waiv
```

#### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file based on the example:

```bash
cp .env.example .env
```

Update `.env` with your own `SECRET_KEY`, `DEBUG`, and database settings.

#### 5. Apply Migrations and Seed Database

```bash
python manage.py migrate
```

#### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

#### 7. Run the Development Server

```bash
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/` to start using the app.

---

## 🧪 Running Tests

To run the unit tests:

```bash
python manage.py test
```

---

## 🛠 Technologies Used

- Django 4.x (Python 3.10+)
- Microsoft SQL Server
- HTML/CSS/JavaScript (or optional frontend framework)
- Git + GitHub
- Environment management via `.env`

---

## 📁 Project Structure Overview

```
waiv/
¦   manage.py
¦   README.md
+---cdcwaiv
¦   ¦   asgi.py
¦   ¦   settings.py
¦   ¦   urls.py
¦   ¦   wsgi.py
¦   ¦   __init__.py     
+---static
¦   ¦   ...
+---waivapp
    ¦   admin.py
    ¦   apps.py
    ¦   EmailBackEnd.py
    ¦   forms.py
    ¦   LoginCheckMiddleWare.py
    ¦   manager.py
    ¦   models.py
    ¦   StaffViews.py
    ¦   tests.py
    ¦   views.py
    ¦   __init__.py
    ¦   
    +---migrations
    ¦   ¦  ...
    ¦   +---__pycache__
    ¦	¦  ...
    ¦           
    +---static
    ¦   +---dist
    ¦	¦   ...
    ¦   +---plugins
    ¦	¦   ...
    ¦               
    +---templates
    ¦   ¦   demo.html
    ¦   ¦   login_page.html
    ¦   ¦   
    ¦   +---manager_template
    ¦   ¦       add_counseling_template.html
    ¦   ¦       add_staff_template.html
    ¦   ¦       add_student_template.html
    ¦   ¦       base_template.html
    ¦   ¦       create_monthly_report.html
    ¦   ¦       edit_staff_template.html
    ¦   ¦       edit_student_template.html
    ¦   ¦       footer.html
    ¦   ¦       form_template.html
    ¦   ¦       home_content.html
    ¦   ¦       import_monthly_client_log.html
    ¦   ¦       manage_staff_template.html
    ¦   ¦       manage_student_template.html
    ¦   ¦       monthly_client_listing.html
    ¦   ¦       monthly_report_detail.html
    ¦   ¦       monthly_report_pdf.html
    ¦   ¦       sidebar_template.html
    ¦   ¦       view_counseling_template.html
    ¦   ¦       
    ¦   +---staff_template
    ¦           add_counseling_template.html
    ¦           base_template.html
    ¦           edit_student_template.html
    ¦           footer.html
    ¦           manage_student_template.html
    ¦           sidebar_template.html
    ¦           staff_home_template.html
    ¦           view_counseling_template.html
    ¦           
    +---__pycache__
```

---

## 🤝 Contributing

This is a private academic project. Collaborators must be approved by the project lead.

---

## 📜 License

This project is intended for internal academic use and is not licensed for public distribution.

---

## 👨‍💻 Maintainers

Developer: **[Mark Le]**  
CSULB WAIV Team, California State University, Long Beach