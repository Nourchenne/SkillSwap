from django.urls import path
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.community_list, name='list'),
    path('<slug:slug>/', views.community_detail, name='detail'),
    path('<slug:slug>/join/', views.join_community, name='join'),
    path('<slug:slug>/leave/', views.leave_community, name='leave'),
]

