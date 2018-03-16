import serpy
from weedmatch import settings
from payment import serializers as payment_serializers
from payment import models as payment_models
from accounts import models as accouns_models
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
    id = serpy.Field()
    username = serpy.Field() 
    first_name = serpy.Field()
    email = serpy.Field()
    direction = serpy.Field()
    description = serpy.MethodField()
    image = serpy.MethodField()
    profile_images = serpy.MethodField()
    images_upload = serpy.MethodField()
    country = serpy.MethodField()
    credit_card = serpy.MethodField()
    age = serpy.MethodField()
    sex = serpy.Field()
    match_sex = serpy.Field()

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

    def get_images_upload(self, obj):
        images = accouns_models.Image.objects.filter(user_id=obj.id).order_by('-id')[:20]
        if not images:
            return []
        serializer = ImagePublicSerializer(images, many=True).data
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
        result = settings.RADIO_EARTH * arccos
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
        return self.distances(obj.latitud, obj.longitud, images.latitud, images.longitud)

    def get_instagram_images(self, obj):
        return ""


class PublicFeedSerializers(serpy.Serializer):
    id = serpy.Field()
    id_user = serpy.MethodField()
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

    def time_format(self,date_now, date_result):
        date_string = str(date_result).split(".")[0]
        if len(date_string) == 7:
            if int(date_string[0:1]) >= 1 and int(date_string[0:1]) < 10:
                return date_string[0:1]+" hours"
            if date_string[2:4] == "00":
                if int(date_string[5:6]) == 0:
                    return date_string[6:7]+ " seconds"
                else:
                    return date_string[5:7]+ " seconds"
            if int(date_string[2:3]) == 0:
                print(date_string[3:4])
                return date_string[3:4] + " minutes"
            else:
                print(date_string[2:4])
                return date_string[2:4] + " minutes"	
        elif len(date_string) == 8:
            return date_string[0:2] + " hours"
        elif len(date_string) >= 14:
            return date_string[:-13] + " days"
            if int(date_string[:-13]) > 7:
                date = date_now - datetime.timedelta(days=int(date_string[:-13]))
            if int(date_now.strftime("%Y")) > int(date.strftime("%Y")):
                return date.strftime("%d the %B the %Y")
            else:
                #print(month[date.strftime("%B")])
                return date.strftime("%d the %B")
    
    def get_time(self, obj):
        if not obj.date_creation:
            return ""
        date_now = datetime.datetime.now()
        local_time = timezone.localtime(obj.date_creation, pytz.timezone('America/Santiago'))
        date_after = local_time.replace(tzinfo=None)
        date_result = date_now - date_after
        print(date_result)
        return self.time_format(date_now, date_result)

    def get_image(self, obj):
        if not obj.image:
            return ""
        return settings.URL + settings.MEDIA_URL + str(obj.image)