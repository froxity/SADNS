from django.db import models
import uuid
from user.models import Profile


class profileConfig(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    owner = models.ForeignKey(Profile,null=True, blank=True,on_delete=models.SET_NULL)
    cat_id = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    cat_status = models.BooleanField()

    def __str__(self):
        return self.cat_id.name
    
    class Meta:
        ordering = ['cat_id']
    

class Whitelist(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
    wl_domain = models.CharField(max_length=500)
    wl_comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wl_domain

class Blacklist(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
    bl_domain = models.CharField(max_length=500)
    bl_comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bl_domain

class Domain(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    owner = models.ForeignKey(Profile,null=True, blank=True,on_delete=models.SET_NULL)
    domain = models.CharField(max_length=500)
    freq = models.IntegerField(null=True, blank=True)
    cat_id = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.domain

class Category(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
