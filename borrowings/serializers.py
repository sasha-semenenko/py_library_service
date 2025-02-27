from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing
from user.serializers import CustomerSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
            "customer",
        )


class BorrowingListSerializer(BorrowingSerializer):

    book_title = serializers.CharField(source="book.title", required=True)
    book_inventory = serializers.CharField(source="book.inventory", required=True)
    customer_full_name = serializers.CharField(
        source="customer.get_full_name", read_only=True
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_title",
            "book_inventory",
            "customer_full_name",
            "is_active",
            "count_return_book",
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True, many=False)
    customer = CustomerSerializer(read_only=True, many=False)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "customer",
        )


class BorrowingReturnBookSerializer(BorrowingSerializer):

    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)
