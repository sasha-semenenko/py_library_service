from rest_framework import viewsets, generics, mixins

from books.models import Book
from books.permissions import IsAdminOrAuthenticatedReadOnly
from books.serializers import BookSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)


class BookListViewSet(generics.ListAPIView):
    serializer_class = BookSerializer


class BookUpdateDestroyViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
