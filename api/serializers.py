from rest_framework import serializers
# Import models from DASHBOARD
from dashboard.models import *
from user.models import *

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = '__all__'

class DomainSerializer(serializers.ModelSerializer):
  class Meta:
    model = Domain
    fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'
  
    

