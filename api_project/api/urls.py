from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Initialize the router and register our ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]