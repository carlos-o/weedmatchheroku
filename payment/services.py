from payment import models as payment_models
from accounts import models as accounts_models
from payment import validations as payment_validations
from datetime import datetime
import re


class CreditCardService:

    def list(self, user: accounts_models.User):
        if user is None or user.is_active is False:
            raise ValueError('{"detail": "para poder ver su informacion su cuenta debe estar activa"}')
        data = payment_models.CreditCard.objects.filter(user=user)
        if user.is_staff:
            data = payment_models.CreditCard.objects.all()
        return data

    def create(self, data: dict, user: accounts_models.User)-> payment_models.CreditCard:
        if user is None or user.is_active is False:
            raise ValueError('{"user": "para poder ver su informacion su cuenta debe estar activa"}')
        date = data['date_expiration'][:10]
        number_card = data.get('number_card')
        if not re.match(r'[0-9]+$', number_card) and number_card:
            raise ValueError('{"number_card":"el campo del numero de tarjeta de credito solo acepta numeros"}')
        if not date:
            raise ValueError('{"date_expiration": "El campo de fecha no puede estar vacio"}')
        match = re.match(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', date)
        if not match:
            raise ValueError('{"date_expiration": "No es una fecha valida"}')
        try:
            data['date_expiration'] = datetime.strptime(date, '%Y-%m-%d')
        except Exception as e:
            raise ValueError('{"date_expiration": "el día está fuera de rango por mes"}')
        user_id = data.get("user_id", None)
        if user_id is None:
            data["user_id"] = str(user.id)
        validator = payment_validations.CreditCardValidate(data)
        if validator.validate() is False:
            raise ValueError(validator.errors())
        if payment_models.CreditCard.objects.filter(number_card=data.get('number_card')).exists():
            raise ValueError('{"number_card": "Ya esta registrado en tu cuenta ese numero de tarjeta"}')
        card = payment_models.CreditCard()
        for key in data.keys():
            setattr(card, key, data[key])
        try:
            card.save(force_insert=True)
        except Exception as e:
            raise ValueError('{"user": "ha ocurrido un error al guardar la tarjeta de credito"}')
        return card

    def update(self, obj_card: payment_models.CreditCard, data: dict, user: accounts_models.User):
        if user is None or user.is_active is False:
            raise ValueError('{"user": "para poder ver su informacion su cuenta debe estar activa"}')
        date = data['date_expiration'][:10]
        if not date:
            raise ValueError('{"date_expiration": "El campo de fecha no puede estar vacio"}')
        match = re.match(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', date)
        if not match:
            raise ValueError('{"date_expiration": "No es una fecha valida"}')
        try:
            data['date_expiration'] = datetime.strptime(date, '%Y-%m-%d')
        except Exception as e:
            raise ValueError('{"date_expiration": "el día está fuera de rango por mes"}')
        validator = payment_validations.CreditCardValidate(data)
        if validator.validate() is False:
            raise ValueError(validator.errors())
        exists = payment_models.CreditCard.objects.filter(number_card=data.get('number_card')).exists()
        if obj_card.number_card == data.get('number_card') and exists:
            obj_card.number_card = data.get('number_card')
        elif not exists:
            obj_card.number_card = data.get('number_card')
        else:
            raise ValueError('{"number_card": "Ya esta registrado en tu cuenta ese numero de tarjeta"}')
        obj_card.first_name = data.get('first_name')
        obj_card.last_name = data.get('last_name')
        obj_card.type_card = data.get('type_card')
        obj_card.date_expiration = data.get('date_expiration')
        obj_card.save()
        return obj_card

    def delete(self, obj_card: payment_models.CreditCard, user: accounts_models.User) -> bool:
        if user is None or user.is_active is False:
            raise ValueError('{"user": "para poder ver su informacion su cuenta debe estar activa"}')
        obj_card.delete()
        return True