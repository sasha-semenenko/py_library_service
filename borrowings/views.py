from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics
from rest_framework.response import Response


from books.permissions import IsAdminOrAuthenticatedReadOnly
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnBookSerializer,
)


class BorrowingCreateViewSet(generics.CreateAPIView):
    queryset = Borrowing.objects.select_related("customer", "book")
    serializer_class = BorrowingSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)


class BorrowListViewSet(generics.ListAPIView):
    serializer_class = BorrowingListSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("customer", "book")
        customer = self.request.query_params.get("customer", None)
        active = self.request.query_params.get("is_active", None)
        if customer:
            queryset = queryset.filter(customer=customer)
        if active:
            queryset = queryset.filter(is_active=active)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="customer",
                description="Filter by customer id (example: ?customer=1)",
                type=int,
            ),
            OpenApiParameter(
                name="is_active",
                description="Filter by is_active status (example: ?is_active=True)",
                type=bool,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BorrowingDetailViewSet(generics.RetrieveDestroyAPIView):
    queryset = Borrowing.objects.select_related("customer", "book")
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)


class BorrowingReturnBookViewSet(generics.UpdateAPIView):
    queryset = Borrowing.objects.select_related("customer", "book")
    serializer_class = BorrowingReturnBookSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

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
