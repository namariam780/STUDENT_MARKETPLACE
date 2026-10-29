# Student Marketplace Backend

## Project Description
The Student Marketplace is a REST API developed using Python, FastAPI, and MySQL. It allows students to manage product listings, categories, and orders. The API sends and receives data in JSON format over HTTP.

## Requirements
- Python installed
- MySQL Server installed and running
- Visual Studio Code or another code editor

## Installation Steps

### 1. Open the backend folder
Open the backend folder in Visual Studio Code.

### 2. Create a virtual environment
Run this command in the terminal:

```bash
python -m venv .venv
```

### 3. Activate the virtual environment
For Windows PowerShell, run:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install the required packages
Run:

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the database
Start MySQL and create the `student_marketplace` database and the required tables. Check `database.py` and configure the MySQL connection using your local database username and password.

Do not publish your real database password on GitHub.

### 6. Start the backend server
Run:

```bash
python -m uvicorn main:app --reload
```

### 7. Test the API
Open this address in your browser:

http://127.0.0.1:8000/docs

The Swagger page allows you to test the API endpoints.

## Stopping the Server
Press `Ctrl + C` in the terminal.

## Technologies Used
- Python
- FastAPI
- MySQL
- Uvicorn
- JSON over HTTP

