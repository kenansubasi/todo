from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from modules.users.models import User


admin.register(User, UserAdmin)
