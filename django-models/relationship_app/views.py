from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Create your views here.
#Function-based view to display all books
def all_books_view(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, 'relationship_app/all_books.html', context)

#View to display all books available in a library
class LibraryBooksView(DetailView):
    model = Library
    template_name = 'relationship_app/library_books.html'
    context_object_name = 'library'