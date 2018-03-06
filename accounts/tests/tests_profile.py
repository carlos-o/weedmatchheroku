from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password
from accounts import models as accounts_models
from payment import models as payment_models

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


class ProfileTestCase(APITestCase):

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
        user2 = accounts_models.User.objects.create(
            username="lomax120",
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email="carlos5_zeta@hotmail.com",
            password=make_password(data.get('password')),
            direction=data.get('direction'),
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            country_id=str(country.id),
        )
        self.user = user
        self.user2 = user2

    def tests_profile(self):
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
        self.assertEqual(response.data.get('number_card'), "5675", "error not equal")

        response = self.c.get('/payment/card/{}/'.format(response.data.get('id')))
        self.assertEqual(response.status_code, 200, "error en enviar la data")
        self.assertEqual(response.data.get('number_card'), "5675", "error not equal")

        response = self.c.get('/profile/{}/'.format(self.user.id))
        self.assertEqual(response.status_code, 200, "error al traer la informacion")
        print("informacion del usuario", response.data)

    def tests_profile_updated_image(self):
        self.c.force_authenticate(user=self.user2)
        value = {
            "first_name": "carlos",
            "last_name": "olivero",
            "number_card": "12345678912345675",
            "type_card": "mastercard",
            "date_expiration": "2022-02-01"
        }
        response = self.c.post('/payment/card/', value, format='json')
        self.assertEqual(response.status_code, 201, "error al crear la tarjeta")
        self.assertEqual(response.data.get('number_card'), "5675", "error not equal")

        response = self.c.get('/payment/card/{}/'.format(response.data.get('id')))
        self.assertEqual(response.status_code, 200, "error en enviar la data")
        self.assertEqual(response.data.get('number_card'), "5675", "error not equal")

        img = 'profile_test.jpg'
        with open(img, 'rb') as infile:
            response = self.c.put('/profile/{}/uploadImage/'.format(self.user2.id), {"image": infile})
            self.assertEqual(response.status_code, 200, "error al traer la informacion")
            self.assertEqual(response.data.get('image'),
                             "http://127.0.0.1:8000/media/profile/profile_test.jpg", "error not equal")
            print("informacion del usuario", response.data)

        response = self.c.get('/profile/{}/'.format(self.user2.id))
        self.assertEqual(response.status_code, 200, "error al traer la informacion")
        self.assertEqual(response.data.get('username'), self.user2.username, "error not equal")

    def tests_profile_updated_image_fail(self):
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

        #img = 'nobody_m.original.jpg'
        #with open(img, 'rb') as infile:
        response = self.c.put('/profile/{}/uploadImage/'.format(self.user.id), {"image": ""})
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)

    def tests_profile_update(self):
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

        response = self.c.get('/payment/card/{}/'.format(response.data.get('id')))
        self.assertEqual(response.status_code, 200, "error en enviar la data")
        self.assertEqual(response.data.get('number_card'), "5675", "error not equal")

        update = {
            "username": "solrac",
            "first_name": "carlos",
            "last_name": "olivero",
            "direction": "18 de octubre calle LM entre av. 3 y 4 casa numero 4-55",
            "country": "222",
            "description": "hola a todo soy nuevo"
        }

        response = self.c.put('/profile/{}/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 200, "error al traer la informacion")
        self.assertEqual(response.data.get('direction'),
                         "18 de octubre calle LM entre av. 3 y 4 casa numero 4-55", "error not equal")
        self.assertEqual(response.data.get('description'),
                         "hola a todo soy nuevo", "error not equal")
        print("informacion editada del usuario", response.data)

    def tests_profile_update_password(self):
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
        credit_card = payment_models.CreditCard.objects.get(user=self.user.id)
        print(credit_card)

        response = self.c.get('/payment/card/{}/'.format(response.data.get('id')))
        self.assertEqual(response.status_code, 200, "error en enviar la data")
        self.assertEqual(response.data.get('number_card'), "5675", "error not equal")

        login = {
            "username": "solrac",
            "password": "1234qwer"
        }

        response = self.c.post('/login/', login, format='json')
        self.assertEqual(response.status_code, 200, "fail login")
        self.assertEqual(response.data.get('username'), login.get('username'), "not equal")

        update = {
            "old_password": "1234qwer",
            "new_password": "carlos123"
        }

        response = self.c.put('/profile/{}/changePassword/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 200, "error al traer la informacion")
        print(response.data)

        login = {
            "username": "solrac",
            "password": "carlos123"
        }

        response = self.c.post('/login/', login, format='json')
        self.assertEqual(response.status_code, 200, "fail login")
        self.assertEqual(response.data.get('username'), login.get('username'), "not equal")
        print(response.data)

    def tests_profile_update_password_fail(self):
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
        credit_card = payment_models.CreditCard.objects.get(user=self.user.id)
        print(credit_card)
        """
            test old_password vacio
        """
        update = {
            "old_password": "",
            "new_password": "carlos123"
        }

        response = self.c.put('/profile/{}/changePassword/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
        """
            test new_password vacio
        """
        update = {
            "old_password": "1234qwer",
            "new_password": ""
        }

        response = self.c.put('/profile/{}/changePassword/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
        """
            test old_password no coincide con su contraseña
        """
        update = {
            "old_password": "1234qwer1",
            "new_password": "carlos123"
        }

        response = self.c.put('/profile/{}/changePassword/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
        """
            test new_password la contraseña debe ser con caracteres y numeros
        """
        update = {
            "old_password": "1234qwer",
            "new_password": "carlos"
        }

        response = self.c.put('/profile/{}/changePassword/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)

    def tests_profile_update_fail(self):
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
        credit_card = payment_models.CreditCard.objects.get(user=self.user.id)
        print(credit_card)
        """
            test username vacio
        """
        update = {
            "username": "",
            "first_name": "carlos",
            "last_name": "olivero",
            "direction": "18 de octubre calle LM entre av. 3 y 4 casa numero 4-55",
            "country": "222"
        }

        response = self.c.put('/profile/{}/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
        """
            test first_name vacio
        """
        update = {
            "username": "solrac",
            "first_name": "",
            "last_name": "olivero",
            "direction": "18 de octubre calle LM entre av. 3 y 4 casa numero 4-55",
            "country": "222"
        }

        response = self.c.put('/profile/{}/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
        """
            test last_name vacio
        """
        update = {
            "username": "solrac",
            "first_name": "carlos",
            "last_name": "",
            "direction": "18 de octubre calle LM entre av. 3 y 4 casa numero 4-55",
            "country": "222"
        }
        response = self.c.put('/profile/{}/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
        """
            test direccion vacio
        """
        update = {
            "username": "solrac",
            "first_name": "carlos",
            "last_name": "olivero",
            "direction": "",
            "country": "222"
        }
        response = self.c.put('/profile/{}/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
        """
            test country vacio
        """
        update = {
            "username": "solrac",
            "first_name": "carlos",
            "last_name": "olivero",
            "direction": "18 de octubre calle LM entre av. 3 y 4 casa numero 4-55",
            "country": ""
        }
        response = self.c.put('/profile/{}/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
        """
            test country no existe
        """
        update = {
            "username": "solrac",
            "first_name": "carlos",
            "last_name": "olivero",
            "direction": "18 de octubre calle LM entre av. 3 y 4 casa numero 4-55",
            "country": "2222"
        }
        response = self.c.put('/profile/{}/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
        """
            test country tiene que ser string
        """
        update = {
            "username": "solrac",
            "first_name": "carlos",
            "last_name": "olivero",
            "direction": "18 de octubre calle LM entre av. 3 y 4 casa numero 4-55",
            "country": 222
        }
        response = self.c.put('/profile/{}/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
        """
            test username ya existe
        """
        update = {
            "username": "lomax120",
            "first_name": "carlos",
            "last_name": "olivero",
            "direction": "18 de octubre calle LM entre av. 3 y 4 casa numero 4-55",
            "country": "222"
        }

        response = self.c.put('/profile/{}/'.format(self.user.id), update, format='json')
        self.assertEqual(response.status_code, 400, "error al traer la informacion")
        print(response.data)
