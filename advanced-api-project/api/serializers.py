from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# BookSerializer handles serialization of Book model instances
# Includes custom validation to ensure publication_year is not in the future
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    # Custom validation method for publication_year field
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year is invalid.")
        return value

# AuthorSerializer handles serialization of Author model instances
# Includes nested BookSerializer to serialize all related books
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer for related books
    # many=True because one author can have multiple books
    # read_only=True because we don't want to create books through the author endpoint
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']