from django.urls import path, include
from rest_framework import routers
from .views import OutletViewSet
router = routers.DefaultRouter()

router.register('outlet', OutletViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
urlpatterns += router.urls