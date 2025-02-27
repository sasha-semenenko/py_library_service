from django.contrib.redirects.models import Redirect
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from books.models import Book
from books.permissions import IsAdminOrAuthenticatedReadOnly
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnBookSerializer,
)
from user.models import Customer


class BorrowingCreateViewSet(generics.CreateAPIView):
    queryset = Borrowing.objects.select_related("customer", "book")
    serializer_class = BorrowingSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)


class BorrowListViewSet(generics.ListAPIView):
    serializer_class = BorrowingListSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("customer", "book")
        customer = self.request.query_params.get("customer", None)
        active = self.request.query_params.get("is_active", None)
        if customer:
            queryset = queryset.filter(customer=customer)
        if active:
            queryset = queryset.filter(is_active=active)
        return queryset


class BorrowingDetailViewSet(generics.RetrieveDestroyAPIView):
    queryset = Borrowing.objects.select_related("customer", "book")
    serializer_class = BorrowingDetailSerializer


class BorrowingReturnBookViewSet(generics.UpdateAPIView):
    queryset = Borrowing.objects.select_related("customer", "book")
    serializer_class = BorrowingReturnBookSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.count_return_book += 1
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
