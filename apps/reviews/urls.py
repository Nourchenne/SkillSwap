from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:exchange_id>/', views.leave_review, name='create'),
]

