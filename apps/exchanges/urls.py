from django.urls import path
from . import views

app_name = 'exchanges'

urlpatterns = [
    path('propose/<int:offer_id>/', views.propose_exchange, name='propose'),
    path('accept/<int:exchange_id>/', views.accept_exchange, name='accept'),
    path('confirm/<int:exchange_id>/', views.confirm_completion, name='confirm'),
    # Backward-compatibility alias for older templates/doc references
    path('confirm-completion/<int:exchange_id>/', views.confirm_completion, name='confirm_completion'),
]
