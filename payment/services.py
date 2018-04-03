from payment import models as payment_models
from accounts import models as accounts_models
from payment import validations as payment_validations
from datetime import datetime
import re
from django.utils.translation import ugettext_lazy as _


class CreditCardService:
    """

    """
    def list(self, user: accounts_models.User)-> payment_models.CreditCard:
        """
            Get a list when all credit card assigned to the user

            :param user: user weedmtach.
            :type user: Model User
            :return: Model CreditCard
            :raise: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"user":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        data = payment_models.CreditCard.objects.filter(user=user)
        if user.is_staff:
            data = payment_models.CreditCard.objects.all()
        return data

    def create(self, data: dict, user: accounts_models.User)-> payment_models.CreditCard:
        """
            This method receives the information from the credit card and stores it in the database; the method
            generates an exception if the credit card number exists in the database.

            :param data: user credit card information.
            :type data: dict.
            :param user: user weedmatch.
            :return: Model CreditCard.
            :raises: ValueError.
        """
        if user is None or user.is_active is False:
            raise ValueError('{"user":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        date = data['date_expiration'][:10]
        if not data.get('number_card'):
            raise ValueError('{"number_card":"' + str(_("The credit card field can not be empty")) + '"}')
        number_card = data.get('number_card')
        if not re.match(r'[0-9]+$', number_card) and number_card:
            raise ValueError('{"number_card":"' +
                             str(_("The field of the credit card number only accepts numbers"))+'"}')
        if not date:
            raise ValueError('{"date_expiration":"' + str(_("The date field can not be empty")) + '"}')
        match = re.match(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', date)
        if not match:
            raise ValueError('{"date_expiration":"' + str(_("The date you entered is not valid")) + '"}')
        try:
            data['date_expiration'] = datetime.strptime(date, '%Y-%m-%d')
        except Exception as e:
            raise ValueError('{"date_expiration":"' + str(_("The day is out of range per month")) + '"}')
        user_id = data.get("user_id", None)
        if user_id is None:
            data["user_id"] = str(user.id)
        validator = payment_validations.CreditCardValidate(data)
        if validator.validate() is False:
            errors = validator.errors()
            for value in errors:
                errors[value] = validator.change_value(errors[value])
            raise ValueError(errors)
        if payment_models.CreditCard.objects.filter(number_card=data.get('number_card')).exists():
            raise ValueError('{"number_card":"' + str(_("This card number is already registered in your account"))+'"}')
        card = payment_models.CreditCard()
        for key in data.keys():
            setattr(card, key, data[key])
        try:
            card.save(force_insert=True)
        except Exception as e:
            raise ValueError('{"user":"' + str(_("an error occurred while saving the credit card")) + '"}')
        return card

    def update(self, obj_card: payment_models.CreditCard, data: dict, user: accounts_models.User):
        """
            This method receives the information from the credit card and edits the field of the card
            chosen by the user. the method generates an exception if the credit card number exists in the database.

            :param obj_card: Credit card to edit.
            :type obj_card: Model CreditCard.
            :param data: credit card information.
            :type data: dict.
            :param user: user weedmatch.
            :type user: Model User.
            :return: Model CreditCard.
            :raises: ValueError.
        """
        if user is None or user.is_active is False:
            raise ValueError('{"user":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        date = data['date_expiration'][:10]
        if not data.get('number_card'):
            raise ValueError('{"number_card":"' + str(_("The credit card field can not be empty")) + '"}')
        if not date:
            raise ValueError('{"date_expiration":"' + str(_("The date field can not be empty")) + '"}')
        match = re.match(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', date)
        if not match:
            raise ValueError('{"date_expiration":"' + str(_("The date you entered is not valid")) + '"}')
        try:
            data['date_expiration'] = datetime.strptime(date, '%Y-%m-%d')
        except Exception as e:
            raise ValueError('{"date_expiration":"' + str(_("The date you entered is not valid")) + '"}')
        validator = payment_validations.CreditCardValidate(data)
        if validator.validate() is False:
            raise ValueError(validator.errors())
        exists = payment_models.CreditCard.objects.filter(number_card=data.get('number_card')).exists()
        if obj_card.number_card == data.get('number_card') and exists:
            obj_card.number_card = data.get('number_card')
        elif not exists:
            obj_card.number_card = data.get('number_card')
        else:
            raise ValueError('{"number_card":"' + str(_("This card number is already registered in your account"))+'"}')
        obj_card.first_name = data.get('first_name')
        obj_card.last_name = data.get('last_name')
        obj_card.type_card = data.get('type_card')
        obj_card.date_expiration = data.get('date_expiration')
        obj_card.save()
        return obj_card

    def delete(self, obj_card: payment_models.CreditCard, user: accounts_models.User) -> bool:
        """
            remove a credit card from the user's profile

            :param obj_card: credit card to delete.
            :type obj_card: Model CreditCard.
            :param user: user weedmatch.
            :type user: Model User.
            :return: True.
            :raise: ValueError.
        """
        if user is None or user.is_active is False:
            raise ValueError('{"user":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        obj_card.delete()
        return True