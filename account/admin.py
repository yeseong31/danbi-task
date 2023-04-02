from django.contrib import admin

from account.models import User, Team

admin.site.register(User)
admin.site.register(Team)
