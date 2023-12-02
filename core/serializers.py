from datetime import datetime
from django.http import request
from rest_framework import serializers
from rest_framework.response import Response
from core.models import Customer, Notifications, DetailOrderProduct, Product, Order
# from django.conf import settings
# from django.forms.models import model_to_dict


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class DetailOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailOrderProduct
        fields = '__all__'

    def to_representation(self, instance):
        product = ProductSerializer(read_only=True)
        order = OrderSerializer(read_only=True)
        self.fields['product'] = product
        self.fields['order'] = order

        return super(DetailOrderProductSerializer, self).to_representation(instance)

class NotificationListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

    def to_representation(self, instance):
        full_name = CustomerSerializer(read_only=True)
        self.fields['customer'] = full_name

        return super(NotificationListViewSerializer, self).to_representation(instance)
