# Event Ticketing System API

Flask REST API for managing tickets system using a MySQL database.

## Setup

1. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
```

4. **Initialize database**
```bash
mysql -u root -p < database.sql
```

5. **Run application**
```bash
python app.py
```

API available at: **http://localhost:5000**
