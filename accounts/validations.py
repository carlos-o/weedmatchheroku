from accounts import models as accounts_user
from cerberus import Validator


class RegisterUserValidate:
    '''
        validate class to register account
    '''

    schema = {
        'username': {'type': 'string', 'required': True, 'empty': False, 'minlength': 6, 'maxlength': 12},
        'first_name': {'type': 'string', 'required': True, 'empty': False, 'minlength': 3, 'maxlength': 30},
        'last_name': {'type': 'string', 'required': True, 'empty': False, 'minlength': 3, 'maxlength': 30},
        'email': {'type': 'string', 'required': True, 'empty': False},
        'password': {'type': 'string', 'required': True, 'empty': False, 'minlength': 6, 'maxlength': 20},
        'direction': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 255},
        'latitud': {'type': 'float', 'required': True, 'empty': False, 'min': -90, 'max': 90},
        'longitud': {'type': 'float', 'required': True, 'empty': False, 'min': -180, 'max': 180},
        'country': {'type': 'string', 'required': True, 'empty': False},
        'age': {'type': 'date', 'required': True, 'empty': False},
    }

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def errors(self):
        return self.validator.errors


class ProfileUserValidate:
    '''
        validate class to register account
    '''

    schema = {
        'username': {'type': 'string', 'required': True, 'empty': False, 'minlength': 6, 'maxlength': 12},
        'first_name': {'type': 'string', 'required': True, 'empty': False, 'minlength': 3, 'maxlength': 30},
        'last_name': {'type': 'string', 'required': True, 'empty': False, 'minlength': 3, 'maxlength': 30},
        'direction': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 255},
        'country': {'type': 'string', 'required': True, 'empty': False},
        'description': {'type': 'string', 'required': False, 'empty': True},
    }

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def errors(self):
        return self.validator.errors