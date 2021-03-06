from accounts import models as accounts_models
from accounts import validations as accounts_validations
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg
from datetime import datetime
from weedmatch import settings
import googlemaps
import re
import os
import math
import requests
import json
import datetime as datetime_module
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class UserService:
    """
        this class controls the login of the user by the different routes in a traditional way,
        via facebook and instagram, in addition to the closing of the session
    """
    def login(self, data: dict)->accounts_models.User:
        """
            A user registered in the system obtain access to weedmatch
            this function fails if the user's credentials do not match
            those registered in the system

            :param data: user information.
            :type data: dict.
            :return: Model User
            :raises: ValueError
        """
        if not data.get('username'):
            raise ValueError('{"detail":"'+str(_("The username can not be empty"))+'"}')
        if not data.get('password'):
            raise ValueError('{"detail": "'+str(_("The password can not be empty"))+'"}')
        try:
            user = accounts_models.User.objects.get(Q(username__iexact=data.get('username')) |
                                                    Q(email__iexact=data.get('username')))
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail":"' + str(_("The user does not exist in the system")) + '"}')
        if not user.is_active:
            raise ValueError('{"detail":"' + str(_("Account inactive, or your account is blocked")) + '"}')
        if not user.check_password(data.get('password')):
            raise ValueError('{"detail":"' + str(_("Password is invalid, please enter your password correctly")) + '"}')
        return user

    def login_facebook(self, data: dict)->accounts_models.User:
        """
            A user gets access to weedmatch with their Facebook credentials
            this function fails if the user's Facebook token does not match
            when the request is made to the api the Facebook

            :param data: access_token of facebook, latitude and longitude.
            :type data: dict.
            :return: Model User
            :raises: ValueError
        """
        if not data.get('access_token'):
            raise ValueError('{"detail":"' + str(_("The access_token field can not be empty")) + '"}')
        if not data.get('latitud'):
            raise ValueError('{"detail":"' + str(_("The latitude field can not be empty")) + '"}')
        if not data.get('longitud'):
            raise ValueError('{"detail":"' + str(_("The field length can not be empty")) + '"}')

        # Requests to Facebook API
        get_code_url = 'https://graph.facebook.com/oauth/client_code'
        access_token_url = 'https://graph.facebook.com/v2.9/oauth/access_token'
        graph_api_url = 'https://graph.facebook.com/v2.12/me?fields=id,name,email,birthday,picture.width(200).height(200)'
        params = {
            'client_id': settings.FACEBOOK_CLIEND_ID,
            'redirect_uri': "192.168.0.21",
            'client_secret': settings.FACEBOOK_SECRET,
            'access_token': data.get('access_token')
        }
        r = requests.get(graph_api_url, params=params)
        if r.status_code == 400:
            raise ValueError('{"detail":"' + str(_("The access token does not belong to that user")) + '"}')
        # Data obtained by calling Facebook API with user token
        profile = json.loads(r.text)
        username = profile.get('email').split("@")[0]
        user_register = accounts_models.User.objects.filter(facebook_id=profile.get('id'))
        if user_register.exists():
            return user_register[0]
        if accounts_models.User.objects.filter(username=username).exists():
            raise ValueError('{"detail":"' + str(_("The username exists, please enter another username")) + '"}')

        # Requests to GoogleMap Api
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)
        try:
            reverse_geocode_result = gmaps.reverse_geocode((float(data.get('latitud')), float(data.get('longitud'))))
        except googlemaps.exceptions.ApiError:
            raise ValueError('{"detail":"' + str(_("The key that was used does not work")) + '"}')
        direction = reverse_geocode_result[1].get('formatted_address')
        count = len(reverse_geocode_result) - 1
        country_map = reverse_geocode_result[count].get('formatted_address')
        try:
            country = accounts_models.Country.objects.filter(name=country_map)
        except accounts_models.Country.DoesNotExist:
            raise ValueError('{"detail":"' + str(_("the country is not registered in the system")) + '"}')
        image = profile.get('picture').get('data').get('url')
        age = profile.get('birthday')
        if not age:
            age = datetime.now().strftime('%Y-%m-%d')
        else:
            age = datetime.strptime(age, "%m/%d/%Y").strftime("%Y-%m-%d")
        if not image:
            image = ""
        user = accounts_models.User.objects.create(
            username=username,
            first_name=profile.get('name'),
            email=profile.get('email'),
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            country_id=country[0].id,
            image=image,
            age=age,
            direction=direction,
            sex=accounts_models.User.SEX_OTHER,
            facebook_id=profile.get('id'),
            facebook_access_token=data.get('access_token')
        )
        print(user)
        group = Group.objects.get(name='WeedMatch')
        user.groups.add(group)
        return user

    def login_instagram(self, data: dict)->accounts_models.User:
        """
            A user gets access to weedmatch with their instagram credentials

            :param data: access_token of instagram, latitude and longitude.
            :type data: dict.
            :return: Model User
            :raises: ValueError
        """
        return True

    def image_user(self, user: accounts_models.User):
        """
            Return the image profile of user

            :param user: user weedmatch.
            :type user: Model User.
            :return: user.image or "" or user.image with path
            :raise: None
        """
        if not user.image:
            return ""
        if re.search("https", user.image):
            return user.image
        return settings.URL + settings.MEDIA_URL + str(user.image)

    def logut(self, user: accounts_models.User)-> accounts_models.User:
        """
            The user disconnects from the system weedmatch

            :param user: user weedmatch.
            :type user: Model User.
            :return: ModelUser
            :raise: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        user.last_login = datetime.now()
        user.save()
        user.auth_token.delete()
        return user


class ProfileUser:
    """
        This class service contain method related with the user profile
    """
    def list(self, user: accounts_models.User)-> accounts_models.User:
        """
            This method get the user information call in database

            :param user: user weedmatch.
            :type user: Model User.
            :return: Model User.
            :raises: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        user_data = accounts_models.User.objects.filter(id=user.id)
        if user.is_staff:
            user_data = accounts_models.User.objects.all()
        return user_data
    
    def update(self, user: accounts_models.User, data: dict)-> accounts_models.User:
        """
            With this method we can update the user information, you can only update the username,
            username, description, address, country, city and match_sex that depending on the user's
            trend the profiles will be filtered in all the functions of the weedmatch.
            this function raises an exception if the user changes his username for another one that is in use

            :param user: user weedmatch.
            :type user: Model User.
            :param data: user data.
            :type data: dict.
            :return: Model User.
            :raises: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        validator = accounts_validations.ProfileUserValidate(data)
        if validator.validate() is False:
            errors = validator.errors()
            for value in errors:
                errors[value] = validator.change_value(errors[value])
            raise ValueError(errors)
        exists = accounts_models.User.objects.filter(username=data.get('username')).exists()
        if user.username == data.get('username') and exists:
            user.username = data.get('username')
        elif not exists:
            user.username = data.get('username')
        else:
            raise ValueError('{"username":"' + str(_("The username exists, please enter another username")) + '"}')
        if not accounts_models.Country.objects.filter(id=data.get('country')).exists():
            raise ValueError('{"country":"' + str(_("The country is not registered in the system")) + '"}')
        if data.get('description'):
            user.description = data.get('description')
        if not data.get('last_name'):
            data['last_name'] = ""
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.direction = data.get('direction')
        user.country_id = data.get('country')
        user.match_sex = data.get('match_sex')
        user.save()
        return user
    
    def change_password(self, user: accounts_models.User, data: dict)-> accounts_models.User:
        """
            change the password user, this method receives the user's previous password and the new password.
            this function generates an exception when the user's previous password does not match the current
            one or the new password it does not have characters and numbers

            :param user: user weedmatch.
            :type user: Model User.
            :param data: user data.
            :type data: dict.
            :return: Model User
            :raises: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        if not data.get('old_password'):
            raise ValueError('{"detail":"' + str(_("The old password field can not be empty")) + '"}')
        if not data.get('new_password'):
            raise ValueError('{"detail":"' + str(_("The new password field can not be empty")) + '"}')
        if not user.check_password(data.get('old_password')):
            raise ValueError('{"detail":"' + str(_("The password entered does not match your current password")) + '"}')
        if not re.match(r'(?=.*[A-Za-z]+)(?=.*\d+)', data.get('new_password')):
            raise ValueError('{"detail":"' + str(_("The password must have characters and numbers")) + '"}')
        user.password = make_password(data.get('new_password')) 
        user.save()
        return user
    
    def upload_images(self, user: accounts_models.User, data: dict)-> accounts_models.User:
        """
            the user can upload images for his profile, if he has not assigned a still the first image
            to upload he will be placed in profile, this method raises exception if the user try
            upload a seventh image

            :param user: user weedmatch.
            :type user: Model User.
            :param data: user data.
            :type data: dict
            :return: Model User
            :raises: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        if not data.get('image'):
            raise ValueError('{"detail":"' + str(_("The profile image field can not be empty")) + '"}')
        if user.count_image < 6:        
            images_profile = accounts_models.ImageProfile.objects.create(
                user_id=user.id,
                image_profile=data.get('image')
            )
            if not user.image:
                user.assign_image_profile(str(images_profile.image_profile))
            user.count_increment()
        else:
            raise ValueError('{"detail":"' +
                             str(_("You can not upload more than 6 images in your profile, you must delete some"))+'"}')
        return user
    
    def delete_images(self, user: accounts_models.User, id_image: int)-> accounts_models.User:
        """
            Delete one image assigned to profile user, this method raises a exception if the id of image
            not exits in database

            :param user: user weedmatch.
            :type user: Model User
            :param id_image: id of image profile.
            :type id_image: integer
            :return: Model User
            :raises: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        try:
            image = accounts_models.ImageProfile.objects.get(id=id_image, user_id=user.id)
        except accounts_models.ImageProfile.DoesNotExist:
            raise ValueError('{"detail":"' + str(_("There is no such image on your profile")) + '"}')
        if user.image == str(image.image_profile):
            user.image = ""
            user.save()
        os.remove(os.path.join(settings.MEDIA_ROOT, str(image.image_profile.name)))
        image.delete()
        user.count_delete()
        return user

    def list_image_profile(self, user: accounts_models.User,)-> accounts_models.ImageProfile:
        """
            Get all images assigned to the profile user

            :param user: user weedmatch.
            :type user: Model User.
            :return: Model ImageProfile
            :raise: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        images_profile = accounts_models.ImageProfile.objects.filter(user_id=user.id)
        return images_profile

    def assing_image_profile(self, user: accounts_models.User, id_image: int)-> accounts_models.User:
        """
            Assigned a image for profile user, this image can see for all user in weedmtach, this method
            raise a exception if id of image not exist in database

            :param user: user weedmtach
            :type user: Model User
            :param id_image: id of image profile
            :type id_image: integer
            :return: Model User
            :raise: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        try:
            image = accounts_models.ImageProfile.objects.get(id=id_image, user_id=user.id)
        except accounts_models.ImageProfile.DoesNotExist:
            raise ValueError('{"detail":"' + str(_("There is no such image on your profile")) + '"}')
        user.assign_image_profile(str(image.image_profile))
        return user

    def update_distance(self, user: accounts_models.User, data: dict)-> accounts_models.User:
        """
            A user can change the distance in which people appear in the public feed 420.
            this method raise a exception when the distance they are not numbers or exceed the limits.

            :param user: user weedmatch.
            :type user: Model User.
            :param data: distance
            :type data: ditc
            :return: Model User.
            :raises: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"user":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        if not data.get('distance'):
            raise ValueError('{"detail":"' + str(_("The distance field can not be empty")) + '"}')
        if not re.match("[0-9]+", data.get("distance")):
            raise ValueError('{"detail":"' + str(_("The distance value can only be numbers")) + '"}')
        data["distance"] = int(data.get("distance"))
        validator = accounts_validations.ProfileUserDistance(data)
        if validator.validate() is False:
            errors = validator.errors()
            for value in errors:
                errors[value] = validator.change_value(errors[value])
            raise ValueError(errors)
        user.distance = data.get('distance')
        user.save()
        return user


class UploadImagePublicProfileService:
    """
        this class contain a crud for the image upload to public feed 420
    """
    def list(self, user: accounts_models.User)->accounts_models.PublicFeed:
        """
            Get all images upload to public feed 420. if user is admin o staff the can see all
            images upload for any user in weedmtach.

            :param user: user weedmatch
            :type user: Model User
            :return: Model PublicFeed
            :raise: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        if user.is_staff:
            images = accounts_models.PublicFeed.objects.all()
        else:
            images = accounts_models.PublicFeed.objects.filter(user_id=user.id)
        return images

    def retrieve(self, user: accounts_models.User, pk: int)->accounts_models.PublicFeed:
        """
            Get all image for one user in public feed 420. this service is called when another user views the
            public profile and wants to see the images that he has uploaded to the public feed 420

            :param user: user weematch
            :param pk: id another user
            :type pk: integer
            :return: Model PublicFeed
            :raise: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        images = accounts_models.PublicFeed.objects.filter(user_id=pk)
        return images

    def create(self, user: accounts_models.User, data: dict)->accounts_models.Image:
        """
            A user cant upload a image to public feed 420, if the user does not activate the gps when uploading
            the image it will take the latitude and longitude registered in the user

            :param user: user weedmatch
            :param data: image, comment, latitud and longitud
            :type data: dict
            :return: Model Image
            :raises: ValueError
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        if not data.get('image'):
            raise ValueError('{"detail":"' + str(_("The public feed image field can not be empty")) + '"}')
        if not data.get('comment'):
            data['comment'] = ""
        if not data.get('latitud'):
            data['latitud'] = user.latitud
        if not data.get('longitud'):
            data['longitud'] = user.longitud
        try:
            public_image = accounts_models.Image.objects.create(
                user_id=user.id,
                image=data.get('image'),
                state=data.get('comment'),
                latitud=data.get('latitud'),
                longitud=data.get('longitud')
            )
            public_feed = accounts_models.PublicFeed.objects.create(
                user_id=user.id,
                id_image=public_image.id,
                image=str(public_image.image),
                state=public_image.state,
                latitud=data.get('latitud'),
                longitud=data.get('longitud'),
                date_creation=public_image.created
            )
        except Exception as e:
            raise ValueError('{"detail":"' + str(_("An error occurred while saving the image")) + '"}')
        return public_image

    def update(self, user: accounts_models.User, data: dict, id_image: int, id_user: int)->accounts_models.PublicFeed:
        """
            Assigned a weed-like or weed-deslike for one image in public feed 420, in this service a
            logged in user who has viewed the photo of another can like or take away that I like that user

            :param user: user weedmatch
            :param data: like (true or false)
            :param id_image: id of image public feed
            :param id_user: id of another user
            :return:
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        try:
            imagen = accounts_models.PublicFeed.objects.get(id_image=id_image, user_id=id_user)
        except accounts_models.Image.DoesNotExist:
            raise ValueError('{"detail":"' + str(_("The image does not exist, you can not add a weed-like")) + '"}')
        if not data.get('like'):
            raise ValueError('{"detail":"' + str(_("The like field can not be empty")) + '"}')
        if data.get('like') == "True" or data.get('like') == "true":
            imagen.increment_like()
            try:
                like_user = accounts_models.LikeUser.objects.get(id_user=user.id, id_public_feed=imagen.id)
                like_user.change_like(True)
            except accounts_models.LikeUser.DoesNotExist:
                like_create = accounts_models.LikeUser.objects.create(
                    id_user=user.id,
                    id_public_feed=imagen.id,
                    like=True
                )
        elif data.get('like') == "False" or data.get('like') == "false":
            imagen.decrement_like()
            like_user = accounts_models.LikeUser.objects.get(id_user=user.id, id_public_feed=imagen.id)
            like_user.change_like(False)
        if not re.search(r'^(true|True|false|False)$', data.get('like')):
            raise ValueError('{"detail":"' + str(_("Can not attach a weed-like to the image")) + '"}')
        return imagen

    def delete(self, user: accounts_models.User, id_image: int)-> bool:
        """
            A user cant delete one image upload in public feed 420, this method raise a exception if the
            image does not exist in the accounts of user.

            :param user: user weematch
            :param id_image: id of public image
            :type user: integer
            :return: True
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        try:
            imagen = accounts_models.Image.objects.get(id=id_image, user_id=user.id)
        except accounts_models.Image.DoesNotExist:
            raise ValueError('{"detail":"' +
                             str(_("The image does not exist in your public feed or you have already deleted it"))+'"}')
        #os.remove(os.path.join(settings.MEDIA_ROOT, str(imagen.image.name)))
        imagen.delete()
        return True


