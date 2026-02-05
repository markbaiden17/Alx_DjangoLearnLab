from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book
from datetime import datetime

"""
Test Suite for API Application

This module contains tests for models, serializers, and views.
Updated with tests for filtering, searching, and ordering functionality.
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
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        
        # Create test data
        self.author1 = Author.objects.create(name="J.R.R. Tolkien")
        self.author2 = Author.objects.create(name="George Orwell")
        
        self.book1 = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="The Lord of the Rings",
            publication_year=1954,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author2
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_get_book_list_unauthenticated(self):
        """Test that unauthenticated users can view book list"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_get_book_detail_unauthenticated(self):
        """Test that unauthenticated users can view book details"""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Hobbit')
    
    def test_create_book_authenticated(self):
        """Test that authenticated users can create books"""
        self.client.login(username=self.username, password=self.password)
        
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author1.id
        }
        
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 5)
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author1.id
        }
        
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_future_year_validation(self):
        """Test that books cannot be created with future publication year"""
        self.client.login(username=self.username, password=self.password)
        
        future_year = datetime.now().year + 10
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_update_book_authenticated(self):
        """Test that authenticated users can update books"""
        self.client.login(username=self.username, password=self.password)
        
        data = {
            'id': self.book1.id,
            'title': 'Updated Book',
            'publication_year': 1937,
            'author': self.author1.id
        }
        
        response = self.client.put('/api/books/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book')
    
    def test_partial_update_book(self):
        """Test partial update (PATCH) of a book"""
        self.client.login(username=self.username, password=self.password)
        
        data = {
            'id': self.book1.id,
            'title': 'Partially Updated Book'
        }
        
        response = self.client.patch('/api/books/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Book')
    
    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete books"""
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.delete(f'/api/books/delete/?id={self.book1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books"""
        response = self.client.delete(f'/api/books/delete/?id={self.book1.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 4)


class FilteringTests(APITestCase):
    """Tests for filtering functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.author1 = Author.objects.create(name="J.R.R. Tolkien")
        self.author2 = Author.objects.create(name="George Orwell")
        
        Book.objects.create(title="The Hobbit", publication_year=1937, author=self.author1)
        Book.objects.create(title="The Lord of the Rings", publication_year=1954, author=self.author1)
        Book.objects.create(title="1984", publication_year=1949, author=self.author2)
        Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author2)
        
        self.client = APIClient()
    
    def test_filter_by_publication_year(self):
        """Test filtering by exact publication year"""
        response = self.client.get('/api/books/?publication_year=1949')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_filter_by_author(self):
        """Test filtering by author ID"""
        response = self.client.get(f'/api/books/?author={self.author1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_filter_by_year_gte(self):
        """Test filtering by publication_year greater than or equal"""
        response = self.client.get('/api/books/?publication_year__gte=1950')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_filter_by_year_lte(self):
        """Test filtering by publication_year less than or equal"""
        response = self.client.get('/api/books/?publication_year__lte=1945')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_filter_by_year_range(self):
        """Test filtering by year range using gte and lte"""
        response = self.client.get('/api/books/?publication_year__gte=1945&publication_year__lte=1950')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_filter_multiple_fields(self):
        """Test filtering by multiple fields simultaneously"""
        response = self.client.get(f'/api/books/?author={self.author1.id}&publication_year__gte=1950')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class SearchTests(APITestCase):
    """Tests for search functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.author1 = Author.objects.create(name="J.R.R. Tolkien")
        self.author2 = Author.objects.create(name="George Orwell")
        
        Book.objects.create(title="The Hobbit", publication_year=1937, author=self.author1)
        Book.objects.create(title="The Lord of the Rings", publication_year=1954, author=self.author1)
        Book.objects.create(title="1984", publication_year=1949, author=self.author2)
        Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author2)
        
        self.client = APIClient()
    
    def test_search_by_title(self):
        """Test searching by book title"""
        response = self.client.get('/api/books/?search=hobbit')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_search_by_author_name(self):
        """Test searching by author name"""
        response = self.client.get('/api/books/?search=tolkien')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        response1 = self.client.get('/api/books/?search=TOLKIEN')
        response2 = self.client.get('/api/books/?search=tolkien')
        self.assertEqual(len(response1.data), 2)
        self.assertEqual(len(response2.data), 2)
    
    def test_search_partial_match(self):
        """Test that search finds partial matches"""
        response = self.client.get('/api/books/?search=lord')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_search_no_results(self):
        """Test search with no matching results"""
        response = self.client.get('/api/books/?search=nonexistent')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class OrderingTests(APITestCase):
    """Tests for ordering functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.author1 = Author.objects.create(name="J.R.R. Tolkien")
        self.author2 = Author.objects.create(name="George Orwell")
        
        Book.objects.create(title="The Hobbit", publication_year=1937, author=self.author1)
        Book.objects.create(title="The Lord of the Rings", publication_year=1954, author=self.author1)
        Book.objects.create(title="1984", publication_year=1949, author=self.author2)
        Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author2)
        
        self.client = APIClient()
    
    def test_order_by_title_ascending(self):
        """Test ordering by title (A-Z)"""
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, ['1984', 'Animal Farm', 'The Hobbit', 'The Lord of the Rings'])
    
    def test_order_by_title_descending(self):
        """Test ordering by title (Z-A)"""
        response = self.client.get('/api/books/?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, ['The Lord of the Rings', 'The Hobbit', 'Animal Farm', '1984'])
    
    def test_order_by_year_ascending(self):
        """Test ordering by publication year (oldest first)"""
        response = self.client.get('/api/books/?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1937, 1945, 1949, 1954])
    
    def test_order_by_year_descending(self):
        """Test ordering by publication year (newest first)"""
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1954, 1949, 1945, 1937])
    
    def test_default_ordering(self):
        """Test that default ordering is by -publication_year"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1954, 1949, 1945, 1937])
    
    def test_order_by_author(self):
        """Test ordering by author ID"""
        response = self.client.get('/api/books/?ordering=author')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


class CombinedFeaturesTests(APITestCase):
    """Tests for combining filtering, searching, and ordering"""
    
    def setUp(self):
        """Set up test data"""
        self.author1 = Author.objects.create(name="J.R.R. Tolkien")
        self.author2 = Author.objects.create(name="George Orwell")
        
        Book.objects.create(title="The Hobbit", publication_year=1937, author=self.author1)
        Book.objects.create(title="The Lord of the Rings", publication_year=1954, author=self.author1)
        Book.objects.create(title="1984", publication_year=1949, author=self.author2)
        Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author2)
        
        self.client = APIClient()
    
    def test_filter_and_order(self):
        """Test combining filtering and ordering"""
        response = self.client.get(f'/api/books/?author={self.author1.id}&ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_search_and_order(self):
        """Test combining search and ordering"""
        response = self.client.get('/api/books/?search=the&ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_filter_search_and_order(self):
        """Test combining all three features"""
        response = self.client.get(
            f'/api/books/?author={self.author1.id}&search=lord&ordering=-publication_year'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_filter_by_range_and_order(self):
        """Test filtering by year range and ordering"""
        response = self.client.get(
            '/api/books/?publication_year__gte=1940&publication_year__lte=1950&ordering=publication_year'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1945, 1949])