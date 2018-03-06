import serpy
from weedmatch import settings
from payment import serializers as payment_serializers
from payment import models as payment_models
import datetime


class CountrySerializers(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field()
    code = serpy. Field()


class ProfileUserSerializers(serpy.Serializer):
    id = serpy.Field()
    username = serpy.Field() 
    first_name = serpy.Field()
    last_name = serpy.Field()
    email = serpy.Field()
    direction = serpy.Field()
    description = serpy.Field()
    country = serpy.MethodField()
    image = serpy.MethodField()
    credit_card = serpy.MethodField()
    age = serpy.MethodField()

    def get_country(self, obj):
        if obj.country == None:
            return ""
        return CountrySerializers(obj.country).data 

    def get_image(sefl, obj):
        if not obj.image:
            return(str(obj.image))
        return(settings.URL+settings.MEDIA_URL+str(obj.image))

    def get_credit_card(self, obj):
        card = payment_models.CreditCard.objects.filter(user=obj.id)
        if not card:
            return []
        serializer = payment_serializers.CreditCardSerializers(card, many=True).data
        return serializer

    def get_age(self, obj):
        if not obj.age:
            return ""
        delta = datetime.date.today() - obj.age
        return datetime.date.fromordinal(delta.days).year
