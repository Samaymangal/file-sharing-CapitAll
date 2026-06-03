# 📁 VDR_PROJECT_CAPITAL

> A secure **Virtual Data Room (VDR)** built with Django — designed for internal teams to store, organize, and manage files and folders with user & group-based access control.

---

## 📌 About the Project

**VDR_PROJECT_CAPITAL** is an internal file management system that allows organizations to securely store and organize documents. Team members can be grouped together, and access to files and folders can be managed at a user or group level — making it ideal for capital market operations, deal management, or any team that needs a private, organized document repository.

---

## ✨ Features

- 📂 **File & Folder Management** — Upload, organize, and manage files inside structured folders
- 👥 **User Management** — Create and manage internal user accounts
- 🏷️ **Group Management** — Organize users into groups for easier access control
- 🔐 **Access Control** — Restrict file/folder access by user or group
- 💾 **Internal Storage** — All files are stored securely within the application
- 🖥️ **Django Admin Panel** — Full admin interface for managing all data
- 📱 **Media Uploads** — Dedicated media/uploads directory for all uploaded content

---

## 🗂️ Project Structure

```
VDR_PROJECT_CAPITAL/
│
├── vdr_project/          # Core Django app (settings, urls, wsgi)
├── documents/            # App handling files & folders
├── uploads/              # User-uploaded files
├── media/uploads/        # Media storage directory
├── manage.py             # Django management script
└── db.sqlite3            # SQLite database
```

---

## ⚙️ Setup & Installation

### Prerequisites

Make sure you have the following installed:
- Python 3.8+
- pip
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/Samaymangal/VDR_PROJECT_CAPITAL.git
cd VDR_PROJECT_CAPITAL
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` doesn't exist yet, install manually:
> ```bash
> pip install django
> ```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and go to:
- 🌐 App → [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 🔧 Admin Panel → [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 👤 Default Admin Access

After running `createsuperuser`, log in at `/admin` to:
- Add / manage users
- Create groups and assign users
- Upload and manage files & folders

---

## 🛠️ Built With

| Technology | Purpose |
|---|---|
| [Django](https://www.djangoproject.com/) | Backend web framework |
| SQLite | Database (development) |
| Python 3 | Core language |
| HTML/CSS | Frontend templates |

---

## 📦 Deployment Notes

For production use, consider:
- Switching from SQLite to **PostgreSQL** or **MySQL**
- Setting `DEBUG = False` in `settings.py`
- Configuring a proper `SECRET_KEY` via environment variables
- Using **Gunicorn** + **Nginx** for serving

---

## 👨‍💻 Author

**Samaymangal**
GitHub: [@Samaymangal](https://github.com/Samaymangal)

---

## 📄 License

This project is for **internal use only**. Not licensed for public distribution.
