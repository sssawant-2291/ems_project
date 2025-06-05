# EMS Project

## Setup Instructions

1. Clone the repo:
    ```bash
    git clone https://github.com/sssawant-2291/ems_project.git
    cd ems_project
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:
    ```bash
    python manage.py migrate
    ```

5. Start the server:
    ```bash
    python manage.py runserver
    ```

---

## 📄 Assumptions

- All API endpoints are accessible via a base URL (configured as `{{URL}}` in Postman).
- The project uses Django with SQLite3.
- Basic CRUD operations are implemented for event and attendee management.
- No authentication or authorization is enforced for API access unless specified.
- All datetime fields and timestamps are stored and processed in **UTC timezone**.
- Still you may create event with local timezone as follows rest will be taken care of
    POST {{URL}}/events/
    Body -
    ```
    {
        "name": "Daily scrum",
        "location": "Banglore Office",
        "start_time": "2025-06-10T10:00:00+05:30",
        "end_time": "2025-06-10T10:15:00+05:30",
        "max_capacity": 10
    }
    ```

---

## 🛠 Database Schema

The full database schema is available in [`schema.sql`](./schema.sql).

To set up the database manually (if not using Django migrations), run:

```bash
sqlite3 db.sqlite3 < schema.sql



## 📬 Postman Collection

You can test all available EMS API endpoints using the Postman collection.

▶️ [Download EMS Postman Collection](./postman/ems_project_collection.json)

### 🚀 How to use:

1. Open [Postman](https://www.postman.com/downloads/)
2. Click **Import**
3. Choose the file: `ems_project_collection.json`
4. Set `{{URL}}` variable in **Environment** to your local or deployed API URL  
   e.g., `http://127.0.0.1:8000/api`
5. Send requests!

### ✅ Sample Endpoints Covered:
- `POST /events/` – Create event
- `GET /events/` – List upcoming events
- `POST /events/{event_id}/register/` – Register attendee
- `GET /events/{event_id}/attendees/` – Get attendees (without pagination)
- `GET /events/{event_id}/attendees/?page=1&page_size=5` – Get attendees (with pagination)

## API Documentation
- http://127.0.0.1:8000/swagger/