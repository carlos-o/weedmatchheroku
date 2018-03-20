from django.contrib import admin
from accounts import models as accounts_models
from django.contrib.auth.admin import UserAdmin as UserAdminProfile


class UserAdmin(UserAdminProfile):
    class Meta:
        model = accounts_models.User
        ordering = ('id',)
    fieldsets = (
        (None, {'fields':
                    ('username', 'first_name', 'email', 'password', 'country', 'direction', 'age',
                     'sex', 'image', 'count_image', 'latitud', 'longitud', 'description', 'match_sex',
                     'facebook_id', 'facebook_access_token')
                }),
        (('Permissions'), {'fields':
                               ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
                           }),
    )
    list_display = ('id', 'username', 'email', 'typeUser')
    search_fields = ('username', 'first_name', 'last_name',)

    def get_ordering(self, request):
        return ['id']


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code',)

    def get_ordering(self, request):
        return ['id']


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'state', 'created',)
    search_fields = ('user',)
    list_filter = ('created',)

    def get_ordering(self, request):
        return ['id']


class ImageProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image_profile', 'created')
    search_fields = ('user',)
    list_filter = ('created',)

    def get_ordering(self, request):
        return ['id']


class TermConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created')
    search_fields = ('title',)
    list_filter = ('created',)

    def get_ordering(self, request):
        return ['id']


class PublicFeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'id_image','created')
    search_fields = ('user',)
    list_filter = ('created',)

    def get_ordering(self, request):
        return ['id']


admin.site.register(accounts_models.PublicFeed, PublicFeedAdmin)
admin.site.register(accounts_models.ImageProfile, ImageProfileAdmin)
admin.site.register(accounts_models.Image, ImageAdmin)
admin.site.register(accounts_models.User, UserAdmin)
admin.site.register(accounts_models.Country, CountryAdmin)
admin.site.register(accounts_models.TermsCondition, TermConditionAdmin)