from django.contrib import admin

from Grant.models import UserInfo
from Grant.models import Application

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Application)