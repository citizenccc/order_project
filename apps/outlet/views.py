from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from apps.outlet.filters import OutletFilter
from apps.outlet.models import Outlet
from apps.outlet.serializers import OutletSerializer


class OutletViewSet(ModelViewSet):
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = OutletFilter
    search_fields = ['title', ]
    ordering_fields = ['city', ]

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes = [IsAdminUser,]
        return super().get_permissions()
