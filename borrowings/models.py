from django.db import models

from books.models import Book
from user.models import Customer


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowed_book")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="borrowed_customer")

    class Meta:
        ordering = ["-borrow_date"]
        unique_together = ["borrow_date", "expected_return_date", "actual_return_date"]

    def __str__(self) -> str:
        return f"{self.book.title} - {self.borrow_date}"
