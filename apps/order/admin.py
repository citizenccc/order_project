from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Order, OrderItems
from import_export.admin import ExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

User = get_user_model()


class OrderItemAdmin(admin.TabularInline):
    model = OrderItems
    max_num = 150
    extra = 1


class OrderResource(resources.ModelResource):
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'email'))

    class Meta:
        model = Order
        fields = ('user', 'status', 'total_sum', 'created_at')


class OrderAdmin(ExportActionModelAdmin):
    resource_class = OrderResource
    list_filter = ['created_at']
    inlines = [OrderItemAdmin, ]


admin.site.register(Order, OrderAdmin)
