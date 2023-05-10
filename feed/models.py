from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


# Create your models here.

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(validators=[MaxLengthValidator(200)], null=True)
    image = models.ImageField(upload_to='upload', null=True)
    video = models.FileField(upload_to='media', null=True)
    date = models.DateField()
    objects = models.Manager()

