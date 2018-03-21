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
from rest_framework.pagination import PageNumberPagination
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
        return Response({'token': token.key, 'id': user.id, 'username': user.username, 'last_login': user.last_login},
                        status=status.HTTP_200_OK)


class LoginFacebookView(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        service = accounts_services.UserService()
        try:
            user = service.login_facebook(request.data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'id': user.id, 'username': user.username, 'last_login': user.last_login},
                        status=status.HTTP_200_OK)


class LoginInstagramView(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        return Response({})


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


class TermsConditionsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        terms = accounts_models.TermsCondition.objects.all().first()
        serializer = accounts_serializers.TermsConditionsSerializers(terms, many=False).data
        return Response(serializer, status=status.HTTP_200_OK)


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
        return Response({"detail": "la creacion de tu cuenta se ha realizado con exito"},
                        status=status.HTTP_201_CREATED)


class RequestRecoverPassword(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        recover = accounts_services.RecoverPasswordService()
        try:
            user = recover.check_email(request.data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        if notifications_views.recover_password(user, request):
            #expire = datetime.now() + timedelta(minutes=10)
            #accounts_tasks.disable_code_recovery_password.apply_async(args=[user.id], eta=expire)
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
            user = recover.check_code(request.data)
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
    
    @detail_route(methods=['put'], url_path='assign-image/(?P<id_image>[0-9]+)',
                  permission_classes=(permissions.IsAuthenticated,))
    def assign_image(self, request, pk=None, id_image=None):
        instance = self.get_object()
        service = accounts_services.ProfileUser()
        try:
            profile = service.assing_image_profile(instance, id_image)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(profile, many=False).data
        serializer['detail'] = 'Tu imagen de perfil ha sido cambiada exitosamente'
        return Response(serializer, status=status.HTTP_200_OK)
    
    @detail_route(methods=['get'], url_path='assign-image',
                  permission_classes=(permissions.IsAuthenticated,))
    def get_image_profile(self, request, pk=None, id_image=None):
        instance = self.get_object()
        service = accounts_services.ProfileUser()
        try:
            images_profile = service.list_image_profile(instance)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        serializer = accounts_serializers.ImageSerializer(images_profile, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @detail_route(methods=['post'], url_path='upload-image',
                  permission_classes=(permissions.IsAuthenticated,))
    def upload_image(self, request, pk=None):
        instance = request.user
        service = accounts_services.ProfileUser()
        try:
            user = service.upload_images(instance, request.data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(user, many=False).data
        serializer['detail'] = 'Has subido una imagen a tu perfil exitosamente'
        return Response(serializer, status=status.HTTP_201_CREATED)
    
    @detail_route(methods=['delete'], url_path='delete-image/(?P<id_image>[0-9]+)',
                  permission_classes=(permissions.IsAuthenticated,))
    def delete_image(self, request, pk=None, id_image=None):
        instance = request.user
        service = accounts_services.ProfileUser()
        try:
            user = service.delete_images(instance, id_image)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(user, many=False).data
        serializer['detail'] = 'Se ha eliminado una imagen de tu perfil exitosamente'
        return Response(serializer, status=status.HTTP_200_OK)

    @detail_route(methods=['put'], url_path='change-password',
                  permission_classes=(permissions.IsAuthenticated,))
    def change_password(self, request, pk=None):
        instance = request.user
        service = accounts_services.ProfileUser()
        try:
            profile = service.change_password(instance, request.data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        profile.auth_token.delete()
        token, created = Token.objects.get_or_create(user=profile)
        return Response({'detail': 'Su contraseña ha sido cambiada exitosamente',
                         'token': token.key,
                         'id': profile.id,
                         'username': profile.username, 
                         'last_login': profile.last_login}, status=status.HTTP_200_OK)


class PublicProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        service = accounts_services.PublicFeedService()
        try:
            user = service.public_profile(request.user, pk)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        serializer = accounts_serializers.PublicProfileUserSerializers(user, many=False).data
        try:
            distance = service.distance_user(request.user, user,
                                             request.GET.get('latitud'),request.GET.get('longitud'))
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        serializer["distance"] = distance
        return Response(serializer, status=status.HTTP_200_OK)


class PublicProfileImagesViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = accounts_models.Image.objects.all()

    def list(self, request):
        service = accounts_services.UploadImagePublicProfileService()
        try:
            image = service.list(request.user)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        paginator = PageNumberPagination()
        context = paginator.paginate_queryset(image, request)
        serializer = accounts_serializers.ImagePublicSerializer(context, many=True).data
        return paginator.get_paginated_response(serializer)

    def create(self, request):
        service = accounts_services.UploadImagePublicProfileService()
        try:
            image = service.create(request.user, request.data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        serializer = accounts_serializers.ImagePublicSerializer(image, many=False).data
        serializer['detail'] = "La imagen se ha subido a tu profile publico con exito"
        return Response(serializer, status=status.HTTP_201_CREATED)

    @detail_route(methods=['put'], url_path='like/(?P<id_user>[0-9]+)',
                  permission_classes=(permissions.IsAuthenticated,))
    def update_image(self, request, pk=None, id_user=None):
        service = accounts_services.UploadImagePublicProfileService()
        try:
            image = service.update(request.user, request.data, pk, id_user)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        serializer = accounts_serializers.ImagePublicSerializer(image, many=False).data
        serializer['detail'] = "se ha editado la imagen con exito"
        return Response(serializer, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        service = accounts_services.UploadImagePublicProfileService()
        try:
            image = service.delete(request.user, pk)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "La imagen a sido borrada con exito de su perfil publico"},
                        status=status.HTTP_200_OK)


class PublicFeedView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        service = accounts_services.PublicFeedService()
        try:
            public_feed = service.list(request.user)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        paginator = PageNumberPagination()
        context = paginator.paginate_queryset(public_feed, request)
        serializer_data = accounts_serializers.PublicFeedSerializers(context, many=True).data
        try:
            serializer = service.distance_feed(request.user, request.GET.get('latitud'),
                                               request.GET.get('longitud'), serializer_data)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        return paginator.get_paginated_response(serializer)