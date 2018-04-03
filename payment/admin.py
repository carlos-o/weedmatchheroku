from django.contrib import admin
from payment import models as payment_models


class CreditCardAdmin(admin.ModelAdmin):
    """
       register the information of the fields of the credit card in django admin
    """
    list_display = ('id', 'user', 'first_name', 'type_card', 'number_card', 'created',)
    search_fields = ('user', 'first_name',)
    list_filter = ('created', 'type_card')


admin.site.register(payment_models.CreditCard, CreditCardAdmin)
