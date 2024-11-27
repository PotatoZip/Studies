from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user-list'),  # Obsługa GET i POST dla listy użytkowników
    path('users/<int:pk>/', views.user_delete, name='user-delete'),  # Obsługa DELETE dla użytkownika
]

