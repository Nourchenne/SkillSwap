from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation'),
    path('conversation/<int:conversation_id>/end/', views.end_course, name='end_course'),
    path('start/<str:username>/', views.start_conversation, name='start'),
]

