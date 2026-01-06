from django.urls import path
from . import views

app_name = 'credits'

urlpatterns = [
    path('history/', views.credit_history, name='history'),
]

