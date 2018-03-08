from django.contrib import admin
from accounts import models as accounts_models


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'typeUser')
    search_fields = ('username', 'first_name', 'last_name',)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'state', 'created',)
    search_fields = ('user',)
    list_filter = ('created',)


class ImageProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image_profile', 'created')
    search_fields = ('user',)
    list_filter = ('created',)


admin.site.register(accounts_models.ImageProfile, ImageProfileAdmin)
admin.site.register(accounts_models.Image, ImageAdmin)
admin.site.register(accounts_models.User, UserAdmin)
admin.site.register(accounts_models.Country, CountryAdmin)