class RegisterUserService:
    """
        this class contain a method to register user in weedmatch
    """
    def create(self, data: dict) -> accounts_models.User:
        """
            register a user in the system weedmtach, this method validate all information and if everything
            is correct register the user, this method raises a exception when the username exist, as well as
            the mail exist.

            :param data: contain all information to register a user in weedmatch
            first_name, username, email, password, latitud, longitud, age, sex
            :type data: dict
            :return: Model User.
            :raises: ValueError
        """
        print(data)
        #validation of the date birth date
        date = data['age'][:10]
        if not date and not data.get('age'):
            raise ValueError('{"age":"' + str(_("The date field can not be empty")) + '"}')
        match = re.match(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', date)
        if not match:
            raise ValueError('{"age":"' + str(_("The date you entered is not valid")) + '"}')
        try:
            data['age'] = datetime.strptime(date, '%Y-%m-%d')
        except Exception as e:
            raise ValueError('{"age":"' + str(_("The day is out of range per month")) + '"}')
        validator = accounts_validations.RegisterUserValidate(data)
        if validator.validate() is False:
            errors = validator.errors()
            for value in errors:
                errors[value] = validator.change_value(errors[value])
            raise ValueError(errors)
        #validation for the username
        if accounts_models.User.objects.filter(username=data.get('username')).exists():
            raise ValueError('{"username":"' + str(_("The username exists, please enter another username")) + '"}')
        #validation for the email
        if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', data.get('email')):
            raise ValueError('{"email":"' + str(_("Please enter a valid email address")) + '"}')
        if accounts_models.User.objects.filter(email=data.get('email')).exists():
            raise ValueError('{"email":"' + str(_("Mail exists, please enter another email")) + '"}')
        """
        necesito para la api en produccion el googlemaps api key del cliente
        """
        # Requests to GoogleMap Api
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)
        try:
            reverse_geocode_result = gmaps.reverse_geocode((float(data.get('latitud')), float(data.get('longitud'))))
        except googlemaps.exceptions.ApiError:
            raise ValueError('{"googlemaps": "'+str(_("The key that was used does not work"))+'"}')
        if len(reverse_geocode_result) == 1:
            direction = reverse_geocode_result[0].get('formatted_address')
            for lists in reverse_geocode_result[0].get('address_components'):
                country = accounts_models.Country.objects.filter(name=lists.get('long_name'))
                if not len(country) == 0:
                    break
        else:
            direction = reverse_geocode_result[1].get('formatted_address')
            count = len(reverse_geocode_result) - 1
            country_map = reverse_geocode_result[count].get('formatted_address')
            try:
                country = accounts_models.Country.objects.filter(name=country_map)
            except accounts_models.Country.DoesNotExist:
                raise ValueError('{"country":"' + str(_("The country is not registered in the system")) + '"}')
        user = accounts_models.User()
        data["country_id"] = country[0].id
        data["direction"] = direction
        data["last_name"] = ""
        for key in data.keys():
            if key == 'password':
                data[key] = make_password(data[key])
            setattr(user, key, data[key])
        try:
            user.save(force_insert=True)
        except Exception as e:
            raise ValueError('{"user":"' + str(_("An error occurred while saving the user")) + '"}')
        print(user)
        # add group weedmatch
        group = Group.objects.get(name='WeedMatch')
        user.groups.add(group)
        return user


