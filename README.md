# Notes App

A simple full-stack Notes Application built with **Django**. Users can create, view, update, and delete their notes, with authentication and image upload functionality.

## Features

* User registration and login
* User logout
* Authentication-protected pages
* Create notes
* View notes
* Update notes
* Delete notes
* Upload images with notes
* Preview images before uploading
* Delete uploaded images
* Regex-based username and password validation
* Django Admin Panel
* AWS S3 storage for uploaded images
* REST API for notes
* Responsive and simple user interface

## Tech Stack

### Backend

* Python
* Django
* Django REST Framework
* SQLite for local development
* AWS S3 for image storage

### Frontend

* HTML
* CSS
* Django Templates
* JavaScript

### Authentication

* Django's built-in User model
* Session-based authentication
* CSRF protection

## Project Structure

```text
notes-app/
│
├── notes/
│   ├── migrations/
│   ├── templates/
│   │   └── notes/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ShabdRastogi/notes-app.git
cd notes-app
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory.

Use `.env.example` as a reference:

```bash
copy .env.example .env
```

Then add your own values.

Example:

```env
SECRET_KEY=

DEBUG=False

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
DATABASE_URL=
```

**Do not commit your `.env` file or any secret credentials to GitHub.**

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 7. Run the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

The Django Admin Panel is available at:

```text
http://127.0.0.1:8000/admin/
```

## API Endpoints

The application also provides REST APIs for managing notes using **Django REST Framework**.

### Get All Notes

**GET**

```text
/api/notes/
```

Returns all notes from the database.

**Success Response:**

```text
200 OK
```

Example response:

```json
[
    {
        "id": 1,
        "title": "Learning DRF",
        "description": "Understanding REST APIs"
    },
    {
        "id": 2,
        "title": "Django",
        "description": "Learning Django REST Framework"
    }
]
```

### Create a Note

**POST**

```text
/api/notes/
```

Creates a new note using the data provided by the client.

**Request Body:**

```json
{
    "title": "Learning DRF",
    "description": "Understanding REST APIs"
}
```

**Success Response:**

```text
201 Created
```

Example response:

```json
{
    "id": 1,
    "title": "Learning DRF",
    "description": "Understanding REST APIs"
}
```

**Invalid Request:**

```text
400 Bad Request
```

The response contains the serializer validation errors.

Example:

```json
{
    "title": [
        "This field may not be blank."
    ]
}
```

### Get a Single Note

**GET**

```text
/api/notes/<id>/
```

Returns the details of a specific note using its ID.

**Example:**

```text
/api/notes/1/
```

**Success Response:**

```text
200 OK
```

Example response:

```json
{
    "id": 1,
    "title": "Learning DRF",
    "description": "Understanding REST APIs"
}
```

**If the note does not exist:**

```text
404 Not Found
```

Example response:

```json
{
    "detail": "Not found."
}
```

### Update a Note

**PUT**

```text
/api/notes/<id>/
```

Updates an existing note using its ID.

**Example:**

```text
/api/notes/1/
```

**Request Body:**

```json
{
    "title": "Learning Django REST Framework",
    "description": "Learning how to create and update notes using DRF."
}
```

**Success Response:**

```text
200 OK
```

Example response:

```json
{
    "id": 1,
    "title": "Learning Django REST Framework",
    "description": "Learning how to create and update notes using DRF."
}
```

**Invalid Request:**

```text
400 Bad Request
```

The response contains the serializer validation errors.

**If the note does not exist:**

```text
404 Not Found
```

Example response:

```json
{
    "detail": "Not found."
}
```

### Delete a Note

**DELETE**

```text
/api/notes/<id>/
```

Deletes an existing note using its ID.

**Example:**

```text
/api/notes/1/
```

**Success Response:**

```text
204 No Content
```

## API Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notes/` | Get all notes |
| POST | `/api/notes/` | Create a new note |
| GET | `/api/notes/<id>/` | Get a single note |
| PUT | `/api/notes/<id>/` | Update a note |
| DELETE | `/api/notes/<id>/` | Delete a note |

> More API endpoints may be added as the REST API is developed.

## Notes Functionality

Each authenticated user can manage their own notes.

A note contains information such as:

* Title
* Description
* Image
* Created date
* Updated date
* Associated user

Images uploaded through the application are stored using **Amazon S3** rather than being stored directly on the application server.

## Authentication

The application uses Django's authentication system for:

* User registration
* Login
* Logout
* Password hashing
* Session management
* Login-protected views

CSRF tokens are also used for POST forms to protect against Cross-Site Request Forgery attacks.

## Image Upload

Users can upload an image while creating or editing a note.

The application uses:

```html
<input type="file" accept="image/*">
```

Images are uploaded through `multipart/form-data` and stored using AWS S3.

Users can also preview an image before submitting the form and delete an existing image.

## Validation

The application includes regular-expression-based validation for username and password fields.

Additional validation is performed through Django's authentication and model systems.

## Environment Variables

The following environment variables are used by the project:

| Variable | Purpose |
| -------------------------- | --------------------------------------- |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Django debug mode |
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket name |
| `AWS_S3_REGION_NAME` | AWS S3 region |
| `AWS_S3_SIGNATURE_VERSION` | S3 signature version |
| `AWS_QUERYSTRING_AUTH` | Controls S3 query-string authentication |
| `DATABASE_URL` | Database connection URL |

Keep sensitive values private and never commit them to the repository.

## Deployment

The application can be deployed to platforms such as **Render**.

For production deployment, configure the required environment variables in the hosting platform instead of committing secrets to the repository.

Before deployment, make sure to:

1. Configure production environment variables.
2. Configure `ALLOWED_HOSTS`.
3. Run database migrations.
4. Collect static files.
5. Configure AWS S3 for media storage.
6. Use a production WSGI server.

## Future Improvements

Some possible improvements for future versions:

* Password reset functionality
* Better form validation and error handling
* Search and filtering for notes
* Note categories/tags
* Pagination
* Rich text editing
* User profile management
* Improved UI/UX
* Automated tests

## License

This project is created for learning and educational purposes.

