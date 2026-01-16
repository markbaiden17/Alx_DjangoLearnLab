from models import Author, Book, Library, Librarian

#Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name) 
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return []
    
#List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return []
    
#Retrieve librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Librarian.objects.get(library=library_name)
        return library
    except Library.DoesNotExist:
        return []