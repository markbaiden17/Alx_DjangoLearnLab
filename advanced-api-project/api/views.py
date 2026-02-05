from rest_framework import generics
from django_filters import rest_framework
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

# View for retrieving all books
class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Read only access for unauthenticated users
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Define filterable fields
    filterset_fields = ['author', 'title', 'publication_year']

    # Define searchable fields
    search_fields = ['author', 'title']

    # Define ordering fields
    ordering_fields = ['publication_year', 'title']

    # Default ordering
    ordering = ['title']

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

    def perform_update(self, serializer):
        serializer.save()

# View for removing a book
class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Only authenticated users can delete books
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()