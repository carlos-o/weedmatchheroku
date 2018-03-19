import serpy
from weedmatch import settings
from payment import serializers as payment_serializers
from payment import models as payment_models
from accounts import models as accouns_models
from accounts import services as accounts_services
from django.utils import timezone
import pytz
import datetime
import math


class CountrySerializers(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field()
    code = serpy. Field()

class TermsConditionsSerializers(serpy.Serializer):
    id = serpy.Field()
    title = serpy.Field()
    description = serpy. Field()


class ImagePublicSerializer(serpy.Serializer):
    id = serpy.Field()
    like = serpy.Field()
    image = serpy.MethodField()
    comment = serpy.MethodField()

    def get_image(self, obj):
        if not obj.image:
            return str(obj.image)
        return settings.URL+settings.MEDIA_URL+str(obj.image)

    def get_comment(self, obj):
        if not obj.state:
            return ""
        return obj.state


class ImageSerializer(serpy.Serializer):
    id = serpy.Field()
    image = serpy.MethodField()

    def get_image(self, obj):
        if not obj.image_profile:
            return str(obj.image_profile)
        return settings.URL+settings.MEDIA_URL+str(obj.image_profile)


class ProfileUserSerializers(serpy.Serializer):
    id_user = serpy.MethodField()
    username = serpy.Field() 
    first_name = serpy.Field()
    email = serpy.Field()
    direction = serpy.Field()
    description = serpy.MethodField()
    image = serpy.MethodField()
    profile_images = serpy.MethodField()
    country = serpy.MethodField()
    credit_card = serpy.MethodField()
    age = serpy.MethodField()
    sex = serpy.Field()
    match_sex = serpy.Field()

    def get_id_user(self, obj):
        return obj.id

    def get_country(self, obj):
        if not obj.country:
            return ""
        return CountrySerializers(obj.country).data 

    def get_image(self, obj):
        if not obj.image:
            return ""
        return settings.URL+'/media/'+obj.image
    
    def get_description(self, obj):
        if not obj.description:
            return ""
        return obj.description

    def get_profile_images(self, obj):
        profile_image = accouns_models.ImageProfile.objects.filter(user_id=obj.id)
        if not profile_image:
            return []
        serializer = ImageSerializer(profile_image, many=True).data
        return serializer

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


class PublicProfileUserSerializers(serpy.Serializer):
    id_user = serpy.MethodField() 
    username = serpy.Field()
    first_name = serpy.Field()
    description = serpy.MethodField()
    country = serpy.MethodField()
    image = serpy.MethodField()
    profile_images = serpy.MethodField()
    age = serpy.MethodField()

    def get_id_user(self, obj):
        return obj.id

    def get_image(self, obj):
        if not obj.image:
            return ""
        return settings.URL+'/media/'+obj.image

    def get_country(self, obj):
        if not obj.country:
            return ""
        return CountrySerializers(obj.country).data

    def get_description(self, obj):
        if not obj.description:
            return ""
        return obj.description

    def get_profile_images(self, obj):
        profile_image = accouns_models.ImageProfile.objects.filter(user_id=obj.id)
        if not profile_image:
            return []
        serializer = ImageSerializer(profile_image, many=True).data
        return serializer

    def get_age(self, obj):
        if not obj.age:
            return ""
        delta = datetime.date.today() - obj.age
        return datetime.date.fromordinal(delta.days).year


class PublicFeedSerializers(serpy.Serializer):
    id_user = serpy.MethodField()
    id_image = serpy.Field()
    username = serpy.MethodField()
    first_name = serpy.MethodField()
    image = serpy.MethodField()
    time = serpy.MethodField()
    latitud = serpy.Field()
    longitud = serpy.Field()

    def get_id_user(self, obj):
        if not obj.user:
            return ""
        return obj.get_user_id()

    def get_username(self, obj):
        if not obj.user:
            return ""
        return obj.get_user_username()

    def get_first_name(self, obj):
        if not obj.user:
            return ""
        return obj.get_user_first_name()

    def get_time(self, obj):
        if not obj.date_creation:
            return ""
        date_now = datetime.datetime.now()
        local_time = timezone.localtime(obj.date_creation, pytz.timezone('America/Santiago'))
        date_after = local_time.replace(tzinfo=None)
        date_result = date_now - date_after
        services = accounts_services.PublicFeedService()
        print(date_result)
        return services.time_format(date_now, date_result)

    def get_image(self, obj):
        if not obj.image:
            return ""
        return settings.URL + settings.MEDIA_URL + str(obj.image)