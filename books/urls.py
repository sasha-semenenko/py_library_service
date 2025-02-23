from django.urls import path

from books.views import BookCreateView, BookUpdateDestroyViewSet, BookListViewSet

app_name = "books"

urlpatterns = [
    path("create/", BookCreateView.as_view(), name="book-create"),
    path("books/", BookListViewSet.as_view(), name="book-list"),
    path(
        "books/<int:pk>/",
        BookUpdateDestroyViewSet.as_view(),
        name="book-retrieve-update-destroy",
    ),
]
