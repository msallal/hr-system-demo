This is project a basic HR system built based on specific requirements, using Python [Django 5.2](https://www.djangoproject.com/), [Django-REST](https://www.django-rest-framework.org/) and a basic UI built with [Next.js](https://nextjs.org).

## Overview
This is a basic implementation for HR System, that's built with Python/Django/DjangoREST framework.
The project is built with Tests (unit testes & Integration tests)
Also, it has a basic UI implemented using React/NextJS & TailwindCSS
The project also contains a ready for development Dockerfile & docker-compose.yml.
The system support to host static files and resume files on AWS S3 storage (check `.env` file on how to enable it)
Below, you will find the details of the project API endpoints and how to use them.


# Installation
- Install on local machine:
  - requirements
    - Python 3.11 or above
    - pip
    - PostgreSQL 15 or above
  - Project setup:
    - run `pip install -r requirements`
    - setup the project environment variables in the project root file `.env`
    - run `python manage.py migrate`
  - Run the frontend UI:
    - go to the frontend dir: `cd frontend` 
    - run the development server, using one of the following commands:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```
Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Run Tests
### Running tests:
This project has covered a lot of unit tests and integrations tests (API)
- in the project root directory, run: `pytest` or `pytest -v`
You should see the green result of all tests passing

## Installation using docker
- make sure you have docker & docker-compose are installed on your host.
- run the project through docker-compose `docker-compose up --build -d` to run in background
  - Open [http://0.0.0.0:8000/](http://0.0.0.0:8000/) with your browser to see the result.
  - you can browse the API endpoints available there.
  - to stop the server, run: `docker-compose down`

# API Endpoints
There are mainly 5 endpoints as the following:
1. Candidate Registration Endpoint:
   - HTTP [POST] /candidates/, with `Content-Type` `multipart/form-data;` as this curl example:
```curl
curl --location 'http://127.0.0.1:8000/candidates/' \
--form 'full_name="Mohammad Alsallal"' \
--form 'email="mohammad@example.com"' \
--form 'phone_number="0799999999"' \
--form 'date_of_birth="1990-07-18"' \
--form 'department_id="IT"' \
--form 'years_of_experience="12"' \
--form 'resume_file=@"/Users/user1/Downloads/resume_file.pdf"' \
--form 'password="test1234"
```
All fields above are required for successful registration (no verification required).
`Department_id` can have one of the following values: `IT`, `HR`, or `FIN` for Finance.
In case of successful registration, the response looks like:
```json
{
    "success": "Your application has been submitted successfully!"
}
```
Which means the application is received and initiated with stats "Submitted".
2. Candidate Status Check Endpoint:
 - HTTP [POST] /candidate/check
```curl
curl --location 'http://127.0.0.1:8000/candidate/check' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email" : "mohammad@example.com",
    "password" : "test1234"
}'
```
and a successful response looks like, `HTTP 200`:
```json
{
    "name": "Mohammad Alsallal",
    "application_status": "INTERVIEW_SCHEDULED",
    "feedback": "Your application has been submitted successfully!",
    "history": [
        {
            "updated_at": "2025-07-08T20:15:20.148709Z",
            "status": "INTERVIEW_SCHEDULED",
            "feedback": "You're invited for a Scheduled interview, please check ur email for more details!",
            "updated by": "Ahmad"
        }
    ]
}
```

3. `Admin` List Candidates Endpoint with (pagination & filters):
- HTTP [GET] /admin/candidates/
```curl
curl --location 'http://127.0.0.1:8000/admin/candidates/' \
--header 'X-Admin: 1'
```
and a successful response looks like, `HTTP 200`:
```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 4,
            "full_name": "last user",
            "email": "demo4@test.com",
            "phone_number": "07955522239",
            "date_of_birth": "1990-01-17",
            "department_id": "IT",
            "years_of_experience": 5
        },
        {
            "id": 3,
            "full_name": "thrid user",
            "email": "demo3@test.com",
            "phone_number": "07955522238",
            "date_of_birth": "1990-01-17",
            "department_id": "FIN",
            "years_of_experience": 5
        },
        {
            "id": 2,
            "full_name": "second user",
            "email": "demo2@test.com",
            "phone_number": "07955522229",
            "date_of_birth": "1990-01-17",
            "department_id": "HR",
            "years_of_experience": 6
        },
        {
            "id": 1,
            "full_name": "demo user",
            "email": "demo1@test.com",
            "phone_number": "07955522228",
            "date_of_birth": "1990-01-17",
            "department_id": "FIN",
            "years_of_experience": 5
        }
    ]
}
```
- Another request with `department` filter and pagination(limit/offset):
```curl
curl --location 'http://127.0.0.1:8000/admin/candidates/?department=IT&offset=10&liimit=5' \
--header 'X-Admin: 1'
```

4. `Admin` - Update Application Status Endpoint:
Through this endpoint, the HR system admin can update an application statusm with new status from the available status: (`SUBMITTED`, `UNDER_REVIEW`, `INTERVIEW_SCHEDULED`, `REJECTED`, `ACCEPTED`).
Also, the 'admin_name' must be provided.
- HTTP [PUT] /admin/candidates/`{candidateID}`/
- Example
```curl
curl --location --request PUT 'http://127.0.0.1:8000/admin/candidates/4/' \
--header 'X-ADMIN: 1' \
--header 'Content-Type: application/json' \
--data '{
    "status" : "INTERVIEW_SCHEDULED",
    "feedback" : "You'\''re invited for a Scheduled interview, please check ur email for more details!",
    
    "admin_name" : "Ahmad"
}'
```
and a successful response looks like, HTTP`204 No Content`.

5. `Admin` Download Resume Endpoint:
The Admins can download candidates resume files, using the candidate ID, which is provided in the admin - list candidates endpoint above.
- HTTP [GET] /admin/candidates/`{candidateID}`/resume-download/
```curl
curl --location 'http://127.0.0.1:8000/admin/candidates/4/resume-download/' \
--header 'X-admin: 1'
```