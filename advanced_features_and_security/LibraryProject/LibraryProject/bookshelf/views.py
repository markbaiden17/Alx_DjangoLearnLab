from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from .models import Book, Library

# --- Book Views with Required Permissions ---

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    # Add a book
    return render(request, 'bookshelf/add_book.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/edit_book.html', {'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/delete_book.html', {'book': book})

# --- Existing Library & Auth Views ---

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'bookshelf/library_detail.html'
    context_object_name = 'library'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'bookshelf/register.html', {'form': form})

def logout_user(request):
    logout(request)
    return render(request, 'bookshelf/logout.html')

# --- Role-based views (Keep these if you need them for other tasks) ---

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'bookshelf/admin_view.html')

# --- Secure Search View (Step 3: Prevent SQL Injection) ---

def search_books(request):
    query = request.GET.get('q', '') 
    
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
        
    return render(request, 'bookshelf/book_list.html', {'books': books})