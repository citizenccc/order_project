from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.order.filters import OrderFilter
from apps.order.models import Order
from apps.order.permissions import DenyAll, IsAuthorPermission
from apps.order.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = OrderFilter
    ordering_fields = ['created_at', ]

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [IsAuthorPermission()]
        elif self.action in ['update', 'partial_update']:
            return [IsAdminUser()]
        else:
            return [DenyAll()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset