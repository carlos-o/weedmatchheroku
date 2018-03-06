from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password
from accounts import models as accounts_models

data = {
    "username": "solrac",
    "first_name": "carlos",
    "last_name": "olivero",
    "email": "carlosolivero2@gmail.com",
    "password": "1234qwer",
    "direction": "18 de octubre",
    "latitud": 12.312312,
    "longitud": -70.125896,
    "country": "222",
    "age": "1992-02-08"
}


class LoginTestCase(APITestCase):

    def setUp(self):
        country = accounts_models.Country.objects.create(name='Venezuela', code='VE') 
        self.c = APIClient()
        user = accounts_models.User.objects.create(
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=make_password(data.get('password')),
            direction=data.get('direction'),
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            country_id=str(country.id),
            age=data.get('age')
        )
        self.user = user

    def test_login(self):
        value = {"username": "solrac", "password": "1234qwer"}
        response = self.c.post('/login/', value, format='json')
        self.assertEqual(response.status_code, 200, "fail login")
        self.assertEqual(response.data.get('username'), value.get('username'), "not equal")
        print(response.data)

    def test_username_fail(self):
        value = {"username": "solrac5", "password": "1234qwer"}
        response = self.c.post('/login/', value, format='json')
        self.assertEqual(response.status_code, 400, "fail login")
        self.assertEqual(response.data.get('detail'), 'El usuario no existe en el sistema', "not equal")
        print(response.data)

    def test_password_fail(self):
        value = {"username": "solrac", "password": "qwer123"}
        response = self.c.post('/login/', value, format='json')
        self.assertEqual(response.status_code, 400, "fail login")
        self.assertEqual(response.data.get('detail'),
                         'Contraseña invalida, porfavor escriba correctamente su contraseña', "not equal")
        print(response.data)

