# Advanced API Project - Django REST Framework

This project demonstrates advanced API development with Django REST Framework, featuring custom serializers, generic views, and comprehensive CRUD operations.

## Project Overview

A RESTful API for managing books and authors with the following features:
- Complete CRUD operations for books
- Custom serializers with nested relationships
- Permission-based access control
- Data validation (e.g., publication year cannot be in the future)

## Project Structure

```
advanced-api-project/
├── manage.py
├── advanced_api_project/          # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── api/                           # API application
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py                  # Author and Book models
    ├── serializers.py             # Custom serializers
    ├── views.py                   # Generic API views
    ├── urls.py                    # URL routing
    ├── tests.py
    └── migrations/
```

## Models

### Author Model
- **Fields:**
  - `name` (CharField): Author's full name (max 100 characters)
- **Relationships:**
  - One-to-many with Book (one author can write multiple books)

### Book Model
- **Fields:**
  - `title` (CharField): Book title (max 200 characters)
  - `publication_year` (IntegerField): Year of publication
  - `author` (ForeignKey): Reference to Author model
- **Constraints:**
  - Unique combination of title, author, and publication_year
  - Cascading delete (if author is deleted, their books are deleted)

## API Endpoints

### Book Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| GET | `/api/books/` | List all books (with filtering, search, ordering) | No (read-only) |
| GET | `/api/books/<int:pk>/` | Retrieve a single book | No (read-only) |
| POST | `/api/books/create/` | Create a new book | Yes |
| PUT/PATCH | `/api/books/<int:pk>/update/` | Update a book | Yes |
| DELETE | `/api/books/<int:pk>/delete/` | Delete a book | Yes |

### Advanced Query Parameters

The Book List endpoint (`/api/books/`) supports advanced querying:

**Filtering:**
- `?publication_year=<year>` - Filter by exact year
- `?publication_year__gte=<year>` - Year >= value
- `?publication_year__lte=<year>` - Year <= value
- `?author=<id>` - Filter by author ID
- `?title=<exact_title>` - Filter by exact title

**Searching:**
- `?search=<term>` - Search in title and author name

**Ordering:**
- `?ordering=<field>` - Sort by field (ascending)
- `?ordering=-<field>` - Sort by field (descending)
- Available fields: `title`, `publication_year`, `author`

**Examples:**
```bash
# Books published after 2000
GET /api/books/?publication_year__gte=2000

# Search for "tolkien"
GET /api/books/?search=tolkien

# Order by title A-Z
GET /api/books/?ordering=title

# Combined: Search for "magic" in books after 2000, newest first
GET /api/books/?search=magic&publication_year__gte=2000&ordering=-publication_year
```

See [FILTERING_GUIDE.md](FILTERING_GUIDE.md) for complete documentation.

## Views Configuration

### 1. BookListView (ListView)
- **Type:** `generics.ListAPIView`
- **Purpose:** Retrieve all books
- **HTTP Method:** GET
- **URL:** `/api/books/`
- **Permission:** `IsAuthenticatedOrReadOnly` (read access for all, write requires authentication)
- **Returns:** List of all books in JSON format

### 2. BookDetailView (DetailView)
- **Type:** `generics.RetrieveAPIView`
- **Purpose:** Retrieve a single book by ID
- **HTTP Method:** GET
- **URL:** `/api/books/<int:pk>/`
- **Permission:** `IsAuthenticatedOrReadOnly`
- **Returns:** Single book object in JSON format

### 3. BookCreateView (CreateView)
- **Type:** `generics.CreateAPIView`
- **Purpose:** Create a new book
- **HTTP Method:** POST
- **URL:** `/api/books/create/`
- **Permission:** `IsAuthenticatedOrReadOnly` (requires authentication)
- **Custom Hooks:** `perform_create()` for additional logic before saving
- **Returns:** 201 Created with the new book data

### 4. BookUpdateView (UpdateView)
- **Type:** `generics.UpdateAPIView`
- **Purpose:** Update an existing book
- **HTTP Methods:** PUT (full update), PATCH (partial update)
- **URL:** `/api/books/<int:pk>/update/`
- **Permission:** `IsAuthenticatedOrReadOnly` (requires authentication)
- **Custom Hooks:** `perform_update()` for additional logic before saving
- **Returns:** 200 OK with updated book data

### 5. BookDeleteView (DeleteView)
- **Type:** `generics.DestroyAPIView`
- **Purpose:** Delete a book
- **HTTP Method:** DELETE
- **URL:** `/api/books/<int:pk>/delete/`
- **Permission:** `IsAuthenticatedOrReadOnly` (requires authentication)
- **Custom Hooks:** `perform_destroy()` for additional logic before deletion
- **Returns:** 204 No Content

## Serializers

### BookSerializer
- **Purpose:** Converts Book model instances to/from JSON
- **Fields:** id, title, publication_year, author
- **Custom Validation:**
  - `validate_publication_year()`: Ensures publication year is not in the future
  - Automatically validates all model constraints

### AuthorSerializer
- **Purpose:** Converts Author model instances to/from JSON with nested books
- **Fields:** id, name, books
- **Nested Relationships:**
  - `books`: Nested BookSerializer (many=True, read_only=True)
  - Displays all books by the author in a hierarchical structure

