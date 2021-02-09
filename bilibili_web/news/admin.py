from django.contrib import admin

# Register your models here.

from news.models import UpInfo, Video
admin.register(UpInfo)
admin.register(Video)