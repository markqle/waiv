from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from waivapp.models import WaivUser

# Register your models here.
class UserModel(UserAdmin):
    pass

admin.site.register(WaivUser, UserModel)