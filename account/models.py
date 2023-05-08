from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


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




# Create your models here.
class Consult(models.Model):
    name = models.CharField(max_length=16, null=True)
    position = models.CharField(max_length=16, null=True)
    group = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=14, null=True)
    describe = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Consult'
