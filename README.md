# Human Resource Management System

This is a Human Resource Management System built with Django, which includes both a web application and API. The system is designed to help organizations manage their hiring processes by allowing students to register and submit their resumes through a user-friendly form.

## Features
- User-friendly registration form for students to submit their details and resumes
- Separate login panels for admin and staff
- Admin panel for managing and approving candidate resumes
- Staff members can only access approved resumes and can send emails to selected candidates
- API endpoints for retrieving candidate information and managing the hiring process
- Generates a PDF version of the candidate's resume for easy printing and sharing


## Installation
To install the project, follow these steps:

1. Clone the repository
2. Install the dependencies by running pip install -r requirements.txt
3. Create a .env file and add your environment variables
4. Run migrations with python manage.py migrate
5. Start the server with python manage.py runserver


## Usage
Once the server is running, you can access the web application at http://http://127.0.0.1 and the API at http://http://127.0.0.1/api/.

Use the registration form to submit resumes as a student, and login as an admin or staff member to access the relevant panels. Staff members can only access approved resumes and can send emails to selected candidates.


### To use app

```sh
docker-compose -f docker-compose-deploy.yml build
```

### To start app

```sh
docker-compose -f docker-compose-deploy.yml up
```