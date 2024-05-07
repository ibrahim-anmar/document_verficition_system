from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')  
