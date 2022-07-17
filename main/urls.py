from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="Open Sky API",
      default_version='v1',
      description="Test description",
    ),
   public=True,
)


urlpatterns = [
    path('', schema_view.with_ui()),
    path('admin/', admin.site.urls),
    path('api/v1/', include("apps.product.urls")),
    path('api/v1/', include("apps.category.urls")),
    path('api/v1/', include("apps.outlet.urls")),
    path('api/v1/', include("apps.order.urls")),
    path('api/v1/auth/', include('apps.account.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Sky Dinning'
admin.site.index_title = 'Administration'
admin.site.site_title = 'Sky Dinning'