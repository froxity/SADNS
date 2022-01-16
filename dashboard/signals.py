# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver

# from user .models import Profile
# from .models import Category, profileConfig

# def defaultProfileConfig(sender, instance, created, **kwargs):
#   if created:
#     user = instance
#     categorys = Category.objects.all()

#     for cat in categorys:
#       profileconfig = profileConfig.objects.create(
#         owner = user,
#         cat_id= cat.name,
#         cat_status= False,
#       )

# post_save.connect(defaultProfileConfig, sender=Profile)