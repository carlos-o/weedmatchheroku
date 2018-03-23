from accounts import models as accounts_models
from accounts import validations as accounts_validations
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg
from datetime import datetime
from weedmatch import settings
import googlemaps
import re
import os
import math
import requests
import json
import datetime as datetime_module
from django.contrib.auth.models import Group


class UserService:
    """
        this class controls the login of the user by the different routes in a traditional way,
        via facebook and instagram, in addition to the closing of the session
    """
    def login(self, data: dict)->accounts_models.User:
        """
            A user registered in the system obtain access to weedmatch
            this function fails if the user's credentials do not match
            those registered in the system

            :param data: user information.
            :type data: dict.
            :return: user
            :raises: ValueError
        """
        if not data.get('username'):
            raise ValueError('{"detail": "El nombre de usuario no puede estar vacio"}')
        if not data.get('password'):
            raise ValueError('{"detail": "La contraseña no puede estar vacia"}')
        try:
            user = accounts_models.User.objects.get(Q(username__iexact=data.get('username')) |
                                                    Q(email__iexact=data.get('username')))
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail": "El usuario no existe en el sistema"}')
        if not user.is_active:
            raise ValueError('{"detail": "Cuenta inactiva, su cuenta esta bloqueada"}')
        if not user.check_password(data.get('password')):
            raise ValueError('{"detail": "Contraseña invalida, porfavor escriba correctamente su contraseña"}')
        return user

    def login_facebook(self, data: dict)->accounts_models.User:
        """
            A user gets access to weedmatch with their Facebook credentials
            this function fails if the user's Facebook token does not match
            when the request is made to the api the Facebook

            :param data: access_token of facebook, latitude and longitude.
            :type data: dict.
            :return: user
            :raises: ValueError
        """
        if not data.get('access_token'):
            raise ValueError('{"detail": "El campo access_token no puede estar vacio"}')
        if not data.get('latitud'):
            raise ValueError('{"detail": "El campo latitud no puede estar vacio"}')
        if not data.get('longitud'):
            raise ValueError('{"detail": "El campo longitud no puede estar vacio"}')

        # Requests to Facebook API
        get_code_url = 'https://graph.facebook.com/oauth/client_code'
        access_token_url = 'https://graph.facebook.com/v2.9/oauth/access_token'
        graph_api_url = 'https://graph.facebook.com/v2.12/me?fields=id,name,email,birthday,picture.width(200).height(200)'

        params = {
            'client_id': settings.FACEBOOK_CLIEND_ID,
            'redirect_uri': "192.168.0.21",
            'client_secret': settings.FACEBOOK_SECRET,
            'access_token': data.get('access_token')
        }

        r = requests.get(graph_api_url, params=params)
        if r.status_code == 400:
            raise ValueError('{"detail":"El token de acceso no pertenece a ese usuario"}')
        # Data obtained by calling Facebook API with user token
        profile = json.loads(r.text)
        username = profile.get('email').split("@")[0]
        user_register = accounts_models.User.objects.filter(facebook_id=profile.get('id'))
        if user_register.exists():
            return user_register[0]
        if accounts_models.User.objects.filter(username=username).exists():
            raise ValueError('{"detail":"El nombre de usuario existe, porfavor escriba otro nombre de usuario"}')

        # Requests to GoogleMap Api
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)
        try:
            reverse_geocode_result = gmaps.reverse_geocode((float(data.get('latitud')), float(data.get('longitud'))))
        except googlemaps.exceptions.ApiError:
            raise ValueError('{"detail": "La llave que se utilzo no funciona"}')
        direction = reverse_geocode_result[1].get('formatted_address')
        count = len(reverse_geocode_result) - 1
        country_map = reverse_geocode_result[count].get('formatted_address')
        try:
            country = accounts_models.Country.objects.filter(name=country_map)
        except accounts_models.Country.DoesNotExist:
            raise ValueError('{"country": "el pais no esta registrado en el sistema"}')
        image = profile.get('picture').get('data').get('url')
        age = profile.get('birthday')
        if not age:
            age = datetime.now().strftime('%Y-%m-%d')
        else:
            age = datetime.strptime(age, "%m/%d/%Y").strftime("%Y-%m-%d")
        if not image:
            image = ""
        user = accounts_models.User.objects.create(
            username=username,
            first_name=profile.get('name'),
            email=profile.get('email'),
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            country_id=country[0].id,
            image=image,
            age=age,
            direction=direction,
            sex=accounts_models.User.SEX_OTHER,
            facebook_id=profile.get('id'),
            facebook_access_token=data.get('access_token')
        )
        print(user)
        group = Group.objects.get(name='WeedMatch')
        user.groups.add(group)
        return user

    def login_instagram(self, data: dict)->accounts_models.User:
        """
            A user gets access to weedmatch with their instagram credentials

            :param data: access_token of instagram, latitude and longitude.
            :type data: dict.
            :return: user
            :raises: ValueError
        """
        return True

    def image_user(self, user: accounts_models.User):
        """
            return the image profile of user
            :param user: user weedmatch.
            :type user: Model User.
            :return: user.image or "" or user.image with path
            :raises: None
        """
        if not user.image:
            return ""
        if re.search("https", user.image):
            return user.image
        return settings.URL + settings.MEDIA_URL + str(user.image)

    def logut(self, user: accounts_models.User)-> accounts_models.User:
        """
            the user disconnects from the system weedmatch

            :param user: user weedmatch.
            :type user: Model User.
            :return: user
            :raises: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        user.last_login = datetime.now()
        user.save()
        user.auth_token.delete()
        return user


class ProfileUser:

    def list(self, user: accounts_models.User)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"user": "para poder ver su informacion su cuenta debe estar activa"}')
        data = accounts_models.User.objects.filter(id=user.id)
        if user.is_staff:
            data = accounts_models.User.objects.all()
        return data
    
    def update(self, user: accounts_models.User, data: dict)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"user": "para poder ver su informacion su cuenta debe estar activa"}') 
        validator = accounts_validations.ProfileUserValidate(data)
        if validator.validate() is False:
            raise ValueError(validator.errors())
        exists = accounts_models.User.objects.filter(username=data.get('username')).exists()
        if user.username == data.get('username') and exists:
            user.username = data.get('username')
        elif not exists:
            user.username = data.get('username')
        else:
            raise ValueError('{"username":"El nombre de usuario existe, porfavor escriba otro nombre de usuario"}')
        if not accounts_models.Country.objects.filter(id=data.get('country')).exists():
            raise ValueError('{"country": "el pais no esta registrado en el sistema"}')
        if data.get('description'):
            user.description = data.get('description')
        if not data.get('last_name'):
            data['last_name']= ""
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.direction = data.get('direction')
        user.country_id = data.get('country')
        user.match_sex = data.get('match_sex')
        user.save()
        return user
    
    def change_password(self, user: accounts_models.User, data: dict)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"user": "para poder ver su informacion su cuenta debe estar activa"}') 
        if not data.get('old_password'):
            raise ValueError('{"detail": "El campo vieja contraseña no puede esta vacio"}')
        if not data.get('new_password'):
            raise ValueError('{"detail": "El campo nueva contraseña no puede esta vacio"}')
        if not user.check_password(data.get('old_password')):
            raise ValueError('{"detail": "La contraseña ingresada no coincide con tu actual contraseña"}')
        if not re.match(r'(?=.*[A-Za-z]+)(?=.*\d+)', data.get('new_password')):
            raise ValueError('{"detail": "La contraseña debe tener caracteres y numeros"}')
        user.password = make_password(data.get('new_password')) 
        user.save()
        return user
    
    def upload_images(self, user: accounts_models.User, data: dict)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}') 
        if not data.get('image'):
            raise ValueError('{"detail": "El campo imagen de perfil no puede estar vacio"}')
        if user.count_image < 6:        
            images_profile = accounts_models.ImageProfile.objects.create(
                user_id=user.id,
                image_profile=data.get('image')
            )
            if not user.image:
                user.assign_image_profile(str(images_profile.image_profile))
            user.count_increment()
        else:
            raise ValueError('{"detail": "no puedes subir mas de 6 imagenes en el profile"}')
        return user
    
    def delete_images(self, user: accounts_models.User, id_image: int)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        try:
            image = accounts_models.ImageProfile.objects.get(id=id_image,user_id=user.id) 
        except accounts_models.ImageProfile.DoesNotExist:
            raise ValueError('{"detail": "no existe la imagen en tu profile"}')
        if user.image == str(image.image_profile):
            user.image = ""
            user.save()
        os.remove(os.path.join(settings.MEDIA_ROOT,str(image.image_profile.name)))
        image.delete()
        user.count_delete()
        return user

    def list_image_profile(self, user: accounts_models.User,)-> accounts_models.ImageProfile:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        try:
            images_profile = accounts_models.ImageProfile.objects.filter(user_id=user.id) 
        except accounts_models.ImageProfile.DoesNotExist:
            raise ValueError('{"detail": "no existe la imagen en tu profile"}')
        return images_profile

    def assing_image_profile(self, user: accounts_models.User, id_image: int)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        try:
            image = accounts_models.ImageProfile.objects.get(id=id_image,user_id=user.id) 
        except accounts_models.ImageProfile.DoesNotExist:
            raise ValueError('{"detail": "no existe la imagen en tu profile"}')
        user.assign_image_profile(str(image.image_profile))
        return user


class UploadImagePublicProfileService:

    def list(self, user: accounts_models.User)->accounts_models.Image:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        images = accounts_models.PublicFeed.objects.filter(user_id=user.id)
        return images

    def retrieve(self, user: accounts_models.User, pk: int)->accounts_models.Image:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        images = accounts_models.PublicFeed.objects.filter(user_id=pk)
        return images

    def create(self, user: accounts_models.User, data: dict)->accounts_models.Image:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        if not data.get('image'):
            raise ValueError('{"detail": "El campo imagen del feed publico no puede estar vacio"}')
        if not data.get('comment'):
            data['comment'] = ""
        if not data.get('latitud'):
            data['latitud'] = user.latitud
        if not data.get('longitud'):
            data['longitud'] = user.longitud
        try:
            public_image = accounts_models.Image.objects.create(
                user_id=user.id,
                image=data.get('image'),
                state=data.get('comment'),
                latitud=data.get('latitud'),
                longitud=data.get('longitud')
            )
            public_feed = accounts_models.PublicFeed.objects.create(
                user_id=user.id,
                id_image=public_image.id,
                image=str(public_image.image),
                state=public_image.state,
                latitud=data.get('latitud'),
                longitud=data.get('longitud'),
                date_creation=public_image.created
            )
        except Exception as e:
            raise ValueError('{"detail": "ha ocurrido un error al guardar la imagen"}')
        return public_image

    def update(self, user: accounts_models.User, data: dict, id_image: int, id_user: int)->accounts_models.Image:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        try:
            imagen = accounts_models.PublicFeed.objects.get(id_image=id_image, user_id=id_user)
        except accounts_models.Image.DoesNotExist:
            raise ValueError('{"detail": "La imagen no existe en tu perfil publico"}')
        if not data.get('like'):
            raise ValueError('{"detail": "el campo like no puede estar vacio"}')
        if data.get('like') == "True" or data.get('like') == "true":
            imagen.increment_like()
            try:
                like_user = accounts_models.LikeUser.objects.get(id_user=user.id, id_public_feed=imagen.id)
                like_user.change_like(True)
            except accounts_models.LikeUser.DoesNotExist:
                like_create = accounts_models.LikeUser.objects.create(
                    id_user=user.id,
                    id_public_feed=imagen.id,
                    like=True
                )
        elif data.get('like') == "False" or data.get('like') == "false":
            imagen.decrement_like()
            like_user = accounts_models.LikeUser.objects.get(id_user=user.id, id_public_feed=imagen.id)
            like_user.change_like(False)
        if not re.search(r'^(true|True|false|False)$', data.get('like')):
            raise ValueError('{"detail":"No se puede anexar un nuevo me gusta a su imagen publica"}')
        return imagen

    def delete(self, user:accounts_models.User, id_image: int)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver la información su cuenta debe estar activa"}')
        try:
            imagen = accounts_models.Image.objects.get(id=id_image, user_id=user.id)
        except accounts_models.Image.DoesNotExist:
            raise ValueError('{"detail": "La imagen no existe en tu feed publico o la has eliminado"}')
        #os.remove(os.path.join(settings.MEDIA_ROOT, str(imagen.image.name)))
        imagen.delete()
        return user


class RegisterUserService:

    def create(self, data: dict) -> accounts_models.User:
        date = data['age'][:10]
        if not date or not data.get('age'):
            raise ValueError('{"age": "El campo de fecha no puede estar vacio"}')
        match = re.match(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', date)
        if not match:
            raise ValueError('{"age": "No es una fecha valida"}')
        try:
            data['age'] = datetime.strptime(date, '%Y-%m-%d')
        except Exception as e:
            raise ValueError('{"age": "el día está fuera de rango por mes"}')
        validator = accounts_validations.RegisterUserValidate(data)
        if validator.validate() is False:
            raise ValueError(validator.errors())
        if accounts_models.User.objects.filter(username=data.get('username')).exists():
            raise ValueError('{"username":"El nombre de usuario existe, porfavor escriba otro nombre de usuario"}')
        if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', data.get('email')):
            raise ValueError('{"email":"por favor escriba una direccion de correo valida"}')
        if accounts_models.User.objects.filter(email=data.get('email')).exists():
            raise ValueError('{"email":"El correo existe, porfavor escriba otro correo"}')
        """
        necesito para la api en produccion el googlemaps api key del cliente
        """
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)
        try:
            reverse_geocode_result = gmaps.reverse_geocode((float(data.get('latitud')), float(data.get('longitud'))))
        except googlemaps.exceptions.ApiError:
            raise ValueError('{"detail": "La llave que se utilzo no funciona"}')
        direction = reverse_geocode_result[1].get('formatted_address')
        count =len(reverse_geocode_result) -1
        country_map = reverse_geocode_result[count].get('formatted_address')
        try:
            country = accounts_models.Country.objects.filter(name=country_map)
        except accounts_models.Country.DoesNotExist:
            raise ValueError('{"country": "el pais no esta registrado en el sistema"}')
        user = accounts_models.User()
        data["country_id"] = country[0].id
        data["direction"] = direction
        data["last_name"] = ""
        for key in data.keys():
            if key == 'password':
                data[key] = make_password(data[key]) 
            setattr(user, key, data[key])
        try:
            user.save(force_insert=True)
        except Exception as e:
            raise ValueError('{"user": "ha ocurrido un error al guardar el usuario"}')
        print(user)
        # add group weedmatch
        group = Group.objects.get(name='WeedMatch')
        user.groups.add(group)
        return user


class RecoverPasswordService:

    def check_email(self, data: dict) -> accounts_models.User:
        if not data.get('email'):
            raise ValueError('{"detail": "el campo correo no puede estar vacio"}')
        try:
            user = accounts_models.User.objects.get(email=data.get('email'))
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail": "el correo no esta registrado en el sistema"}')
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        return user

    def check_code(self, data: dict) -> accounts_models.User:
        if not data.get('code'):
            raise ValueError('{"detail": "El campo codigo no puede estar vacio"}')
        if not data.get('password'):
            raise ValueError('{"detail": "El campo contraseña no puede estat vacio"}')
        try:
            user = accounts_models.User.objects.get(recovery=str(data.get('code')))
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail": "Código que enviaste no coinciden con el registrado en tu cuenta"}')
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        user.password = make_password(str(data.get('password')))
        user.recovery = ''
        user.save()
        return user


class PublicFeedService:

    def list(self, user: accounts_models.User):
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver la información su cuenta debe estar activa"}')
        if user.match_sex == accounts_models.User.SEX_OTHER:
            users = accounts_models.User.objects.all().exclude(username=user.username).exclude(is_superuser=True)
        if user.match_sex == accounts_models.User.SEX_MALE:
            users = accounts_models.User.objects.filter(sex=user.match_sex).exclude(username=user.username)\
                .exclude(is_superuser=True)
        if user.match_sex == accounts_models.User.SEX_FEMALE:
            users = accounts_models.User.objects.filter(sex=user.match_sex).exclude(username=user.username)\
                .exclude(is_superuser=True)
        ids = users.aggregate(users_id=ArrayAgg('id'))
        public_feed = accounts_models.PublicFeed.objects.filter(user_id__in=ids.get('users_id'))
        return public_feed, public_feed.aggregate(id_public_feed=ArrayAgg('id'))
    
    def public_profile(self, user: accounts_models.User, pk: int)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        try:
            public_user = accounts_models.User.objects.get(id=pk)
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail": "el usuario no se encuentra registrado en el sistema"}')
        return public_user

    def distances(self, latA: float, lonA: float, latB: float, lonB: float):
        arccos = math.acos(
            ((math.sin(latA) * math.sin(latB)) + (math.cos(latA) * math.cos(latB))) * math.cos(lonA - lonB))
        result = settings.RADIO_EARTH * arccos
        degrees = (math.pi * result) / 180
        if degrees < 0.9:
            meters = degrees * 1000
            return 999, str(meters)[:3]+" mts"
        if degrees > 1:
            convert = str(degrees)
            value = convert.find(".")
            number = convert[value + 1:value + 2]
            if int(number) >= 5:
                return math.ceil(degrees), str(math.ceil(degrees))[:3]+" km"
            else:
                return degrees, str(degrees)[0:1]+" km"
    
    def time_format(self, date_now, date_result):
        date_string = str(date_result).split(".")[0]
        if len(date_string) == 7:
            if int(date_string[0:1]) >= 1 and int(date_string[0:1]) < 10:
                return date_string[0:1]+" hours"
            if date_string[2:4] == "00":
                if int(date_string[5:6]) == 0:
                    return date_string[6:7]+ " seconds"
                else:
                    return date_string[5:7]+ " seconds"
            if int(date_string[2:3]) == 0:
                #print(date_string[3:4])
                return date_string[3:4] + " minutes"
            else:
                #print(date_string[2:4])
                return date_string[2:4] + " minutes"	
        elif len(date_string) == 8:
            return date_string[0:2] + " hours"
        elif len(date_string) >= 14:
            return date_string[:-13] + " days"
            if int(date_string[:-13]) > 7:
                date = date_now - datetime_module.timedelta(days=int(date_string[:-13]))
            if int(date_now.strftime("%Y")) > int(date.strftime("%Y")):
                return date.strftime("%d the %B the %Y")
            else:
                #print(month[date.strftime("%B")])
                return date.strftime("%d the %B")

    def distance_feed(self, user: accounts_models.User, latitud: str, longitud: str, datas: list):
        if not latitud:
            latitud = user.latitud
        if not longitud:
            longitud = user.longitud
        list_accept = []
        for data in datas:
            distance, str_distance = self.distances(float(data.get('latitud')), float(data.get('longitud')),
                                                    float(latitud), float(longitud))
            if distance == 999:
                data['distance'] = str_distance
                data.pop('latitud')
                data.pop('longitud')
                list_accept.append(data)
            if not distance >= 100: #add userprofile distance user.distance_user
                data['distance'] = str_distance
                data.pop('latitud')
                data.pop('longitud')
                list_accept.append(data)
        datas.clear()
        return list_accept

    def distance_user(self, user: accounts_models.User, user_pk: accounts_models.User, latitud: str, longitud: str):
        public_image_user = accounts_models.Image.objects.filter(user_id=user_pk.id).last()
        if not public_image_user:
            return ""
        if not latitud:
            latitud = user.latitud
        if not longitud:
            longitud = user.longitud
        distance, str_distance = self.distances(float(latitud), float(longitud),
                                                float(user_pk.latitud), float(user_pk.longitud))
        return str_distance

    def like_user(self, id_user: int, datas: dict, ids: dict):
        like_user = accounts_models.LikeUser.objects.filter(id_user=id_user,
                                                            id_public_feed__in=ids.get('id_public_feed'))
        for list in like_user:
            for data in datas:
                if list.id_public_feed == data.get('id'):
                    data['band'] = str(list.like)
        return datas
