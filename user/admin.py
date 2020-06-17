from django.contrib import admin

from .models import Profile,Brother, Education, Profession, Devotional

admin.site.register(Profile)
admin.site.register(Brother)
admin.site.register(Education)
admin.site.register(Profession)
admin.site.register(Devotional)
# Register your models here.
