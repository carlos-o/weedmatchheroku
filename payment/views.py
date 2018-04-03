from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from payment import models as payment_models
from payment import validations as payment_validations
from payment import serializers as payment_serializers
from payment import services as payment_services
import re
import base64
import requests
import json
from datetime import datetime
from datetime import timedelta
from weedmatch import settings
from django.utils.translation import ugettext_lazy as _


class CreditCardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = payment_serializers.CreditCardSerializers
    queryset = payment_models.CreditCard.objects.all()

    def list(self, request, *args, **kwargs):
        service = payment_services.CreditCardService()
        try:
            card = service.list(request.user)
        except Exception as e:
            return Response(json.loads(str(e)), status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(card, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        service = payment_services.CreditCardService()
        try:
            card = service.create(request.data, request.user)
        except Exception as e:
            return Response({"detail": json.loads(str(e).replace("'", '"'))}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(card, many=False).data
        serializer['detail'] = str(_("You have successfully added a credit card to your account"))
        return Response(serializer, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        service = payment_services.CreditCardService()
        try:
            card = service.update(instance, request.data, request.user)
        except Exception as e:
            return Response({"detail": json.loads(str(e).replace("'", '"'))}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(card, many=False).data
        serializer['detail'] = str(_("Your credit card information has been successfully edited"))
        return Response(serializer, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = payment_services.CreditCardService()
        try:
            card = service.delete(instance, request.user)
        except Exception as e:
            return Response(json.loads(str(e)), status=status)
        return Response({"detail": str(_("The credit card has been successfully deleted from your account"))},
                        status=status.HTTP_200_OK)
