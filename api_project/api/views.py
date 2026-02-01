from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Create your views here.
# View that uses the serializer to retrieve and return book data
class BookList(generics.ListAPIView):
     queryset = Book.objects.all()
     serializer_class = BookSerializer

# View that handles CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer