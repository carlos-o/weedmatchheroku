from django.db import models
from django.utils.translation import ugettext_lazy as _


class CreditCard(models.Model):

    CARD_VISA = "visa"
    CARD_MASTER = "mastercard"
    CARD_AMERICAN = "americanexpress"
    CARD_MAESTRO = "maestro"
    CARD_DISCOVER = "discover"

    TYPE_CARD = (
        (CARD_VISA, _("Visa")),
        (CARD_MASTER, _("MasterCard")),
        (CARD_AMERICAN, _("AmericanExpress")),
        (CARD_MAESTRO, _("Maestro")),
        (CARD_DISCOVER, _("Discover")),
    )

    user = models.ForeignKey('accounts.User', related_name='card_user', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(_('First_name'), max_length=50, blank=True, null=False)
    last_name = models.CharField(_('Last_name'), max_length=50, blank=True, null=False)
    type_card = models.CharField(_('Type_Card'), choices=TYPE_CARD, max_length=20, null=False)
    number_card = models.CharField(_('Number_Card'), max_length=20, null=False)
    cod_security = models.CharField(_('Code_Security'), max_length=4, blank= True, null=True)
    date_expiration = models.DateField(null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.id)
