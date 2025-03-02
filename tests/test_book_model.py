from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer

URL_BOOK_LIST = reverse("books:book-list")
URL_BOOK_CREATE = reverse("books:book-create")


def get_detail_url(pk: int):
    return reverse("books:book-retrieve-update-destroy", kwargs={"pk": pk})


def sample_book(**params) -> Book:
    default = {
        "title": "Sample Title",
        "author": "Sample Author",
        "cover": "SFT",
        "inventory": 20,
        "daily_fee": 1.24,
    }
    default.update(params)
    return Book.objects.create(**default)


class UnAuthenticatedBookTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_book_create(self):
        default = {
            "title": "Create Book",
            "author": "Sample Author",
            "cover": "HRD",
            "inventory": 14,
            "daily_fee": 0.51,
        }
        response = self.client.post(URL_BOOK_CREATE, data=default)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_book_detail(self):
        customer = sample_book(title="Custom Book")
        customer_ = sample_book()
        response = self.client.get(get_detail_url(customer.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_list(self):
        response = self.client.get(URL_BOOK_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticatedBookTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="auth@user.com", password="123pass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_book(self):
        book = sample_book(title="Custom Book")
        book_ = sample_book()
        response = self.client.get(get_detail_url(book.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BookSerializer(book)
        serializer_ = BookSerializer(book_)
        self.assertEqual(response.data, serializer.data)
        self.assertNotEqual(response.data, serializer_.data)

    def test_create_book_forbidden(self):
        data = {
            "title": "Create Title",
            "author": "Create Author",
            "cover": "SFT",
            "inventory": 7,
            "daily_fee": 3.49,
        }
        response = self.client.post(URL_BOOK_CREATE, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAuthenticationBookTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="super@user.com", password="123pass123"
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        data = {
            "title": "Create Title allow",
            "author": "Create Author allow",
            "cover": "HRD",
            "inventory": 54,
            "daily_fee": 0.13,
        }
        response = self.client.post(URL_BOOK_CREATE, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_book(self):
        book = sample_book()
        response = self.client.delete(get_detail_url(book.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_book(self):
        book = sample_book()
        data = {
            "title": "Update Title",
            "author": "Update Author",
            "cover": "HRD",
            "inventory": 64,
            "daily_fee": 0.05,
        }
        response = self.client.put(get_detail_url(book.pk), data=data)
        book.title = data["title"]
        book.author = data["author"]
        book.cover = data["cover"]
        book.inventory = data["inventory"]
        book.daily_fee = data["daily_fee"]
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
