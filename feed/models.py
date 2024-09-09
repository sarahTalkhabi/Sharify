from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    text = models.TextField(validators=[MaxLengthValidator(200)], null=True)
    image = models.ImageField(upload_to='upload', null=True)
    video = models.FileField(upload_to='media', null=True)
    date = models.DateField(auto_now_add=True)
    like = models.IntegerField()
    objects = models.Manager()

