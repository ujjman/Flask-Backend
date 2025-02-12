# Task Management System API 🚀

Welcome to the **Task Management System API**! This project is a simple REST API built with Python Flask that allows you to create, update, delete, and list tasks. It uses an in-memory SQLite database, JWT authentication, pagination, and an event log to track task-related events.

---

## Features ✨

- **Task CRUD Operations:** Create, update, delete, and list tasks.
- **JWT Authentication:** Secure your endpoints via token-based authentication.
- **Pagination:** Easily paginate through tasks with query parameters.
- **Event Log:** Automatically log events like "Task Created", "Task Updated", and "Task Deleted".

---

## Tech Stack 🛠

- **Language:** Python 3.x
- **Framework:** Flask
- **Database:** SQLite (in-memory)
- **ORM:** Flask-SQLAlchemy
- **Authentication:** Flask-JWT-Extended
- **Testing:** Python's built-in `unittest` module

---

## Getting Started 🚀

### Prerequisites

- Python 3 installed on your machine.

### Installation Steps

1. **Clone the Repository** 📂

   ```bash
   git clone https://github.com/ujjman/Task-Management-API
   cd "Task-Management-API"
   ```

2. **Create a Virtual Environment** (Optional but recommended) 🌱

   ```bash
   python3 -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies** 📦

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application** 🏃‍♂️

   ```bash
   python app.py
   ```

   The API will be available at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## API Endpoints 🌐

### 1. Login (JWT Authentication)

- **Endpoint:** `POST /login`
- **Request Body:**
  ```json
  {
    "username": "ujjwal",
    "password": "mishra"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "<JWT_TOKEN>"
  }
  ```
- **Usage:** Include the JWT token in the `Authorization` header as follows:
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```

---

### 2. Create a Task

- **Endpoint:** `POST /tasks`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "title": "Complete Internship Assignment",
    "description": "Solve the given problem and submit the code",
    "status": "PENDING"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "title": "Complete Internship Assignment",
    "description": "Solve the given problem and submit the code",
    "status": "PENDING",
    "createdAt": "2025-02-01T12:00:00Z"
  }
  ```

---

### 3. Get All Tasks (with Pagination)

- **Endpoint:** `GET /tasks`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Query Parameters:**
  - `page` (default: 1)
  - `per_page` (default: 10)
- **Response:** Returns an array of task objects.
- **For example:** http://127.0.0.1:5000/tasks?page=3&per_page=15

---

### 4. Update a Task

- **Endpoint:** `PUT /tasks/{id}`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:** (Example to update the task status)
  ```json
  {
    "status": "COMPLETED"
  }
  ```
- **Response:** Returns the updated task object.

---

### 5. Delete a Task

- **Endpoint:** `DELETE /tasks/{id}`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:** `204 No Content`

---

### 6. Get Event Logs

- **Endpoint:** `GET /events`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:** Returns an array of event log objects.

---

## Testing 🧪

### Manual Pagination Testing

1. **Create Multiple Tasks:**

   - Use the `POST /tasks` endpoint to create at least 15 tasks.

2. **Retrieve Tasks Using Pagination:**

   - **Page 1 (10 tasks):**
     ```bash
     curl -X GET "http://127.0.0.1:5000/tasks?page=1&per_page=10" \
       -H "Authorization: Bearer <JWT_TOKEN>"
     ```
   - **Page 2 (Remaining tasks):**
     ```bash
     curl -X GET "http://127.0.0.1:5000/tasks?page=2&per_page=10" \
       -H "Authorization: Bearer <JWT_TOKEN>"
     ```

### Running Unit Tests

The project includes unit tests for both the repository and service layers.

#### Run All Tests

```bash
python -m unittest discover tests
```

#### Run Tests File by File

- **Repository Tests:**
  ```bash
  python -m unittest tests.test_repository
  ```
- **Service Tests:**
  ```bash
  python -m unittest tests.test_service
  ```

---
