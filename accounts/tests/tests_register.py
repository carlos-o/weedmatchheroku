from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password
from accounts import models as accounts_models

data = {
    "username": "nigixx",
    "first_name": "luisana",
    "last_name": "olivero",
    "email": "luisanaolivero@gmail.com",
    "password": "1234qwer",
    "direction": "18 de octubre",
    "latitud": 12.312312,
    "longitud": -70.125896,
    "country": "222",
    "age": "1995-05-21"
}


class RegisterTestCase(APITestCase):
    """
        tests para registrar un cliente de manera normal 
    """

    def setUp(self):
        country = accounts_models.Country.objects.create(name='Venezuela', code='VE')
        self.c = APIClient()
        self.user_data = {
            "username": "solrac",
            "first_name": "carlos",
            "last_name": "olivero",
            "email": "carlosolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": -70.125896,
            "country": str(country.id),
            "age": "1992-02-08"
        }
        user = accounts_models.User.objects.create(
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=make_password(data.get('password')),
            direction=data.get('direction'),
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            country_id= str(country.id),
            age=data.get('age')
        )
        self.user_data2 = user
    
    def test_register_success(self):
        data = self.user_data
        response = self.c.post("/register/", data, format='json')
        print("register success ", response.data)
        self.assertEqual(response.status_code, 201, "fail register")
        self.assertEqual(response.data.get('detail'), "la creacion de tu cuenta se ha realizado con exito", "not equal")
        user = accounts_models.User.objects.get(username=data.get('username'))
        print(user)

        value = {"username": "solrac", "password": "1234qwer"}
        response = self.c.post('/login/', value, format='json')
        self.assertEqual(response.status_code, 200, "fail login")
        self.assertEqual(response.data.get('username'), value.get('username'), "not equal")
        print(response.data)

    def test_register_fail(self):
        """
            test username vacio
        """
        data = {
            "username": "",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test first_name vacio
        """
        data = {
            "username": "dark12",
            "first_name": "",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test last_name vacio
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test email vacio
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test email no valido
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardo_olivero12.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test password vacio
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test direccion vacio
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "",
            "latitud": 12.312312,
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test latitud vacio
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test latitud fuera de rango
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 91.212341,
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test latitud string
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": "90.212341",
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test longitud vacio
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test longitud fuera de rango
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": 181.123456,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test longitud string
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": "189.123343",
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test country vacio
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": 179.123343,
            "country": "",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test country no existe
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": 170.123343,
            "country": "2222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test age vacio
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": 170.123343,
            "country": "2222",
            "age": ""
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test age la fecha no es valida
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": 170.123343,
            "country": "2222",
            "age": "1992-0s2-08"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)
        """
            test age la fecha esta fuera del rango
        """
        data = {
            "username": "dark12",
            "first_name": "eduardo",
            "last_name": "olivero",
            "email": "eduardoolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": 170.123343,
            "country": "2222",
            "age": "1992-02-31"
        }
        response = self.c.post("/register/", data, format='json')
        self.assertEqual(response.status_code, 400, "fail register")
        print(response.data)

    def test_register_fail_username(self):
        data_initial = {
            "username": "nigixx",
            "first_name": "luisana",
            "last_name": "olivero",
            "email": "luisanaolivero1@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data_initial, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 400, "fail register")
        self.assertEqual(response.data.get('detail').get('username'), "El nombre de usuario existe, porfavor escriba otro nombre de usuario", "not equal")
    
    def test_register_fail_email(self):
        data_initial = {
            "username": "nigixx12",
            "first_name": "luisana",
            "last_name": "olivero",
            "email": "luisanaolivero@gmail.com",
            "password": "1234qwer",
            "direction": "18 de octubre",
            "latitud": 12.312312,
            "longitud": -70.125896,
            "country": "222",
            "age": "1992-02-08"
        }
        response = self.c.post("/register/", data_initial, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 400, "fail register")
        self.assertEqual(response.data.get('detail').get('email'), "El correo existe, porfavor escriba otro correo", "not equal")

