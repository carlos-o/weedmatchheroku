from accounts import models as accounts_models
from accounts import validations as accounts_validations
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg
from datetime import datetime
from weedmatch import settings
import re
import os


class UserService:

    def login(self, data: dict)->accounts_models.User:
        if not data.get('username'):
            raise ValueError('{"detail": "El nombre de usuario no puede estar vacio"}')
        if not data.get('password'):
            raise ValueError('{"detail": "La contraseña no puede estar vacia"}')
        try:
            user = accounts_models.User.objects.get(Q(username__iexact=data.get('username')) | Q(email__iexact=data.get('username')))
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail": "El usuario no existe en el sistema"}')
        if not user.is_active:
            raise ValueError('{"detail": "Cuenta inactiva, su cuenta esta bloqueada"}')
        if not user.check_password(data.get('password')):
            raise ValueError('{"detail": "Contraseña invalida, porfavor escriba correctamente su contraseña"}')
        return user

    def logut(self, user: accounts_models.User)-> accounts_models.User:
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
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.direction = data.get('direction')
        user.country_id = data.get('country')
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

    def assing_image_profile(self, user: accounts_models.User, id_image: int)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        try:
            image = accounts_models.ImageProfile.objects.get(id=id_image,user_id=user.id) 
        except accounts_models.ImageProfile.DoesNotExist:
            raise ValueError('{"detail": "no existe la imagen en tu profile"}')
        user.image = str(image.image_profile)
        user.save()
        return user

    def public_profile(self, user: accounts_models.User, pk: int)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        try:
            public = accounts_models.User.objects.get(id=pk)
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail": "el usuario no se encuentra registrado en el sistema"}')
        return public


class UploadImagePublicProfileService:

    def list(self, user: accounts_models.User)->accounts_models.Image:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        images = accounts_models.Image.objects.filter(user_id=user.id)
        return images

    def create(self, user:accounts_models.User, data:dict)->accounts_models.Image:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        if not data.get('image'):
            raise ValueError('{"detail": "El campo imagen de perfil no puede estar vacio"}')
        if not data.get('comment'):
            data['comment'] = ""
        try:
            image = accounts_models.Image.objects.create(
                user_id=user.id,
                image=data.get('image'),
                state=data.get('comment'),
                latitud=user.latitud,
                longitud=user.longitud
            )
        except Exception as e:
            raise ValueError('{"detail": "ha ocurrido un error al guardar el usuario"}')
        return image

    def update(self, user: accounts_models.User, data: dict, id_image: int)->accounts_models.Image:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        try:
            imagen = accounts_models.Image.objects.get(id=id_image, user_id=user.id)
        except accounts_models.Image.DoesNotExist:
            raise ValueError('{"detail": "La imagen no existe en tu perfil publico"}')
        if data.get('like') == "True" or data.get('like') == "true":
            imagen.increment_like()
        elif data.get('like') == "False" or data.get('like') == "false":
            imagen.decrement_like()
        else:
            raise ValueError('{"detail":"No se puede anexar un nuevo me gusta a su imagen publica"}')
        return imagen

    def delete(self, user:accounts_models.User, id_image: int)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver la información su cuenta debe estar activa"}')
        try:
            imagen = accounts_models.Image.objects.get(id=id_image, user_id=user.id)
        except accounts_models.Image.DoesNotExist:
            raise ValueError('{"detail": "La imagen no existe en tu perfil publico o la has eliminado"}')
        os.remove(os.path.join(settings.MEDIA_ROOT, str(imagen.image.name)))
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
        if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',data.get('email')):
            raise ValueError('{"email":"por favor escriba una direccion de correo valida"}')
        if accounts_models.User.objects.filter(email=data.get('email')).exists():
            raise ValueError('{"email":"El correo existe, porfavor escriba otro correo"}')
        if not accounts_models.Country.objects.filter(id=data.get('country')).exists():
            raise ValueError('{"country": "el pais no esta registrado en el sistema"}')
        user = accounts_models.User()
        country_id = data.get('country')
        data.pop('country')
        data["country_id"] = country_id
        for key in data.keys():
            if key == 'password':
                data[key] = make_password(data[key]) 
            setattr(user, key, data[key])
        try:
            user.save(force_insert=True)
        except Exception as e:
            raise ValueError('{"user": "ha ocurrido un error al guardar el usuario"}')
        return user


class RecoverPasswordService:

    def check_email(self, data: dict) -> accounts_models.User:
        if not data.get('email'):
            raise ValueError('{"detail": "el campo correo no puede estar vacio"}')
        try:
            user = accounts_models.User.objects.get(email=data.get('email'))
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail": "el correo no esta registrado en el sistema"}')
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
        user.password = make_password(str(data.get('password')))
        user.recovery = ''
        user.save()
        return user


class PublicFeedService:

    def list(self, user: accounts_models.User):
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver la información su cuenta debe estar activa"}')
        users = accounts_models.User.objects.all().exclude(username=user.username).exclude(is_superuser=True)
        ids = users.aggregate(users_id=ArrayAgg('id'))
        images = accounts_models.Image.objects.filter(user_id__in=ids.get('users_id'))
        print(images)
        return images