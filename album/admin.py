from django.contrib import admin
from .models import AlbumInfo
# Register your models here.

class AlbumInfoAdmin(admin.ModelAdmin):
    list_display = ('user','title','photo')

admin.site.register(AlbumInfo, AlbumInfoAdmin)