## Permissions

The API uses `IsAuthenticatedOrReadOnly` permission class:

- **Unauthenticated Users:**
  - ✅ Can view books (GET requests to list and detail views)
  - ❌ Cannot create, update, or delete books

- **Authenticated Users:**
  - ✅ Full CRUD access to all book endpoints
  - ✅ Can create, read, update, and delete books

## Setup Instructions

### 1. Install Dependencies
```bash
pip install django djangorestframework
```

### 2. Create Project and App
```bash
# Create project directory
mkdir advanced-api-project
cd advanced-api-project

# Create Django project (note the dot at the end)
django-admin startproject advanced_api_project .

# Create API app
python manage.py startapp api
```

### 3. Configure Settings
Add to `advanced_api_project/settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Add Django REST Framework
    'api',             # Add your API app
]
```

### 4. Configure Main URLs
Update `advanced_api_project/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include API URLs
]
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (for authentication)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## Testing the API

### Using curl

#### 1. List all books (No authentication required)
```bash
curl http://localhost:8000/api/books/
```

#### 2. Get a specific book (No authentication required)
```bash
curl http://localhost:8000/api/books/1/
```

#### 3. Create a new book (Authentication required)
```bash
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "title": "The Great Gatsby",
    "publication_year": 1925,
    "author": 1
  }'
```

#### 4. Update a book - Full update (Authentication required)
```bash
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "title": "The Great Gatsby - Revised",
    "publication_year": 1925,
    "author": 1
  }'
```

#### 5. Update a book - Partial update (Authentication required)
```bash
curl -X PATCH http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "title": "The Great Gatsby - Final Edition"
  }'
```

#### 6. Delete a book (Authentication required)
```bash
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -u username:password
```

### Using Postman

1. **Set up authentication:**
   - Type: Basic Auth
   - Username: your_superuser_username
   - Password: your_superuser_password

2. **Test GET requests** (no auth needed):
   - GET `http://localhost:8000/api/books/`
   - GET `http://localhost:8000/api/books/1/`

3. **Test POST request** (auth required):
   - Method: POST
   - URL: `http://localhost:8000/api/books/create/`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
     ```json
     {
       "title": "1984",
       "publication_year": 1949,
       "author": 1
     }
     ```

4. **Test PUT/PATCH requests** (auth required):
   - Method: PUT or PATCH
   - URL: `http://localhost:8000/api/books/1/update/`
   - Body: Book data (all fields for PUT, partial for PATCH)

5. **Test DELETE request** (auth required):
   - Method: DELETE
   - URL: `http://localhost:8000/api/books/1/delete/`

### Using Django Shell

```bash
python manage.py shell
```

```python
from api.models import Author, Book
from api.serializers import BookSerializer, AuthorSerializer

# Create an author
author = Author.objects.create(name="F. Scott Fitzgerald")

# Create a book
book = Book.objects.create(
    title="The Great Gatsby",
    publication_year=1925,
    author=author
)

# Test serialization
book_serializer = BookSerializer(book)
print(book_serializer.data)

# Test author with nested books
author_serializer = AuthorSerializer(author)
print(author_serializer.data)
```

## Custom Features & Hooks

### View Customization Hooks

Each view includes custom hooks for extending functionality:

1. **`perform_create(self, serializer)`** in CreateView
   - Called after validation but before saving
   - Use for: Setting user, timestamps, triggering notifications

2. **`perform_update(self, serializer)`** in UpdateView
   - Called after validation but before updating
   - Use for: Logging changes, updating timestamps

3. **`perform_destroy(self, instance)`** in DeleteView
   - Called before deletion
   - Use for: Soft deletes, archiving, logging

### Example Custom Implementation

```python
def perform_create(self, serializer):
    # Set the current user as creator
    serializer.save(created_by=self.request.user)
    
    # Send notification
    send_notification("New book created!")
```

## Validation

### Built-in Validation
- Model field constraints (max_length, required fields)
- Unique constraints (no duplicate book titles from same author/year)

### Custom Validation
- **Publication Year:** Cannot be in the future (validated in BookSerializer)

### Error Responses

```json
{
  "publication_year": [
    "Publication year cannot be in the future. Current year is 2026."
  ]
}
```

## Future Enhancements

Potential improvements for this API:

1. **Add filtering and search:**
   ```python
   from rest_framework import filters
   filter_backends = [filters.SearchFilter, filters.OrderingFilter]
   search_fields = ['title', 'author__name']
   ```

2. **Add pagination:**
   ```python
   from rest_framework.pagination import PageNumberPagination
   pagination_class = PageNumberPagination
   ```

3. **Add more permission classes:**
   - `IsOwner`: Only allow users to modify their own books
   - `IsAdminOrReadOnly`: Only admins can modify

4. **Add viewsets and routers:**
   - Combine CRUD operations into a single ViewSet
   - Use DRF routers for automatic URL generation

5. **Add API documentation:**
   - Use `drf-yasg` or `drf-spectacular` for Swagger/OpenAPI docs

## License

This project is for educational purposes.