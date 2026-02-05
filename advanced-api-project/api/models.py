from django.db import models

# Author model represents a book author
# This model has a one-to-many relationship with Book (one author can write multiple books)
class Author(models.Model):
    # The author's full name
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Book model represents a book written by an author
# Each book is linked to one author via a foreign key relationship
class Book(models.Model):
    # The title of the book
    title = models.CharField(max_length=200)
    
    # The year the book was published
    publication_year = models.IntegerField()
    
    # Foreign key to Author - creates a one-to-many relationship
    # related_name='books' allows us to access an author's books via author.books.all()
    # on_delete=models.CASCADE ensures that if an author is deleted, their books are also deleted
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title