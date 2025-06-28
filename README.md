
#  Device Health Monitoring System

A clean and beginner-friendly **Flask web application** for managing and monitoring IoT devices. Built as part of a Python learning journey, this project lets users securely register, log in, manage their own devices, and log diagnostics like CPU and memory usage — all with a simple UI and useful features.

---

##  What This App Does

This app is designed for people who want to:

- 🔐 Register and log in with a secure system  
- 🛠️ Create and manage IoT devices (name, location, type, status)  
- 📊 Log device diagnostics (CPU, memory usage, timestamp)  
- 🔎 Sort and filter data to find what matters  
- 💬 Get instant feedback with flash messages  
- 🎨 Navigate easily with a responsive Bootstrap-powered UI  

No need for complicated setups or APIs — just run the app and start managing your data.

---

## 📁 Project Folder Structure

```

FLASK PROJECT/
├── app/
│   ├── **init**.py             # App setup and JWT config
│   ├── models.py               # Database models
│   ├── utils.py                # Logging setup
│   ├── schemas.py              # Marshmallow validation schemas
│   ├── templates/              # HTML pages (Bootstrap)
│   └── routes/
│       ├── main.py             # Home page and error handling
│       ├── auth.py             # Login, Register, Logout
│       ├── device.py           # Device operations
│       └── diagnostics.py      # Diagnostics operations
├── logs/
│   └── app.log
├── config.py
├── run.py
├── requirements.txt
└── README.md

````

---

## 🔐 Authentication Features

- Secure login/register using **JWT** stored in cookies  
- Username validation: 3–20 characters (letters, numbers, underscores)  
- Password validation: Min 8 characters, includes uppercase, number, symbol  
- Tracks sessions via `session['username']`  
- Unauthorized access shows a flash message and logs the event  

---

## 🛠️ Device Management

- Fields: `name`, `device_type`, `status`, `location`  
- Create, Read, Update, Delete (CRUD) support  
- Search/filter by ID, location, status  
- Pagination support (5 devices per page)  

---

## 📊 Diagnostics Logging

- Fields: `device_id`, `cpu_usage`, `memory_usage`, `timestamp`  
- Filter diagnostics by device ID  
- Sort diagnostics by `timestamp`, `CPU usage`, or `memory usage`  
- Pagination support  

---

## 🧩 UI Pages (Templates)

| Page                     | Purpose                                |
|--------------------------|----------------------------------------|
| `base.html`              | Master layout + nav + flash            |
| `home.html`              | Dashboard landing                      |
| `login.html`             | Login form                             |
| `register.html`          | Registration form                      |
| `devices.html`           | Device list + filters                  |
| `add_device.html`        | Add device form                        |
| `update_device.html`     | Edit device form                       |
| `diagnostics.html`       | Diagnostics table + sorting/filtering  |
| `add_diagnostics.html`   | Add diagnostics entry                  |
| `update_diagnostics.html`| Update diagnostics entry               |

---

##   Getting Started

### 1. Clone This Repo
```bash
git clone https://github.com/bari8333/FLASK-PROJECT.git
cd FLASK_PROJECT
````

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate  # On Linux/macOS
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
flask run
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

##   API Endpoints

> ⚠️ All routes (except auth) require JWT authentication via cookies.

### 🔐 Auth

| Method | Endpoint    | Description   |
| ------ | ----------- | ------------- |
| POST   | `/register` | Register user |
| POST   | `/login`    | Login user    |
| GET    | `/logout`   | Logout user   |

### 🛠️ Devices

| Method | Endpoint              | Description      |
| ------ | --------------------- | ---------------- |
| GET    | `/device/home`        | List devices     |
| GET    | `/device/add`         | Show add form    |
| POST   | `/device/add`         | Add new device   |
| GET    | `/device/update/<id>` | Show update form |
| POST   | `/device/update/<id>` | Update device    |
| GET    | `/device/delete/<id>` | Delete device    |

### 📊 Diagnostics

| Method | Endpoint                   | Description           |
| ------ | -------------------------- | --------------------- |
| GET    | `/diagnostics/home`        | List diagnostics      |
| GET    | `/diagnostics/add`         | Show add form         |
| POST   | `/diagnostics/add`         | Add diagnostic record |
| GET    | `/diagnostics/update/<id>` | Show update form      |
| POST   | `/diagnostics/update/<id>` | Update diagnostics    |
| GET    | `/diagnostics/delete/<id>` | Delete diagnostics    |

---

##   Database Models

### `User`

* `id`: Primary key
* `username`: Unique
* `password`: Hashed

### `Device`

* `id`, `name`, `device_type`, `status`, `location`
* `user_id`: FK to User

### `DeviceDiagnostics`

* `id`, `device_id`, `cpu_usage`, `memory_usage`, `timestamp`

---

## 🛠 Dev Notes

* Logs stored in `logs/app.log`
* Frontend powered by Bootstrap 5
* JWT handled via `flask_jwt_extended`
* Optional: Use Flask-Migrate

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

##   Screenshots

![Home page](<Screenshot 2025-06-27 212241.png>)![Login Page](<Screenshot 2025-06-27 212626.png>)![Register Page](<Screenshot 2025-06-27 215242.png>)  ![Device home page ](<Screenshot 2025-06-27 212334.png>)  ![Diagnostics home page](<Screenshot 2025-06-27 212542.png>) ![Upadate Device](<Screenshot 2025-06-27 212657.png>)  ![Add Device](<Screenshot 2025-06-27 212452.png>)

---

##  Built With

* Flask
* Bootstrap 5
* Flask-JWT-Extended
* Flask-SQLAlchemy
* Flask-Migrate
* Marshmallow

---

## 👨‍💻 Author

**Abdul Bari M**
GitHub: [bari8333](https://github.com/bari8333)

---
