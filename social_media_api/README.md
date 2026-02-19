# Social Media API 🚀

A robust Social Media API built with **Django** and **Django REST Framework (DRF)**. This project features a custom user model with follower/following capabilities, a dynamic content feed, and secure Token-based authentication.

---

## 🛠️ Setup Instructions

### 1. Environment Configuration
Ensure you have Python installed, then run the following to set up your environment:

# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Install required dependencies
pip install django djangorestframework

### 2. Database Initialization
Because this project uses a Custom User Model and new Post/Comment features, you must initialize the database schema:

# Create migrations for the apps
python manage.py makemigrations accounts
python manage.py makemigrations posts

# Apply all migrations to the database
python manage.py migrate

### 3. Launching the API
Start the Django development server:
python manage.py runserver

The API will be accessible at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔐 Authentication & User Management

This API uses **Token-based Authentication**.

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| /api/accounts/register/ | POST | Register a new user and receive an Auth Token. |
| /api/accounts/login/ | POST | Login with username/password to retrieve your Token. |
| /api/accounts/follow/<int:user_id>/ | POST | Follow a specific user by their ID. |
| /api/accounts/unfollow/<int:user_id>/ | POST | Unfollow a specific user by their ID. |

**Header Format for Protected Routes:**
Authorization: Token <your_generated_token>

---

## 📝 Social Features (Posts, Comments & Feed)

Manage content and engage with other users through the following endpoints:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| /api/posts/ | GET | List all posts (supports ?search=term). |
| /api/posts/ | POST | Create a new post (Auth required). |
| /api/posts/<id>/ | PUT/DELETE | Update or Delete a post (Author only). |
| /api/posts/feed/ | GET | View posts from users you follow, newest first. |
| /api/comments/ | POST | Add a comment to a specific post. |
| /api/posts/<int:pk>/like/ | POST | Like a post and notify the author. |
| /api/posts/<int:pk>/unlike/ | POST | Remove a like from a post. |
| /api/notifications/ | GET | List all notifications for the current user. |

### 🔍 Filtering & Search
To search for posts by title or content:
GET /api/posts/?search=django

---

## 👤 User Model Overview

The system uses a **Custom User Model** (accounts.User) extending Django's AbstractUser:

* bio: A text field for user profile descriptions.
* profile_picture: Supports image uploads (stored in profile_pics/).
* following: A Many-to-Many relationship (non-symmetrical) allowing users to follow others.

---

## 🧪 Testing with Postman/cURL

To test the registration, send a POST request to [http://127.0.0.1:8000/api/accounts/register/](http://127.0.0.1:8000/api/accounts/register/) with the following JSON body:

{
    "username": "new_user",
    "password": "secure_password_123",
    "email": "user@example.com",
    "bio": "Developing a cool social media API!"
}

The response will contain your token. Use this token in the Headers for all other requests.

---

## 📂 Project Structure
* accounts/: Handles user logic, authentication, and follow relationships.
* posts/: Manages posts, comments, and the aggregated feed logic.
* social_media_api/: Project configuration and main routing.
* manage.py: Django's command-line utility.