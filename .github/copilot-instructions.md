# 📱 Mobile Phone Sales Management Application

A Flask-based web application to manage the sales and inventory of mobile phones using IMEI tracking. Designed for businesses selling devices via cash or credit, with a role-based dashboard for Admin and Staff and optional RESTful API endpoints for integrations.

---

General Guidelines:
- Use Flask 3.1.1
- Use Python 3.13.3
- Always activate `.productivity` virtual environment before running the application or installing dependencies.

## 💼 Project Goals

- IMEI-based stock management (each device is identified by its IMEI).
- Role-based user access:
  - **Admin**: Full access to all data, inventory, and reporting.
  - **Staff**: Can only perform sales and view personal activity.
- Sales workflow:
  - Scan or enter IMEI.
  - Display device details.
  - Record sale with payment type (Cash or Credit), amount paid.
- Dashboards and reports:
  - Current inventory.
  - Staff performance.
  - Profit per device model.



mobile_sales_app/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── devices.py
│   │   ├── sales.py
│   │   └── reports.py
│   ├── templates/
│   ├── static/
│   └── forms.py
│
├── migrations/
├── .env
├── config.py
├── run.py
├── requirements.txt
└── README.md


## 🚀 Core Features## 💼 Project Goals

- IMEI-based stock management (each device is identified by its IMEI).
- Role-based user access:
  - **Admin**: Full access to all data, inventory, and reporting.
  - **Staff**: Can only perform sales and view personal activity.
- Sales workflow:
  - Scan or enter IMEI.
  - Display device details.
  - Record sale with payment type (Cash or Credit), amount paid.
- Dashboards and reports:
  - Current inventory.
  - Staff performance.
  - Profit per device model.


### 📦 IMEI-Based Stock Management
- Add new stock by scanning or entering IMEI numbers.
- Capture brand, model, purchase price, and date of arrival.
- Devices are marked as `available` or `sold`.

### 💳 Sales Workflow
- Staff scan an IMEI to start a sale.
- If the device exists and is available, show details and input:
  - Seller (logged-in user)
  - Sale price
  - Payment type: Cash or Credit
  - Amount paid (full or deposit)

### 📊 Admin Dashboard
- View current inventory, stock levels.
- Track profit per model and time period.
- Monitor staff performance and export detailed sales logs.

### 👥 User Roles
- **Admin**: Full access to inventory, sales reports, staff management.
- **Staff**: Can only perform sales and view personal sales activity.

---

## 🧰 Tech Stack

| Component        | Technology                    |
|------------------|-------------------------------|
| Backend          | Flask 2.x, Flask-SQLAlchemy   |
| Frontend         | HTML, Bootstrap 5             |
| REST API         | Flask-RESTful / Flask Blueprint API |
| Forms            | Flask-WTF                     |
| Auth             | Flask-Login, Flask-Bcrypt     |
| DB Migrations    | Flask-Migrate + Alembic       |
| Password Hashing | Flask-Bcrypt or Flask-Argon2  |
| IMEI Scanning    | Optional via QuaggaJS         |

---

## 🌐 REST API Endpoints

| Endpoint                        | Method | Role   | Description                                |
|--------------------------------|--------|--------|--------------------------------------------|
| `/api/login`                   | POST   | Public | Login and receive auth token               |
| `/api/devices`                 | GET    | Admin  | Get list of all devices                    |
| `/api/devices`                 | POST   | Admin  | Add a new device to inventory              |
| `/api/devices/<imei>`          | GET    | Staff  | Get details of a device by IMEI            |
| `/api/sales`                   | POST   | Staff  | Record a new sale for a device             |
| `/api/reports/summary`         | GET    | Admin  | Get summarized sales and profit data       |
| `/api/reports/staff/<user_id>` | GET    | Admin  | Get performance and sales by staff member  |

- Auth via token or session (JWT or Flask-Login session cookie).
- All API responses return JSON.

---

## 📦 Required Packages

```txt
Flask>=2.3
Flask-SQLAlchemy>=3.1
Flask-Migrate>=4.0
Flask-Login>=0.6
Flask-WTF>=1.1
Flask-Bcrypt
Flask-RESTful>=0.3.9
python-dotenv
email-validator
gunicorn

## ✅ Copilot Tasks

Copilot should:
- Follow Flask best practices (Blueprints, configs, security).
- Use SQLAlchemy with appropriate relationships:
  - One `User` has many `Sales`
  - One `Sale` has one `Device`
- Implement REST API routes with access control decorators.
- Use JWT or Flask-Login session-based auth.
- Ensure sales cannot be recorded for unavailable devices.
- Generate code that is modular, clear, and scalable.