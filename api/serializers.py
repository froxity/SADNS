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

class WhitelistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Whitelist
    fields = '__all__'

class BlacklistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Blacklist
    fields = '__all__'

class profileConfigSerializer(serializers.ModelSerializer):
  # cat_id = CategorySerializer(many=False)
  class Meta:
    model = profileConfig
    fields = '__all__'