class RecoverPasswordService:
    """
        this class controls the validation of the mail at the moment in which the user makes a request to change
        the password, as well as the code that sends the results of the request.
    """
    def check_email(self, data: dict) -> accounts_models.User:
        """
            this method verifies that the email sent by the user exists in the database,
            raise a exception if the email does not exist

            :param data: user's email
            :type data: dict
            :return: Model User
            :raises: ValueError
        """
        if not data.get('email'):
            raise ValueError('{"detail":"' + str(_("The mail field can not be empty")) + '"}')
        try:
            user = accounts_models.User.objects.get(email=data.get('email'))
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail":"' + str(_("The mail is not registered in the system")) + '"}')
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        return user

    def check_code(self, data: dict) -> accounts_models.User:
        """
            this method verifies the code sent by the user and if this is in your profile you can make a
            password change, this code is obtained in the previous method. raises exception when the code does
            not exits in the user.

            :param data: code and new password
            :type data: dict
            :return: Model User
            :raises: ValueError
        """
        if not data.get('code'):
            raise ValueError('{"detail":"' + str(_("The code field can not be empty")) + '"}')
        if not data.get('password'):
            raise ValueError('{"detail":"' + str(_("The password can not be empty")) + '"}')
        try:
            user = accounts_models.User.objects.get(recovery=str(data.get('code')))
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail":"' +
                             str(_("Code you sent does not match the one registered in your account")) + '"}')
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        user.password = make_password(str(data.get('password')))
        user.recovery = ''
        user.save()
        return user


