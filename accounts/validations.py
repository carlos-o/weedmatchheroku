from accounts import models as accounts_models
from cerberus import Validator
from django.utils.translation import ugettext_lazy as _


class RegisterUserValidate:
    '''
        validate class to register account
    '''

    schema = {
        'username': {'type': 'string', 'required': True, 'empty': False, 'minlength': 6, 'maxlength': 12},
        'first_name': {'type': 'string', 'required': True, 'empty': False, 'minlength': 3, 'maxlength': 30},
        'last_name': {'type': 'string', 'required': False, 'empty': True, 'minlength': 3, 'maxlength': 30},
        'email': {'type': 'string', 'required': True, 'empty': False},
        'password': {'type': 'string', 'required': True, 'empty': False, 'minlength': 6, 'maxlength': 20},
        'direction': {'type': 'string', 'required': False, 'empty': True, 'maxlength': 255},
        'latitud': {'type': 'string', 'required': True, 'empty': False},
        'longitud': {'type': 'string', 'required': True, 'empty': False},
        'country': {'type': 'string', 'required': False, 'empty': True},
        'age': {'type': 'date', 'required': True, 'empty': False},
        'sex': {'type': 'string', 'required': True, 'empty': False, 
                'allowed': [i[0] for i in accounts_models.User.TYPE_SEX]},
    }

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def change_value(self, data: list)-> list:
        for i in range(0, len(data)):
            if data[i][0:15] == "unallowed value":
                convert = str(data[i])
                data[i] = str(_(convert[0:15])) + convert[16:]
            else:
                convert = str(data[i])
                data[i] = str(_(convert))
        return data

    def errors(self):
        return self.validator.errors


class ProfileUserValidate:
    '''
        validate class to register account
    '''

    schema = {
        'username': {'type': 'string', 'required': False, 'empty': True, 'minlength': 6, 'maxlength': 12},
        'first_name': {'type': 'string', 'required': True, 'empty': False, 'minlength': 3, 'maxlength': 30},
        'last_name': {'type': 'string', 'required': False, 'empty': True, 'minlength': 3, 'maxlength': 30},
        'direction': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 255},
        'country': {'type': 'string', 'required': True, 'empty': False},
        'description': {'type': 'string', 'required': False, 'empty': True},
        'sex': {'type': 'string', 'required': True, 'empty': False},
        "match_sex": {'type': 'string', 'required': True, 'empty': False,
                      'allowed': [i[0] for i in accounts_models.User.TYPE_SEX]},
    }

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def change_value(self, data: list)-> list:
        for i in range(0, len(data)):
            if data[i][0:15] == "unallowed value":
                convert = str(data[i])
                data[i] = str(_(convert[0:15])) + convert[16:]
            else:
                convert = str(data[i])
                data[i] = str(_(convert))
        return data

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def errors(self):
        return self.validator.errors


class ProfileUserDistance:
    '''
        validate class to register account
    '''

    schema = {
        'distance': {'type': 'integer', 'required': True, 'empty': False, 'min': 2, 'max': 200},
    }

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def change_value(self, data: list)-> list:
        for i in range(0, len(data)):
            convert = str(data[i])
            data[i] = str(_(convert))
        return data

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def errors(self):
        return self.validator.errors