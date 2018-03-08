from cerberus import Validator
from payment.models import CreditCard


class CreditCardValidate:
    '''
        validate credit card
    '''
    schema = {
        'user_id': {'type': 'string', 'empty': False},
        'first_name': {'type': 'string', 'required': True, 'empty': False, 'minlength': 3, 'maxlength': 50},
        'last_name': {'type': 'string', 'required': True, 'empty': False, 'minlength': 3, 'maxlength': 50},
        'type_card': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 20,
                      'allowed': [i[0] for i in CreditCard().TYPE_CARD]},
        'number_card': {'type': 'string', 'required': True, 'empty': False,
                        'minlength': 15, 'maxlength': 20},
        'cod_security': {'type': 'string', 'required': False, 'empty': True, 'regex': '^[0-9]+$',
                         'minlength': 3, 'maxlength': 4},
        'date_expiration': {'type': 'date', 'required': True, 'empty': False},
    }

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def errors(self):
        return self.validator.errors