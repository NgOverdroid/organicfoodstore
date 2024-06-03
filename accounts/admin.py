from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Profile)

class ProfileInline(admin.StackedInline): #Mix profile info and user info in django admin
    model = Profile

class UserAdmin(admin.ModelAdmin): #extends user model
    model = User
    field = ["username", "first_name", "last_name", "email", "phone", "address"]
    inlines = [ProfileInline]

#Unregister the built in User model
admin.site.unregister(User)
#Register the custom User model
admin.site.register(User, UserAdmin)