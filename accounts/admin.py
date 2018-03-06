from django.contrib import admin
from accounts import models as accounts_models


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email','typeUser')
    search_fields = ('username', 'first_name', 'last_name',)


admin.site.register(accounts_models.User, UserAdmin)