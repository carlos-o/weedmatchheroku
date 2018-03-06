from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from accounts import models as accounts_models
from payment import models as paymet_models

data = {
    "username": "soulrac",
    "first_name": "carlos",
    "last_name": "olivero",
    "email": "carlos5_zeta@hotmail.com",
    "password": "1234qwer",
    "direction": "18 de octubre",
    "latitud": 12.312312,
    "longitud": -70.125896
}


class CreditCardTestCase(APITestCase):

    def setUp(self):
        self.c = APIClient()
        user = accounts_models.User.objects.create(
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=make_password(data.get('password')),
            direction=data.get('direction'),
            latitud=data.get('latitud'),
            longitud=data.get('longitud')
        )
        self.user = user

    def test_list_retrieve_credit_card(self):
        """
            test para ver la lista de tarjetas de credito asociada a la cuenta
        """
        card = paymet_models.CreditCard()
        card1 = paymet_models.CreditCard()
        value = {
            "first_name": "eduardo",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "visa",
            "date_expiration": "2022-02-01",
            "user_id": str(self.user.id)
        }
        value2 = {
            "first_name": "eduardo",
            "last_name": "olivero",
            "number_card": "09123718313712399",
            "type_card": "visa",
            "date_expiration": "2022-02-01",
            "user_id": str(self.user.id)
        }
        for key in value2.keys():
            setattr(card, key, value2[key])
        card.save(force_insert=True)
        for key in value.keys():
            setattr(card1, key, value[key])
        card1.save(force_insert=True)
        self.c.force_authenticate(user=self.user)
        response = self.c.get('/payment/card/')
        print("respuesta de la lista", response.data)
        self.assertEqual(response.status_code, 200, "error en enviar la data")

        response = self.c.get('/payment/card/{}/'.format(card.id))
        print("respuesta de un solo elemento", response.data)
        self.assertEqual(response.status_code, 200, "error en enviar la data")

    def test_create_credit_card(self):
        """
            test para comprobar el ingreso de una tarjeta de credito sin errores en el json
        """
        self.c.force_authenticate(user=self.user)
        value = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "mastercard",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        self.assertEqual(response.status_code, 201, "error al crear la tarjeta")
        credit_card = paymet_models.CreditCard.objects.filter(user=self.user.id).values()
        print("valores del test para agregar la tarjeta: ", credit_card)

    def test_error_create_credit_card(self):
        """
            test para comprobar el ingreso de una tarjeta de credito sin errores en el json
        """
        self.c.force_authenticate(user=self.user)
        """
        first_name vacio
        """
        value = {
            "first_name": "",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "mastercard",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("first_name vacio", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
                first_name menor de 3 caracteres
                """
        value = {
            "first_name": "ca",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "mastercard",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("first_name menor de 3 caracteres", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
            last_name vacio
        """
        value = {
            "first_name": "carlos",
            "last_name": "",
            "number_card": "12345678912345675",
            "type_card": "mastercard",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("last_name vacio", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
            last_name menor a 3 caracateres
        """
        value = {
            "first_name": "carlos",
            "last_name": "ol",
            "number_card": "12345678912345675",
            "type_card": "mastercard",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("last_name menor a 3 caracteres", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
            number_card vacio
        """
        value = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "",
            "type_card": "mastercard",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("number_card vacio", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
            number_card menor a 15 caracteres
        """
        value = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "12345678901244",
            "type_card": "mastercard",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("number_card mayor a 15 caracteres", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
             number_card solo puede ser numeros
        """
        value = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "12345678901244s",
            "type_card": "mastercard",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("number_card solo pueden ser numeros", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
            type_card vacio
        """
        value = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("type_card vacio", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
            type_card no existen los tipos de tarjetas en la base de datos
        """
        value = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "visas",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("type_card no existen los tipos de tarjetas en la base de datos ", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
            date_expiration vacio
        """
        value = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "mastercard",
            "date_expiration": ""
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("date_expiration vacio", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
            date_expiration no es una fecha valida
        """
        value = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "mastercard",
            "date_expiration": "2018-10-2s3"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("date_expiration no es una fecha valida", response.data)
        self.assertEqual(response.status_code, 400, "error")
        """
            date_expiration fecha fuera de rango
        """
        value = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "mastercard",
            "date_expiration": "2018-11-31"
        }
        response = self.c.post('/payment/card/', value, format='json')
        print("date_expiration fecha fuera de rango", response.data)
        self.assertEqual(response.status_code, 400, "error")

    def test_update_credit_card(self):
        """
            test para comprobar la edicion de una tarjeta de credito ya agregada sin errores en el json
        """
        self.c.force_authenticate(user=self.user)
        card = paymet_models.CreditCard()
        value = {
            "first_name": "eduardo",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "visa",
            "date_expiration": "2022-02-01",
            "user_id": str(self.user.id)
        }
        for key in value.keys():
            setattr(card, key, value[key])
        card.save(force_insert=True)
        print("valores iniciales de la tarjeta de credito", value)
        data_edit = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "mastercard",
            "date_expiration": "2022-02-01"
        }
        response = self.c.put('/payment/card/{}/'.format(card.id), data_edit, format='json')
        self.assertEqual(response.status_code, 200, "error al editar la tarjeta")
        credit_card = paymet_models.CreditCard.objects.filter(user=self.user.id).values()
        print("valores despues de editar: ", credit_card)

    def test_delete_credit_card(self):
        """
            test para comprobar la eliminacion de una tarjeta de credito ya agregada sin errores en el json
        """
        self.c.force_authenticate(user=self.user)
        card = paymet_models.CreditCard()
        value = {
            "first_name": "eduardo",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "visa",
            "date_expiration": "2022-02-01",
            "user_id": str(self.user.id)
        }
        for key in value.keys():
            setattr(card, key, value[key])
        card.save(force_insert=True)
        card_id = card.id
        response = self.c.delete('/payment/card/{}/'.format(card.id))
        print(response.data)
        self.assertEqual(response.status_code, 200, "error al eliminar la tarjeta")
        try:
            credit_card = paymet_models.CreditCard.objects.filter(user=self.user.id).values()
        except paymet_models.CreditCard.DoesNotExist as e:
            print(e)
            raise e

