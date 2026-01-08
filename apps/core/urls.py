from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/mark-all/', views.mark_all_notifications_read, name='notifications_mark_all'),
    path('notifications/<int:pk>/mark-read/', views.mark_notification_read, name='notification_mark_read'),
    path('notifications/<int:pk>/mark-unread/', views.mark_notification_unread, name='notification_mark_unread'),
    # JSON API for navbar dropdown
    path('notifications/api/list/', views.api_notifications_list, name='notifications_api_list'),
    path('notifications/api/unread-count/', views.api_unread_count, name='notifications_api_unread_count'),
    path('notifications/api/mark-read/<int:pk>/', views.api_mark_read, name='notifications_api_mark_read'),
    path('notifications/api/mark-all-read/', views.api_mark_all_read, name='notifications_api_mark_all_read'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
