from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now


class Country(models.Model):
    name = models.CharField(_('Country name'), max_length=50, blank=False, null=False)
    code = models.CharField(_('Code'), max_length=2, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey('Country', related_name='country_city', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_('City name'), max_length=50, blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    SEX_MALE = "Hombre"
    SEX_FEMALE = "Mujer"
    SEX_OTHER = "Otro"
    TYPE_SEX = (
        (SEX_MALE, _('Hombre')),
        (SEX_FEMALE, _('Mujer')),
        (SEX_OTHER, _("Otro"))
    )

    country = models.ForeignKey('Country', related_name='country_user', on_delete=models.CASCADE, null=True, blank=True)
    recovery = models.CharField(_('Recovery'), max_length=40, blank=True)
    image = models.CharField(_('Photo'), max_length=255, blank=True, null=True)
    count_image = models.IntegerField(_('Count'), default=0, blank=True, null=True)
    direction = models.CharField(_('Direction'), max_length=255, blank=True, null=True)
    age = models.DateField(_('Age'), null=True, blank=True)
    sex = models.CharField(_('Type_sex'), max_length=10, choices=TYPE_SEX, default=SEX_OTHER, blank=True, null=True)
    latitud = models.DecimalField(_('Latitud'), max_digits=10, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(_('Longitud'), max_digits=10, decimal_places=6, blank=True, null=True)
    description = models.CharField(_('Description'), max_length=255, blank=True, null=True)
    match_sex = models.CharField(_('Match_sex'), max_length=10, choices=TYPE_SEX, default=SEX_OTHER, blank=True, null=True)
    facebook_id = models.CharField(max_length=140, blank=True, null=True)
    facebook_access_token = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username
    
    def count_increment(self):
        self.count_image += 1
        self.save()
    
    def count_delete(self):
        self.count_image -= 1
        self.save()
    
    def assign_image_profile(self, image_name):
        self.image = image_name
        self.save()
    

class ImageProfile(models.Model):
    user = models.ForeignKey('User', related_name='user_image_profile', on_delete=models.CASCADE, null=True, blank=True)
    image_profile = models.ImageField(_('Image'), upload_to='profile', max_length=255, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user.username


class Image(models.Model):
    user = models.ForeignKey('User', related_name='user_image', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to='profile_420', max_length=255, blank=False, null=False)
    like = models.IntegerField(_('weedy-like'), default=0, null=False, blank=False)
    state = models.CharField(_('State_image'), max_length=255, blank=False, null=False)
    latitud = models.DecimalField(_('Latitud_image'), max_digits=10, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(_('Longitud_image'), max_digits=10, decimal_places=6, blank=True, null=True)
    created = models.DateTimeField(default=now, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user.username


class PublicFeed(models.Model):
    user = models.ForeignKey('User', related_name='user_image_feed', on_delete=models.CASCADE, null=True, blank=True)
    id_image = models.IntegerField(_('Image_id'), blank=True, null=True)
    image = models.CharField(_('Image'), max_length=255, blank=True, null=True)
    like = models.IntegerField(_('weedy-like'), default=0, null=False, blank=False)
    state = models.CharField(_('State_image'), max_length=255, blank=True, null=True)
    latitud = models.DecimalField(_('Latitud_image'), max_digits=10, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(_('Longitud_image'), max_digits=10, decimal_places=6, blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.user.username

    def increment_like(self):
        self.like += 1
        self.save()

    def decrement_like(self):
        if self.like == 0:
            self.like = 0
            self.save()
        else:
            self.like -= 1
            self.save()


class LikeUser(models.Model):
    id_user = models.IntegerField(_('user_id'), blank=True, null=True)
    id_public_feed = models.IntegerField(_('public_feed_id'), blank=True, null=True)
    like = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return str(self.id)

    def change_like(self, band):
        if band:
            self.like = True
            self.save()
        else:
            self.like = False
            self.save()

class TermsCondition(models.Model):
    title = models.CharField(_('Title'), max_length=50, blank=False, null=False)
    description = models.TextField(_('Description'), blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title