from rest_framework import generics
from django_filters import rest_framework
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer

# View for retrieving all books
class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Read only access for unauthenticated users
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Define filterable fields
    filterset_fields = {
        'title': ['exact', 'icontains'],
        'author': ['exact'],
        'publication_year': ['exact', 'gte', 'lte'],
    }

    # Define searchable fields
    search_fields = ['title', 'author__name']

    # Define ordering fields
    ordering_fields = ['publication_year', 'title']

    # Default ordering
    ordering = ['-publication_year']

# View for retrieving a single book by ID
class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Read only access for unauthenticated users
    permission_classes = [IsAuthenticatedOrReadOnly]

# View for adding a new book
class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Only authenticated users can create new books
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

# View for modifying an existing book (partial modification)
class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Only authenticated users can update books
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Look for the identifier in request data or query parameters
        obj_id = (self.request.data.get("id") or 
                  self.request.query_params.get("id") or 
                  self.request.data.get("pk") or
                  self.request.query_params.get("pk"))
        return get_object_or_404(Book, id=obj_id)

    def perform_update(self, serializer):
        serializer.save()

# View for removing a book
class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Only authenticated users can delete books
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Look for the identifier in request data or query parameters
        obj_id = (self.request.data.get("id") or 
                  self.request.query_params.get("id") or 
                  self.request.data.get("pk") or
                  self.request.query_params.get("pk"))
        return get_object_or_404(Book, id=obj_id)

    def perform_destroy(self, instance):
        instance.delete()