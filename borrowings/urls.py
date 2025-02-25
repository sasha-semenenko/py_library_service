from django.urls import path

from borrowings.views import (
    BorrowingCreateViewSet,
    BorrowListViewSet,
    BorrowingDetailViewSet,
    BorrowingReturnBookViewSet,
)

app_name = "borrowings"

urlpatterns = [
    path("create/", BorrowingCreateViewSet.as_view(), name="create"),
    path("borrowings/", BorrowListViewSet.as_view(), name="borrow-list"),
    path(
        "borrowings/<int:pk>/", BorrowingDetailViewSet.as_view(), name="borrow-detail"
    ),
    path(
        "borrowings/<int:pk>/return/",
        BorrowingReturnBookViewSet.as_view(),
        name="return book",
    ),
]
