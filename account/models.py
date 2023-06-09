from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

class UserProfile(models.Model):
    objects = models.manager
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,related_name='user_profile')
    firstName = models.CharField(max_length=100,null=True)
    lastName = models.CharField(max_length=100,null=True)
    location = models.CharField(max_length=50,null=True)
    bio = models.CharField(max_length=500, null=True)
    image = models.ImageField(upload_to='profile',null=True)
    followers = models.ManyToManyField(User,null=True)



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )




