
# Flask User Management System

This project is a Flask-based user management system that includes functionalities for user registration, login, password reset, and OTP verification. The application uses Amazon SES for sending emails and SQLite for the database.

## Features

- User Registration
- User Login
- Forgot Password with OTP Verification
- Password Reset
- User Account Management
- Custom Error Pages for 400, 404, and 500 status codes

## Project Structure

```
your_project/
├── .env
├── .sample.env
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── forms.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── account.html
│   │   ├── forgot_password.html
│   │   ├── verify_otp.html
│   │   ├── reset_password.html
│   │   ├── welcome_email.html
│   │   ├── welcome_email.txt
│   │   ├── 400.html
│   │   ├── 404.html
│   │   ├── 500.html
│   ├── static/
│       ├── css/
│           ├── custom.css
│   ├── error_handlers.py
├── config.py
├── requirements.txt
├── application.py
├── utils.py
```

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Virtualenv

### Installation

1. Clone the repository:

```sh
git clone https://github.com/marketcalls/flask-user-management.git
cd flask-user-management
```

2. Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

4. Create a `.env` file in the project root directory and add the following environment variables:

```env
SECRET_KEY=your_secret_key_here
SQLALCHEMY_DATABASE_URI=sqlite:///site.db
MAIL_SERVER=email-smtp.ap-south-1.amazonaws.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_ses_smtp_username_here
MAIL_PASSWORD=your_ses_smtp_password_here
MAIL_DEFAULT_SENDER=your_default_sender_email_here
```

### Running the Application

1. Run the Flask application:

```sh
flask run
```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

- Register a new user account.
- Log in with the registered account.
- Use the "Forgot Password" feature to reset the password via OTP verification.
- Access and manage user account details.

## License

This project is licensed under the MIT License. 
