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

#status-code-response
STATUS = {
    "200": status.HTTP_200_OK,
    "201": status.HTTP_201_CREATED,
    "202": status.HTTP_202_ACCEPTED,
    "204": status.HTTP_204_NO_CONTENT,
    "400": status.HTTP_400_BAD_REQUEST,
    "401": status.HTTP_401_UNAUTHORIZED,
    "404": status.HTTP_404_NOT_FOUND,
    "500": status.HTTP_500_INTERNAL_SERVER_ERROR
}


class CreditCardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = payment_serializers.CreditCardSerializers
    queryset = payment_models.CreditCard.objects.all()

    def list(self, request, *args, **kwargs):
        service = payment_services.CreditCardService()
        try:
            card = service.list(request.user)
        except Exception as e:
            return Response(json.loads(str(e)), status=STATUS['400'])
        serializer = self.get_serializer(card, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        service = payment_services.CreditCardService()
        try:
            card = service.create(request.data, request.user)
        except Exception as e:
            return Response({"detail": json.loads(str(e).replace("'", '"'))}, status=STATUS['400'])

        serializer = self.get_serializer(card, many=False).data
        serializer['detail'] = 'La tarjeta de credito se ha agregado a tu cuenta con exito'
        return Response(serializer, status=STATUS['201'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        service = payment_services.CreditCardService()
        try:
            card = service.update(instance, request.data, request.user)
        except Exception as e:
            return Response({"detail": json.loads(str(e).replace("'", '"'))}, status=STATUS['400'])
        serializer = self.get_serializer(card, many=False).data
        serializer['detail'] = 'La información de la tarjeta de credito se ha editado con exito'
        return Response(serializer, status=STATUS['200'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = payment_services.CreditCardService()
        try:
            card = service.delete(instance, request.user)
        except Exception as e:
            return Response(json.loads(str(e)), status=STATUS['400'])
        return Response({"detail": "la tarjeta de credito ha sido eliminada de tu cuenta con exito"}, status=STATUS['200'])
