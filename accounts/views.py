from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from accounts import models as accounts_models
from accounts import serializers as accounts_serializers
from accounts import services as accounts_services
from accounts import tasks as accounts_tasks
from notifications import views as notifications_views
#from account import permissions as accounts_permissions
import re
import base64
import requests
import json
from datetime import datetime
from datetime import timedelta
from weedmatch import settings


class LoginView(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        service = accounts_services.UserService()
        try:
            user = service.login(request.data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'id': user.id, 'username': user.username, 'last_login': user.last_login})


class LogoutView(APIView):
    """
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        service = accounts_services.UserService()
        try:
            user = service.logut(request.user)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Te has desconectado del sistema'}, status=status.HTTP_200_OK)
    

class CountryView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        country = accounts_models.Country.objects.all()
        serializer = accounts_serializers.CountrySerializers(country, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        register = accounts_services.RegisterUserService()
        try:
            data = register.create(request.data) 
        except Exception as e:
            return Response({"detail": json.loads(str(e).replace("'", '"'))}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "la creacion de tu cuenta se ha realizado con exito"}, status=status.HTTP_201_CREATED)


class RequestRecoverPassword(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        recover = accounts_services.RecoverPasswordService()
        try:
            user = recover.checkEmail(request.data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        if notifications_views.recover_password(user, request):
            expire = datetime.now() + timedelta(minutes=10)
            accounts_tasks.disableCodeRecoveryPassword.apply_async(args=[user.id], eta=expire)
            return Response({'detail': 'el correo se ha enviado con exito'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Problemas del servidor no se ha podido realizar la peticion'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecoverPassword(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        recover = accounts_services.RecoverPasswordService()
        try:
            user = recover.checkCode(request.data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'La contraseña se ha cambiado con exito'}, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = accounts_serializers.ProfileUserSerializers
    queryset = accounts_models.User.objects.all()

    def list(self, request, *args, **kwargs):
        service = accounts_services.ProfileUser()
        try:
            profile = service.list(request.user)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        if len(profile) != 1:
            serializer = self.get_serializer(profile, many=True)    
        serializer = self.get_serializer(profile[0], many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        service = accounts_services.ProfileUser()
        try:
            profile = service.update(instance, request.data)
        except Exception as e:
            return Response({"detail": json.loads(str(e).replace("'", '"'))}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(profile, many=False).data
        serializer['detail'] = 'Tu información personal ha sido editada con exito'
        return Response(serializer, status=status.HTTP_200_OK)
    
    @detail_route(methods=['put'], permission_classes=(permissions.IsAuthenticated,))
    def uploadImage(self, request, pk=None):
        instance = request.user
        service = accounts_services.ProfileUser()
        try:
            profile = service.changeProfileImage(instance, request.data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(profile, many=False).data
        serializer['detail'] = 'Tu imagen de perfil ha sido cambiada exitosamente'
        return Response(serializer, status=status.HTTP_200_OK)

    @detail_route(methods=['put'], permission_classes=(permissions.IsAuthenticated,))
    def changePassword(self, request, pk=None):
        instance = request.user
        service = accounts_services.ProfileUser()
        try:
            profile = service.changePassword(instance, request.data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        profile.auth_token.delete()
        token, created = Token.objects.get_or_create(user=profile)
        return Response({'detail': 'Su contraseña ha sido cambiada exitosamente',
                         'token': token.key,
                         'id': profile.id,
                         'username': profile.username, 
                         'last_login': profile.last_login}, status=status.HTTP_200_OK)
