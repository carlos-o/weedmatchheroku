from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

NORMAL = 'normal'
ADMIN = 'admin'

TYPE_USER = (
    (NORMAL, _('Normal')),
    (ADMIN, _('Admin'))
)


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
    country = models.ForeignKey('Country', related_name='country_user', on_delete=models.CASCADE, null=True, blank=True)
    typeUser = models.CharField(_('TypeUser'), choices=TYPE_USER, max_length=10, default=NORMAL,
                                blank=False, null=False)
    recovery = models.CharField(_('Recovery'), max_length=40, blank=True)
    image = models.CharField(_('Photo'), max_length=255, blank=True, null=True)
    count_image = models.IntegerField(_('Count'), default=0, blank=True, null=True)
    direction = models.CharField(_('Direction'), max_length=255, blank=True)
    age = models.DateField(_('Age'), null=True, blank=True)
    latitud = models.DecimalField(_('Latitud'), max_digits=10, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(_('Longitud'), max_digits=10, decimal_places=6, blank=True, null=True)
    description = models.CharField(_('Description'), max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    def count_increment(self):
        self.count_image += 1
        self.save()
    
    def count_delete(self):
        self.count_image -= 1
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
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['id']

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

    def __str__(self):
        return self.user.username