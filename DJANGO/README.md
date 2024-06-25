# Car-Park

In this project, you will be able to see the parking lots and occupancy rates near your location on our website.There are also features such as registration, login, login with google, password reset, profile editing in our project.When you register on our site, if you are going to log in to the site for the first time, you must first verify your account with the link that comes to your mail. Otherwise you will not be able to log in to the site. And if you forget your password, you can reset your password with the link to your mail. Our project is still under development. We will add new features.

In this project, we used google firebase authentication for authentication. We created a google account for Carpark. To use this project, you must first create google firebase and update the password and mail parts from settings.py.

## Installation And Requirements

Operating System: Windows-based systems.
RAM: At least 4GB (8GB recommended).
Required Tools: Android Studio, Java Development Kit (JDK).
Database we use: Firebase
Firebase Account: For integration with Firebase, a Firebase account must be created.
There is a firebase account and application id that we have already used for the first versions of the application. The necessary information about the database accounts of the project will be transferred with the application codes after the purchase.

- Python 3.x
- Django

### Steps

1. Navigate to the Project Directory
    Change your current directory to the project's directory:

    cd /path/to/your/project

2. Create and activate a virtual environment:

    python -m venv myvenv

    myvenv\Scripts\activate
        
3. Create the database:
    python manage.py makemigrations

    python manage.py migrate
    
4. Start the development server:

    python manage.py runserver
    
5. Create Admin Profile

    To create a superuser for the admin panel, run:

    python manage.py createsuperuser


### Login

Login page for both librarians and users:
http://127.0.0.1:8000
