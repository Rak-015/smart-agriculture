from django.db import models
import os



# Create your models here.
class Plants(models.Model):
    image = models.ImageField(upload_to='static/assets/images')

    def filename(self):
        return os.path.basename(self.image.name) 
    
class Soil_History(models.Model):
    prediction = models.CharField(max_length=200)
    fertilizer = models.TextField()
    created = models.DateTimeField(auto_now_add=True) 

class Crop_History(models.Model):
    crop = models.TextField()
    created = models.DateTimeField(auto_now_add=True) 

class Plant_History(models.Model):
    upload_image = models.ImageField(upload_to='static/assets/upload_image')
    prediction = models.TextField()
    created = models.DateTimeField(auto_now_add=True) 

    




