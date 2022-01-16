from django.contrib import admin
from .models import *

admin.site.register(profileConfig)
admin.site.register(Whitelist)
admin.site.register(Blacklist)
admin.site.register(Domain)
admin.site.register(Category)

# Register your models here.
