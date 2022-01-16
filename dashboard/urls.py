from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('webfilter/', views.webfilter, name='webfilter'),
    path('setfilter_true/<str:pk>', views.setfilter_true, name='setfiltertrue'),
    path('setfilter_false/<str:pk>', views.setfilter_false, name='setfilterfalse'),
    path('domains/', views.domains, name='domains'),
    path('edit_wdomain/<str:pk>', views.edit_wdomain, name='edit_wdomain'),
    path('edit_bdomain/<str:pk>', views.edit_bdomain, name='edit_bdomain'),
    path('delete_wdomain/<str:pk>', views.delete_wdomain, name='delete_wdomain'),
    path('delete_bdomain/<str:pk>', views.delete_bdomain, name='delete_bdomain'),
]