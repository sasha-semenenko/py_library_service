from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics

from user.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class CustomerCreateViewSet(generics.CreateAPIView):
    serializer_class = CustomerSerializer


class ManageCustomerViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer

    def get_object(self):
        return self.request.user
