# Sky Engineering Registry

A Django web application built as part of the **5COSC021W Coursework 2** group project at the University of Westminster. The application serves as an internal engineering portal for a Sky, allowing authenticated users to browse departments, teams, send messages, schedule meetings, and view summary reports.

***

## Group Members

| Name | Module |
|------|--------|
| Andre Ferreira | Organisation / Department |
| Aung Myo Oo | Messaging |
| Aiman Chowdhury | Teams |
| Mursal Hassan | Reports |
| Nima Momenzadehjahromi | Schedule |

***

## Features

### Organisation
- Browse all departments with name, leader, and specialisation
- Search departments by name or specialisation
- Department detail page showing leader, teams table, and inter-team dependencies
- Teams listing with search across team name, manager, skills, and department

### Messaging
- Inbox, Sent, and Drafts folders
- Compose new messages with recipient pre-fill from the Teams page
- Mark messages as read/unread
- Delete messages

### Schedule
- Create new meeting records linked to a team
- View upcoming meetings

### Reports
- Summary dashboard showing total teams, departments, and users
- Highlights teams with no assigned manager
- Department breakdown with team counts
- Export report as **CSV** or **PDF**

### Shared / Auth
- Login required across the entire application
- Login and logout with redirect to department list
- Shared sidebar navigation with active-state highlighting
- Responsive layout (collapses on screens below 980 px)
- Django Admin panel with inline editing for all models

***

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 5.x |
| Database | SQLite (development) |
| Frontend | Custom CSS (no framework) |
| Auth | Django built-in `django.contrib.auth` |
| PDF export | ReportLab |
| Python | 3.12+ |

***

## Setup and Installation

### Prerequisites

- Python 3.12 or higher
- `pip`
- Git

### 1. Clone the repository

```bash
git clone https://github.com/ajxlf/sky-registry.git
cd sky-registry
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Load seed data

```bash
python manage.py loaddata organisation/fixtures/initial_data.json
```

### 6. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

***

## Running Tests

```bash
python manage.py test
```

Tests cover login/logout flows, authentication enforcement on protected views, and correct redirect behaviour.

***

## Admin Panel

Navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with superuser credentials to manage:

- Departments (with inline Team editing)
- Teams (with inline Dependency editing)
- Dependencies
- Messages
- Meetings

***

## Notes

- `db.sqlite3` is excluded from version control via `.gitignore`. Run migrations and load fixtures after cloning.
- The `SECRET_KEY` in `settings.py` is a development key only. In a production deployment it would be loaded from an environment variable.
- `DEBUG = True` is set for development. This must be set to `False` before any production deployment.
- PDF export requires the `reportlab` package, which is included in `requirements.txt`.
