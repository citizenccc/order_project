from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from apps.category.models import Category

# from apps.outlet.models import Outlet
from .models import Product, ProductImage



class ProductImagesAdmin(admin.TabularInline):
    model = ProductImage
    max_num = 5
    extra = 1



class ProductResource(resources.ModelResource):
    # outlet = fields.Field(column_name='outlet', attribute='outlet', widget=ForeignKeyWidget(Outlet, 'title'))
    category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(Category, 'name'))

    class Meta:
        model = Product
        fields = ('id', 'category', 'title', 'description', 'weight', 'price', 'quantity')
        skip_unchanged = True
        report_skipped = True
        export_order = ('category', 'title', 'description', 'weight', 'price', 'quantity')


class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    inlines = [ProductImagesAdmin]
    # list_filter = ['outlet']
    list_display = ('id', 'category', 'title', 'description', 'weight', 'price', 'quantity')
    ordering = ('id',)

admin.site.register(Product, ProductAdmin)