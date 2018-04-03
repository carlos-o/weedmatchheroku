from cerberus import Validator
from payment.models import CreditCard
from django.utils.translation import ugettext_lazy as _


class CreditCardValidate:
    """
        validate all information credit card
    """
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
        """
            initialize cerberus with the credit card information

            :param data: credit card information.
            :type data: dict.
        """
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def validate(self):
        """
            :return: none if data is correct
        """
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
        """
            This method returns the error when, the information sent by the user does not comply
            with the rules in the validation with cerberus

            :return: error of cerberus
        """
        return self.validator.errors