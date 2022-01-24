from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)


urlpatterns = [

  path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 
  path('domains/', views.domains),
  path('category/', views.getCategory),
  path('whitelist/', views.whitelist),
  path('blacklist/', views.blacklist),
  path('profileConfig/', views.getProfileConfig),
  path('profileConfig/<str:pk>', views.putProfileConfig),
  
]
