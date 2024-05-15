from django.contrib import admin
from Users.models import *


admin.site.register(CustomUser)
admin.site.register(CustomUserProfile)
