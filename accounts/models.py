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
    image = models.ImageField(_('Photo'), upload_to='profile', max_length=255, blank=True, null=True)
    direction = models.CharField(_('Direction'), max_length=255, blank=True)
    age = models.DateField(_('Age'), null=True, blank=True)
    latitud = models.DecimalField(_('Latitud'), max_digits=10, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(_('Longitud'), max_digits=10, decimal_places=6, blank=True, null=True)
    description = models.CharField(_('Description'), max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
