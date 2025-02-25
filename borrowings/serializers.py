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
            "actual_return_date",
            "book",
            "customer",
        )

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs)
        Borrowing.validated_book_inventory(
            attrs["book"].inventory, serializers.ValidationError
        )
        return data


class BorrowingListSerializer(BorrowingSerializer):

    book_title = serializers.CharField(source="book.title", required=True)
    book_inventory = serializers.CharField(source="book.inventory", required=True)
    customer_first_name = serializers.CharField(
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
            "customer_first_name",
            "is_active",
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


class BorrowingReturnBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)
