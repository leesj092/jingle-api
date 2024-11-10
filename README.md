# Jingle-API

This project implements a backend API for a 1:1 tutoring service where students can enroll in classes with tutors.
The API is built using Django and Django REST Framework and supports features for both tutors and students.

## Features
### Tutor
- Create Availability: Tutors can specify time slots during which they are available.
- Delete Availability: Tutors can delete their previously created availability.
- List Availability: Tutors can view all available time slots.

### Student
- Query Available Time Slots: Students can query available time slots within a specified time range and duration.
- Query Available Tutors: Students can find tutors available for a specific time and duration.
- Create Enrollment: Students can book a tutor's available time slot.
- View Enrollments: Students can view their own enrollments.
- Delete Enrollment: Students can cancel their enrollments.

## Technical Details
### Tech Stack
- Framework: Django REST Framework
- Database: SQLite (can be swapped for PostgreSQL or MySQL)
- Authentication: JWT (via SimpleJWT)

### Validation Logic
- Students can only query time slots that start on the hour or half-hour (e.g., 10:00, 10:30).
- Tutors cannot create overlapping availability slots.
- Students cannot enroll in overlapping time slots.
- Students can only view or manage their own enrollments.

## Installation
### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)
- pip for dependency management

1. Clone the repository:
```
git clone https://github.com/leesj092/jingle-api.git
cd jingle-api
```

2. Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Apply migrations to set up the database:
```
python manage.py migrate
```

5. Create a superuser for accessing the admin panel (optional):
```
python manage.py createsuperuser
```

6. Start the development server:
```
python manage.py runserver
```

## API Endpoints
### Tutor
#### Create Availability:
`POST /api/tutors/availability/`

#### Request Body:
```
{
    "tutor": 1,
    "start_time": "2023-11-05T10:00:00Z",
    "duration": 60
}
```

#### Delete Availability:
`DELETE /api/tutors/availability/<id>/`

#### List Availability:
`GET /api/tutors/availability/`

### Student
#### Query Available Time Slots:
`GET /api/tutors/availability/?start_time=<start_time>&duration=<duration>`
#### Example:
```
curl -X GET "http://127.0.0.1:8000/api/tutors/availability/?start_time=2023-11-05T10:30:00Z&duration=30"
```

#### Query Available Tutors:
`GET /api/tutors/available-tutors/?start_time=<start_time>&duration=<duration>`
#### Example:
```
curl -X GET "http://127.0.0.1:8000/api/tutors/available-tutors/?start_time=2023-11-05T10:30:00Z&duration=30"
```

#### Create Enrollment:
`POST /api/students/enrollments/`
#### Request Body:
```
{
    "tutor": 1,
    "start_time": "2023-11-05T10:30:00Z",
    "duration": 30
}
```

#### View Enrollments:
`GET /api/students/enrollments/`
#### Example:
```
curl -X GET "http://127.0.0.1:8000/api/students/enrollments/" \
-H "Authorization: Bearer <access_token>"
```

#### Delete Enrollment:
`DELETE /api/students/enrollments/<id>/`

## Authentication
This API uses JWT for authentication.

1. Obtain Token:
```
curl -X POST "http://127.0.0.1:8000/api/token/" \
-H "Content-Type: application/json" \
-d '{
    "username": "your_username",
    "password": "your_password"
}'
```
2. Use Access Token:
Include the Authorization: Bearer <access_token> header in your API requests.

## Validation Rules
### Students:
- Can only view and manage their own enrollments.
- Cannot enroll in overlapping time slots.
- Can only query for classes starting on the hour or half-hour.
### Tutors:
- Cannot create overlapping availability slots.

