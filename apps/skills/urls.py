from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('browse/', views.browse_skills, name='browse'),
    path('<int:pk>/', views.skill_detail, name='detail'),
    path('offer/create/', views.create_skill_offer, name='create_offer'),
    path('offer/<int:pk>/edit/', views.edit_skill_offer, name='edit_offer'),
    path('offer/<int:pk>/delete/', views.delete_skill_offer, name='delete_offer'),
    path('request/create/', views.create_skill_request, name='create_request'),
]

