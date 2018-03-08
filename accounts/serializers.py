import serpy
from weedmatch import settings
from payment import serializers as payment_serializers
from payment import models as payment_models
from accounts import models as accouns_models
import datetime
import math
RADIO = 6372.795477598


class CountrySerializers(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field()
    code = serpy. Field()


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
    id = serpy.Field()
    username = serpy.Field() 
    first_name = serpy.Field()
    last_name = serpy.Field()
    email = serpy.Field()
    direction = serpy.Field()
    description = serpy.MethodField()
    image = serpy.MethodField()
    profile_images = serpy.MethodField()
    country = serpy.MethodField()
    credit_card = serpy.MethodField()
    age = serpy.MethodField()

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
    username = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    description = serpy.Field()
    country = serpy.MethodField()
    image = serpy.MethodField()
    profile_images = serpy.MethodField()
    age = serpy.MethodField()
    images_upload = serpy.MethodField()
    instagram_images = serpy.MethodField()
    distance = serpy.MethodField()

    def get_image(self, obj):
        if not obj.image:
            return ""
        return settings.URL+'/media/'+obj.image

    def get_country(self, obj):
        if not obj.country:
            return ""
        return CountrySerializers(obj.country).data

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

    def get_images_upload(self, obj):
        images = accouns_models.Image.objects.filter(user_id=obj.id).order_by('-id')[:20]
        if not images:
            return []
        serializer = ImagePublicSerializer(images, many=True).data
        return serializer

    def distances(self, latA: float, lonA: float, latB: float, lonB: float):
        arccos = math.acos(
            ((math.sin(latA) * math.sin(latB)) + (math.cos(latA) * math.cos(latB))) * math.cos(lonA - lonB))
        result = RADIO * arccos
        degrees = (math.pi * result) / 180
        if degrees < 0.9:
            meters = degrees * 1000
            return str(meters)[:3]+" mts"
        if degrees > 1:
            convert = str(degrees)
            value = convert.find(".")
            number = convert[value + 1:value + 2]
            if int(number) >= 5:
                return str(math.ceil(degrees))[:3]+" km"
            else:
                return str(degrees)[0:1]+" km"
        return ""

    def get_distance(self, obj):
        images = accouns_models.Image.objects.filter(user_id=obj.id).last()
        if not images:
            return ""
        return self.distances(obj.latitud, obj.longitud,images.latitud, images.longitud)

    def get_instagram_images(self, obj):
        return ""


class PublicFeedSerializers(serpy.Serializer):
    id = serpy.Field()
    username = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    distance = serpy.MethodField()
    image = serpy.MethodField()
    time = serpy.MethodField

    def get_time(self, obj):
        profile_image = accouns_models.ImageProfile.objects.filter(user_id=obj.id).last()
        if not profile_image:
            return ""

    def get_image(self, obj):
        profile_image = accouns_models.ImageProfile.objects.filter(user_id=obj.id).last()
        if not profile_image:
            return ""
        serializer = ImageSerializer(profile_image, many=True).data
        return serializer

    def distances(self, latA: float, lonA: float, latB: float, lonB: float):
        arccos = math.acos(
            ((math.sin(latA) * math.sin(latB)) + (math.cos(latA) * math.cos(latB))) * math.cos(lonA - lonB))
        result = RADIO * arccos
        degrees = (math.pi * result) / 180
        if degrees < 0.9:
            meters = degrees * 1000
            return str(meters)[:3]+" mts"
        if degrees > 1:
            convert = str(degrees)
            value = convert.find(".")
            number = convert[value + 1:value + 2]
            if int(number) >= 5:
                return str(math.ceil(degrees))[:3]+" km"
            else:
                return str(degrees)[0:1]+" km"
        return ""

    def get_distance(self, obj):
        images = accouns_models.Image.objects.filter(user_id=obj.id).last()
        if not images:
            return ""
        return self.distances(obj.latitud, obj.longitud,images.latitud, images.longitud)