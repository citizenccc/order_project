from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (RegistrationSerializer, ChangePasswordSerializer, ForgotPasswordSerializer,
                          LoginSerializer, ForgotPassCompleteSerializer, ProfileSerializer)

User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response('Account has been successfully registered', status=201)


class ActivationView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.activate_with_code(activation_code)
        return Response('Your account is activated')


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('You have successfully logged out')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data,
                                              context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Password is changed!')


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('A recovery message has been sent')


class ForgotPasswordCompleteView(APIView):
    def post(self, request, verification_code):
        user = User.objects.get(activation_code=verification_code)
        user.activate_with_code(verification_code)
        serializer = ForgotPassCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Password is updated')


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data.get("name")
        instance.save()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class PrivacyPolicy(APIView):
    def get(self, request):
        return render(request, 'privacy_policy.html')


class SecurityPolicy(APIView):
    def get(self, request):
        return render(request, 'security_policy.html')

