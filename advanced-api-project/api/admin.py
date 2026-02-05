from django.contrib import admin
from .models import Author, Book

"""
Django Admin Configuration

This module registers the models with Django's admin interface,
allowing easy management of Authors and Books through the admin panel.
"""

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface for Author model.
    
    Features:
    - Display author name in list view
    - Search by author name
    - Order by name
    """
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book model.
    
    Features:
    - Display book details in list view
    - Filter by author and publication year
    - Search by title and author name
    - Order by publication year (newest first)
    """
    list_display = ['id', 'title', 'author', 'publication_year']
    list_filter = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_year', 'title']
    
    # Show author name in the form with a helpful dropdown
    autocomplete_fields = []
    raw_id_fields = []