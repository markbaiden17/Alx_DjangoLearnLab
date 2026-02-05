from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book
from datetime import datetime

"""
Test Suite for API Application

This module contains tests for models, serializers, and views.
Run tests with: python manage.py test
"""

class AuthorModelTest(TestCase):
    """Tests for the Author model"""
    
    def setUp(self):
        """Set up test data"""
        self.author = Author.objects.create(name="Test Author")
    
    def test_author_creation(self):
        """Test that an author can be created"""
        self.assertEqual(self.author.name, "Test Author")
        self.assertEqual(str(self.author), "Test Author")
    
    def test_author_book_relationship(self):
        """Test the relationship between Author and Book"""
        book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        self.assertEqual(self.author.books.count(), 1)
        self.assertEqual(self.author.books.first(), book)


class BookModelTest(TestCase):
    """Tests for the Book model"""
    
    def setUp(self):
        """Set up test data"""
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
    
    def test_book_creation(self):
        """Test that a book can be created"""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.publication_year, 2020)
        self.assertEqual(self.book.author, self.author)
    
    def test_book_str_representation(self):
        """Test the string representation of a book"""
        self.assertEqual(str(self.book), "Test Book (2020)")
    
    def test_cascade_delete(self):
        """Test that books are deleted when author is deleted"""
        book_id = self.book.id
        self.author.delete()
        self.assertFalse(Book.objects.filter(id=book_id).exists())


class BookAPITest(APITestCase):
    """Tests for the Book API endpoints"""
    
    def setUp(self):
        """Set up test data and authentication"""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test data
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_get_book_list_unauthenticated(self):
        """Test that unauthenticated users can view book list"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_book_detail_unauthenticated(self):
        """Test that unauthenticated users can view book details"""
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_create_book_authenticated(self):
        """Test that authenticated users can create books"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_book_future_year_validation(self):
        """Test that books cannot be created with future publication year"""
        self.client.force_authenticate(user=self.user)
        
        future_year = datetime.now().year + 10
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.id
        }
        
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_update_book_authenticated(self):
        """Test that authenticated users can update books"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'Updated Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        
        response = self.client.put(f'/api/books/{self.book.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
    
    def test_partial_update_book(self):
        """Test partial update (PATCH) of a book"""
        self.client.force_authenticate(user=self.user)
        
        data = {'title': 'Partially Updated Book'}
        
        response = self.client.patch(f'/api/books/{self.book.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Partially Updated Book')
        self.assertEqual(self.book.publication_year, 2020)  # Unchanged
    
    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete books"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/api/books/{self.book.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books"""
        response = self.client.delete(f'/api/books/{self.book.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 1)  # Book still exists