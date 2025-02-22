from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):

    class CoverChoices(models.TextChoices):
        HARD = "HRD", _("HARD")
        SOFT = "SFT", _("SOFT")

    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    cover = models.CharField(
        max_length=100, choices=CoverChoices, default=CoverChoices.SOFT
    )
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"
