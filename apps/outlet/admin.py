from django.contrib import admin
from .models import Outlet, OutletImage
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from ..city.models import City


class OutletImageAdmin(admin.TabularInline):
    model = OutletImage
    max_num = 5
    extra = 1


class OutletResource(resources.ModelResource):
    city = fields.Field(column_name='city', attribute='city', widget=ForeignKeyWidget(City, 'city'))

    class Meta:
        model = Outlet
        fields = ('id', 'city', 'title')
        skip_unchanged = True
        report_skipped = True
        export_order = ('city', 'title')


class OutletAdmin(ImportExportActionModelAdmin):
    resource_class = OutletResource
    inlines = [OutletImageAdmin]
    list_filter = ['city']
    list_display = ('id', 'city', 'title', )
    ordering = ('id',)


admin.site.register(Outlet, OutletAdmin)