class PublicFeedService:
    """
        in this class posse all the necessary methods to visualize people in the public feed 420,
        among them the search of them, the calculation of distance and between them, as well as the calculation of time in upload of an image and the handling of weed -like, weed-deslike
    """
    def list(self, user: accounts_models.User):
        """
            this method obtains all images upload in public feed 420, the images to show depend on
            the user's tendency

            :param user: user weedmtach
            :type user: Model User
            :return: Model PublicFeed and dict with all id of the PublicFeed
        """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        if user.match_sex == accounts_models.User.SEX_OTHER:
            users = accounts_models.User.objects.all().exclude(username=user.username).exclude(is_superuser=True)
        if user.match_sex == accounts_models.User.SEX_MALE:
            users = accounts_models.User.objects.filter(sex=user.match_sex).exclude(username=user.username)\
                .exclude(is_superuser=True)
        if user.match_sex == accounts_models.User.SEX_FEMALE:
            users = accounts_models.User.objects.filter(sex=user.match_sex).exclude(username=user.username)\
                .exclude(is_superuser=True)
        ids = users.aggregate(users_id=ArrayAgg('id'))
        public_feed = accounts_models.PublicFeed.objects.filter(user_id__in=ids.get('users_id'))
        return public_feed, public_feed.aggregate(id_public_feed=ArrayAgg('id'))
    
    def public_profile(self, user: accounts_models.User, pk: int)-> accounts_models.User:
        """
            Obtain the public profile whose image appeared in the public feed the other user.
            raise an exception if the profile of the user to search does not exist in the system

            :param user:
            :param pk:
            :return:
       """
        if user is None or user.is_active is False:
            raise ValueError('{"detail":"' +
                             str(_("In order to perform this operation, your account must be active")) + '"}')
        try:
            public_user = accounts_models.User.objects.get(id=pk)
        except accounts_models.User.DoesNotExist:
            raise ValueError('{"detail":"' + str(_("The user does not exist in the system")) + '"}')
        return public_user

    def distances(self, latA: float, lonA: float, latB: float, lonB: float):
        """
            Distances method performs a calculation involving the radius of the earth, where the
            length and length of one point is compared with another and results in the distance
            between the two points, that distance can be expressed in meters or kilometers depending on
            the result obtained.

            :param latA: latitude the point A.
            :type latA: Float.
            :param lonA: longitude the point A.
            :type lonA: Float.
            :param latB: latitude the point B.
            :type latB: Float.
            :param lonB: longitude the point B.
            :type lonB: Float.
            :return: 999 number and distance in meters if the calcule is less 0.9.
            :return: if the floating point of the number is greater than 5 the value will be
            increased to the next number for example if the value is 4.6 then it will be converted to 5.
            :return:if the floating point of the number is less than 5 the value will be decreased to the
            number for example if the value is 4.4 then it will be converted to 4.
        """
        arccos = math.acos(
            ((math.sin(latA) * math.sin(latB)) + (math.cos(latA) * math.cos(latB))) * math.cos(lonA - lonB))
        result = settings.RADIO_EARTH * arccos
        degrees = (math.pi * result) / 180
        if degrees < 0.9:
            meters = degrees * 1000
            return 999, str(meters)[:3]+" mts"
        if degrees > 1:
            convert = str(degrees)
            value = convert.find(".")
            number = convert[value + 1:value + 2]
            if int(number) >= 5:
                return math.ceil(degrees), str(math.ceil(degrees))[:3]+" km"
            else:
                return degrees, str(degrees)[0:1]+" km"
    
    def time_format(self, date_now, date_result):
        """
            in this method the result of subtracting the date in which a user uploaded a photo to
            the public feed 420 is calculated with the time of the server, the time will be formed
            depending on whether they are seconds, minutes, hour, day after a single week passes
            it will be shown on the day the month and the year in which the photo was uploaded

            :param date_now: current date with the hour, minute and seconds
            :type date_now: datetime
            :param date_result: is the result of subtracting two date
            :type date_result: datetime.timedelta
            :return: date format
        """
        date_string = str(date_result).split(".")[0]
        if len(date_string) == 7:
            if int(date_string[0:1]) >= 1 and int(date_string[0:1]) < 10:
                return date_string[0:1]+" hours"
            if date_string[2:4] == "00":
                if int(date_string[5:6]) == 0:
                    return date_string[6:7] + " seconds"
                else:
                    return date_string[5:7] + " seconds"
            if int(date_string[2:3]) == 0:
                #print(date_string[3:4])
                return date_string[3:4] + " minutes"
            else:
                #print(date_string[2:4])
                return date_string[2:4] + " minutes"	
        elif len(date_string) == 8:
            return date_string[0:2] + " hours"
        elif len(date_string) >= 14:
            return date_string[:-13] + " days"
            if int(date_string[:-13]) > 7:
                date = date_now - datetime_module.timedelta(days=int(date_string[:-13]))
            if int(date_now.strftime("%Y")) > int(date.strftime("%Y")):
                return date.strftime("%d the %B the %Y")
            else:
                #print(month[date.strftime("%B")])
                return date.strftime("%d the %B")

    def distance_feed(self, user: accounts_models.User, latitud: str, longitud: str, datas: list):
        """
            this method calls the distance of the method to perform the calculation of the latitude and
            longitude of the user with the latitude and longitude of the user that will be displayed in
            the public feed 420 depending on the user's tendency.
            if the user turns on the gps and sends the latitude and longitude of its current position, the
            calculation is made based on its position if it is not performed with the one registered at the
            time of registering in weedmatch.

            :param user: user weedmatch.
            :type user: Model User.
            :param latitud: latitude of user if turns on your gps.
            :type latitud: String.
            :param longitud: longitude of use if tunds of your gps.
            :type longitud: String.
            :param datas: list contain all image upload in public feed 420 depending of user's tendency.
            :type datas: List.
            :return: list with the distance.
        """
        if not latitud:
            latitud = user.latitud
        if not longitud:
            longitud = user.longitud
        list_accept = []
        for data in datas:
            distance, str_distance = self.distances(float(data.get('latitud')), float(data.get('longitud')),
                                                    float(latitud), float(longitud))
            if distance == 999:
                data['distance'] = str_distance
                data.pop('latitud')
                data.pop('longitud')
                list_accept.append(data)
            if not distance >= user.distance:
                data['distance'] = str_distance
                data.pop('latitud')
                data.pop('longitud')
                list_accept.append(data)
        datas.clear()
        return list_accept

    def distance_user(self, user: accounts_models.User, user_pk: accounts_models.User, latitud: str, longitud: str):
        """
            this method performs the calculation between the latitude and longitude recorded in the user who
            makes the request with the latitude and longitude of the user who is viewing his public profile,
            this calculation varies depending on whether the user sending the request has turned on his gps.

            :param user: user weedmatch
            :type user: Model User
            :param user_pk: user weedmatch
            :type user_pk: Model User
            :param latitud: latitude of user if turns on your gps.
            :type latitud: String.
            :param longitud: longitude of user if turns on your gps.
            :type longitud: String.
            :return: the distance the user who made the visit and the user who is viewing their public profile
        """
        public_image_user = accounts_models.Image.objects.filter(user_id=user_pk.id).last()
        if not public_image_user:
            return ""
        if not latitud:
            latitud = user.latitud
        if not longitud:
            longitud = user.longitud
        distance, str_distance = self.distances(float(latitud), float(longitud),
                                                float(user_pk.latitud), float(user_pk.longitud))
        return str_distance

    def like_user(self, id_user: int, datas: dict, ids: dict):
        """
            In this method, you will search within all the images brought by the list method of the class,
            if the user in section gave a like to that image and consequently will change the internal
            flag of the image, so the front will have control of all the like that the user has given.

            :param id_user: id user weedmatch
            :param datas: serialized information that contains the entire image in the public feed 420
            depending on the user's distance and current.
            :type datas: dict.
            :param ids: id of all PrublicFeed
            :type ids: dict
            :return: datas with change the field band
        """
        like_user = accounts_models.LikeUser.objects.filter(id_user=id_user,
                                                            id_public_feed__in=ids.get('id_public_feed'))
        for list in like_user:
            for data in datas:
                if list.id_public_feed == data.get('id'):
                    data['band'] = str(list.like)
        return datas
