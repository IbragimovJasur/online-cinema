from apps.users.models import CustomUser
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model= CustomUser
    list_display= ['username', 'email', 'bill', ]

admin.site.register(CustomUser, CustomUserAdmin)
