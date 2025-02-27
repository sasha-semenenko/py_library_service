from datetime import date

from django.db import models
from rest_framework.exceptions import ValidationError

from books.models import Book
from user.models import Customer


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowed_book"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="borrowed_customer"
    )
    is_active = models.BooleanField(default=True)
    count_return_book = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ["-borrow_date"]
        unique_together = ["borrow_date", "expected_return_date", "actual_return_date"]

    def __str__(self) -> str:
        return f"{self.book.title} - {self.borrow_date}"

    @staticmethod
    def validated_book_inventory(inventory: int, return_book: int, error_to_raise):
        if inventory < 0:
            raise error_to_raise(
                f"Inventory in book is {inventory} that is not more or equal 0"
            )
        if return_book == 2:
            raise error_to_raise("You can not return book twice")

    def clean(self):
        Borrowing.validated_book_inventory(
            self.book.inventory, self.count_return_book, error_to_raise=ValidationError
        )

    def save(self, *args, **kwargs):
        if not self.actual_return_date:
            self.book.inventory -= 1
        else:
            self.book.inventory += 1
        self.full_clean()
        self.book.save()
        return super(Borrowing, self).save(*args, **kwargs)
