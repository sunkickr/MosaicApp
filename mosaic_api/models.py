from django.db import models
from django.core.files import File
from mosaic_api.model_functions import mosaic, thumb, newmosaic

# Create your models here.
class Mosaic(models.Model):
    name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(upload_to = 'images/')
    mosaic = models.ImageField(upload_to = 'mosaic/')

    def save(self, *args, **kwargs):
        self.mosaic = mosaic(self.image)
        super().save(*args, **kwargs)

class Album(models.Model):
    order = models.PositiveIntegerField(default=9999)
    create_at = models.DateTimeField(auto_now_add=True)

class Image(models.Model):
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'new/sourceimages/')

    def save(self, *args, **kwargs):
        self.image = thumb(self.image, 50)
        super().save(*args, **kwargs)

class NewMosaic(models.Model):
    create_at = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(upload_to = 'new/images/')
    mosaic = models.ImageField(upload_to = 'new/mosaic/')

    def save(self, *args, **kwargs):
        self.mosaic = newmosaic(self.image)
        super().save(*args, **kwargs)

 
