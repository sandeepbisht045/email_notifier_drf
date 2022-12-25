from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Products
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator
from datetime import date
from email_notifier_api.settings import payment_mode as payment

class ProductsListAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class ProductsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        extra_kwargs = {
            'product_name': {'required': True},
            'purchase_date': {'required': True},
            'expiry_date': {'required': True},
            'expires_in': {'required': True},
            'vendor_email': {'required': True},
            'vendor_name': {'required': True},
            'payment_mode': {'required': True},
        }

    def validate(self, data):
        purchase_date = data['purchase_date']
        expiry_date = data['expiry_date']
        payment_mode = data['payment_mode']
        today = date.today()

        if purchase_date > today:
            raise serializers.ValidationError('Purchase date cannot be greater than today.')
        if expiry_date < purchase_date:
            raise serializers.ValidationError('Expiry date cannot be less than purchase date.')
        if payment_mode not in payment.keys():
            print(payment_mode)
            print(tuple(payment.keys()))
            raise serializers.ValidationError('Enter valid value')

        return data




