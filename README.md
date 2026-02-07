# Rumor Tracking System

ระบบติดตามข่าวลือบนสื่อสังคมออนไลน์ พัฒนาด้วย Django + MySQL

## Requirements

- Python 3.10+
- Docker Desktop
- pip

## Setup

### 1. สร้าง Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start MySQL (Docker)

```bash
docker-compose up -d
```

### 5. สร้าง Database Tables

```bash
python manage.py makemigrations rumors
python manage.py migrate
```

### 6. โหลดข้อมูลตัวอย่าง

```bash
python manage.py load_sample_data
```

### 7. รันเซิร์ฟเวอร์

```bash
python manage.py runserver
```

## การใช้งาน

- หน้าหลัก: http://localhost:8000/
- หน้าสรุปผล: http://localhost:8000/summary/

## โครงสร้างโปรเจกต์

```
mvc_2_68_66050067/
├── rumor_tracking/     # Project settings
├── rumors/             # Main app
│   ├── models.py       # User, Rumour, Report
│   ├── views.py        # Controller
│   └── templates/      # Views (HTML)
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

## MVC Pattern

| Component  | Django   | ไฟล์              |
| ---------- | -------- | ----------------- |
| Model      | Model    | rumors/models.py  |
| View       | Template | rumors/templates/ |
| Controller | View     | rumors/views.py   |
