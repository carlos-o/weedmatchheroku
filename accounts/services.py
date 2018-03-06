from accounts import models as accounts_models
from accounts import validations as accounts_validations
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from datetime import datetime
import re


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
    
    def changePassword(self, user: accounts_models.User, data: dict)-> accounts_models.User:
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
    
    def changeProfileImage(self, user: accounts_models.User, data: dict)-> accounts_models.User:
        if user is None or user.is_active is False:
            raise ValueError('{"user": "para poder ver su informacion su cuenta debe estar activa"}') 
        if not data.get('image'):
            raise ValueError('{"detail": "El campo imagen de perfil no puede estar vacio"}')
        user.image = data.get('image')
        user.save()
        return user


class RegisterUserService:

    def create(self, data: dict) -> accounts_models.User:
        date = data['age'][:10]
        if not date:
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

    def checkEmail(self, data: dict) -> accounts_models.User:
        if not data.get('email'):
            raise ValueError('{"detail": "el campo correo no puede estar vacio"}')
        try:
            user = accounts_models.User.objects.get(email=data.get('email'))
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail": "el correo no esta registrado en el sistema"}')
        return user

    def checkCode(self, data: dict) -> accounts_models.User:
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
