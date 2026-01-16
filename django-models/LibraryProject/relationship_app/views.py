from django.shortcuts import render, redirect
from urllib3 import request
from .models import Book 
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout

# Create your views here.

#Function-based view to display all books


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('list_books') # Or wherever you want them to go
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def logout_user(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')