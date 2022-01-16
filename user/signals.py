from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile
from dashboard .models import Category, profileConfig
from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            first_name = user.first_name,
            last_name = user.last_name,
        )

        categorys = Category.objects.all()
        for cat in categorys:
            if cat.name != 'Others':
                profileConfig.objects.create(
                    owner = profile,
                    cat_id = cat,
                    cat_status = False,
                )

        subject = "Welcome to SADNS"
        message = 'Thank you for creating a parenting account with SA DNS. We are glad you are here!'

        send_mail(
            subject, 
            message, 
            settings.EMAIL_HOST_USER, 
            [profile.email],
            fail_silently=False,
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)