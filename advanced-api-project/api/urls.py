from django.urls import path
from .views import ListView, DetailView, CreateView, UpdateView, DeleteView

# URL patterns for the API endpoints
urlpatterns = [
    # Endpoint for listing all books
    path('books/', ListView.as_view(), name='book-list'),

    # Endpoint for retrieving a single book by ID
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),

    # Endpoint for creating a new book
    path('books/create/', CreateView.as_view(), name='book-create'),

    # Endpoint for updating an existing book by ID
    path('books/update/', UpdateView.as_view(), name='book-update'),

    # Endpoint for deleting a book by ID
    path('books/delete/', DeleteView.as_view(), name='book-delete'),
]