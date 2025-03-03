from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer, BorrowingDetailSerializer, BorrowingReturnBookSerializer

URL_BORROWINGS_LIST = reverse("borrowings:borrow-list")
URL_BORROWINGS_CREATE = reverse("borrowings:create")

def return_book(pk: int):
    return reverse("borrowings:return book", kwargs={"pk": pk})

def detail_url(pk: int):
    return reverse("borrowings:borrow-detail", kwargs={"pk": pk})


def sample_borrow(**params):
    book = Book.objects.create(
        title="Sample Title",
        author="Sample Author",
        cover="SFT",
        inventory=20,
        daily_fee=1.24,
    )

    data = {
        "borrow_date": "2025-02-20",
        "expected_return_date": "2025-02-28",
        "book": book,
        "customer": None,
        "is_active": True,
    }
    data.update(params)
    return Borrowing.objects.create(**data)


class UnAuthenticatedBorrowingsTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated(self):
        response = self.client.get(URL_BORROWINGS_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="borrow@user.com", password="pass123pass"
        )
        self.client.force_authenticate(self.user)

    def test_borrowings_list(self):
        borrow_1 = sample_borrow(customer=self.user)
        book_2 = Book.objects.create(
            title="Book Second",
            author="borrow Author",
            cover="HRD",
            inventory=10,
            daily_fee=1.74,
        )
        borrow_2 = Borrowing.objects.create(
            borrow_date="2025-02-22",
            expected_return_date="2025-02-27",
            book=book_2,
            customer=self.user,
            is_active=True,
        )

        response = self.client.get(URL_BORROWINGS_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        borrows = Borrowing.objects.all()
        serializer_list = BorrowingListSerializer(borrows, many=True)

        self.assertEqual(response.data, serializer_list.data)

    def test_borrowings_detail(self):
        borrow = sample_borrow(customer=self.user)
        response = self.client.get(detail_url(borrow.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BorrowingDetailSerializer(borrow)
        self.assertEqual(response.data, serializer.data)

    def test_borrowings_filter_by_customer(self):
        borrow = sample_borrow(customer=self.user)
        book_2 = Book.objects.create(
            title="Book Second",
            author="borrow Author",
            cover="HRD",
            inventory=10,
            daily_fee=1.74,
        )
        borrow_2 = Borrowing.objects.create(
            borrow_date="2025-02-22",
            expected_return_date="2025-02-27",
            book=book_2,
            customer=get_user_model().objects.create_user(
            email="test@user.com", password="pass123pass"
        ),
            is_active=True,
        )

        response = self.client.get(
            URL_BORROWINGS_LIST, kwargs={"customer": self.user.pk}
        )

        serializer = BorrowingListSerializer(borrow)

        self.assertEqual(response.data[1], serializer.data)

    def test_borrowings_filter_by_is_active(self):
        borrow = sample_borrow(customer=self.user)
        response = self.client.get(
            URL_BORROWINGS_LIST, kwargs={"is_active": True}
        )
        serializer = BorrowingListSerializer(borrow)

        self.assertEqual(response.data[0], serializer.data)

    def test_borrowings_create_forbidden(self):
        book = Book.objects.create(
            title="Create Book Title",
            author="Author",
            cover="SFT",
            inventory=32,
            daily_fee=4.1,
        )

        data = {
            "borrow_date": "2025-02-01",
            "expected_return_date": "2025-02-03",
            "book": book,
            "customer": self.user,
            "is_active": True,
        }
        response = self.client.post(URL_BORROWINGS_CREATE, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAuthenticatedBorrowingsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="super@user.com", password="pass24pass"
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing(self):
        book = Book.objects.create(
            title="Create Book Title",
            author="Author",
            cover="SFT",
            inventory=32,
            daily_fee=4.1,
        )

        data = {
            "borrow_date": "2025-02-01",
            "expected_return_date": "2025-02-03",
            "book": book.id,
            "customer": self.user.id,
        }
        response = self.client.post(URL_BORROWINGS_CREATE, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_borrowings_delete(self):
        borrow = sample_borrow(customer=self.user)
        response = self.client.delete(detail_url(borrow.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_borrowings_return_book(self):
        borrow = sample_borrow(customer=self.user)
        response = self.client.put(return_book(borrow.pk), data={"actual_return_date": "2025-02-01"})
        borrow.book.inventory += 1
        borrow.actual_return_date = "2025-02-01"
        serializer = BorrowingReturnBookSerializer(borrow)
        self.assertEqual(response.data, serializer.data)
        res = self.client.get(URL_BORROWINGS_LIST)
        serializer_ = BorrowingListSerializer(borrow)
        self.assertEqual(res.data[0]["book_inventory"], serializer_.data["book_inventory"])
