Django Blog Project Documentation
1. Authentication System
This project uses a custom authentication system built on Django’s built-in auth framework, extended with User Profiles.

Components
Registration: Users create an account via a CustomUserCreationForm which includes an email field.

Login/Logout: Handled by Django’s LoginView and LogoutView.

Profiles: Each user has a Profile model (created automatically via Django Signals) that stores a bio and profile picture.

Permissions: Access to creating, editing, and deleting content is restricted to authenticated authors.

How to Test
Registration: Navigate to /register/, fill the form, and submit. Verify you are redirected to the login page.

Login: Use your new credentials at /login/.

Profile Update: Once logged in, visit /profile/ to update your bio or image. Verify changes persist.

2. Blog Post Features (CRUD)
The blog allows for dynamic content management using Class-Based Views (CBVs).

Features
Create: Authenticated users can write new posts.

Read: The home page lists all posts (ListView), and clicking a title shows the full content (DetailView).

Update/Delete: Only the original author can modify or remove their posts.

Permissions & Data Handling
LoginRequiredMixin: Used to block anonymous users from the "New Post" page.

UserPassesTestMixin: Ensures that if a user tries to edit a post they didn't write, they receive a 403 Forbidden error.

3. Comment System
The comment system fosters community engagement on every blog post.

How to Use
Adding: Logged-in users will see a comment form at the bottom of every Post Detail page.

Editing/Deleting: Authors of a comment will see "Edit" and "Delete" links next to their specific comment.

Visibility: Anyone (including guests) can read comments, but only authenticated users can participate.

Rules
Comments are deleted automatically if the parent Blog Post is deleted (Cascade Delete).

Permissions are strictly enforced: you cannot edit another user's comment.

4. Tagging and Search
These features improve navigability and content discovery.

Tagging System
Adding Tags: When creating or editing a post, use the tags field. Enter keywords separated by commas (e.g., django, tutorial, python).

Functionality: We use django-taggit with a TagWidget for clean input.

Filtering: Clicking any tag (e.g., #web) redirects you to a filtered list view (/tags/<tag_slug>/) showing all posts with that tag.

Search Functionality
How to Search: Use the search bar in the navigation menu.

Logic: The system uses Django Q objects to perform a case-insensitive search across:

Post Titles

Post Content

Tag Names

5. Technical Requirements
Environment: Python 3.x, Django 4.x/5.x

Dependencies: django-taggit, Pillow (for images)

Database: SQLite (default)