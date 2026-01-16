from django.shortcuts import render
from django.views.generic import DetailView
from urllib3 import request
from .models import Book, Library

# Create your views here.
#Function-based view to display all books
def all_books_view(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

#View to display all books available in a library
class LibraryBooksView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'