from django.core.mail import send_mail
from rest_framework import serializers

from apps.order.models import OrderItems, Order
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)

    class Meta:
        model = Order
        exclude = ('user', 'id', 'created_at',)

    def create(self, validated_data):
        items = validated_data.pop('items')
        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user
        order = Order.objects.create(user=user)
        order_items = []
        total = 0
        for item in items:
            product = item['product']
            quantity = item['quantity']
            total += float(item['product'].price) * float(item['quantity'])
            order_item = OrderItems(product=product, order=order, quantity=quantity)
            order_items.append(order_item)
        OrderItems.objects.bulk_create(order_items)
        order.total_sum = total
        order.save()
        admins_email = list(User.objects.filter(is_staff=True).values_list('email', flat=True))
        send_mail('New order ',
                  f'Description: {order}\nUser: {user}',
                  user.email,
                  [user for user in admins_email])
        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        orders = Order.objects.filter()
        for order in orders.iterator():
            representation['outlet'] = order.product.values('outlet__city__city', 'outlet__city__id')
        return representation
