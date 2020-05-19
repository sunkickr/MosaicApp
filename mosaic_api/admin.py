from django.contrib import admin
from .models import Mosaic, Album, Image, NewMosaic

# Register your models here.

admin.site.register(Mosaic)
admin.site.register(Album)
admin.site.register(Image)
admin.site.register(NewMosaic)