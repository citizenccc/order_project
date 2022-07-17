from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from rest_framework import serializers

from apps.order.models import Order
from apps.order.serializers import OrderSerializer
from main.settings import ALLOWED_HOSTS, EMAIL_HOST_USER, ALLOWED_HOSTS, HOST

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)
    name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email has already been registered')
        return email

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords should match')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        user.send_activation_email()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6, required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    new_password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_old_password(self, old_pass):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_pass):
            raise serializers.ValidationError('Input correct password')
        return old_pass

    def validate(self, attrs):
        new_pass1 = attrs.get('new_password')
        new_pass2 = attrs.get('new_password_confirm')
        if new_pass1 != new_pass2:
            raise serializers.ValidationError('Passwords don\'t match')
        return attrs

    def set_new_password(self):
        new_pass = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This user hasn\'t been registered yet')
        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail('Restore password',
                  f'Restore code: https://{HOST}/api/v1/auth/forgot_password_complete/{user.activation_code}/',
                  EMAIL_HOST_USER,
                  [user.email])


class ForgotPassCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User is not found')
        if password1 != password2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User is not found')
        return email

    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email,
                                password=password,
                                request=request)
            if not user:
                raise serializers.ValidationError('Wrong email or password')
        else:
            raise serializers.ValidationError('Email and password are mandatory')
        data['user'] = user
        return data


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    last_name = serializers.CharField()
    contact_number = serializers.CharField()
    contact_method = serializers.CharField()

    class Meta:
        model = User
        fields = ('name', 'last_name', 'contact_number', 'contact_method')

    def validate(self, data):
        name = data.get('name')
        last_name = data.get('last_name')
        contact_number = data.get('contact_number')
        contact_method = data.get('contact_method')
        data['name'] = name
        data['last_name'] = last_name
        data['contact_number'] = contact_number
        data['contact_method'] = contact_method
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['orders'] = OrderSerializer(Order.objects.filter(user=instance).filter(status="received"), many=True).data
        print(instance)
        return representation
