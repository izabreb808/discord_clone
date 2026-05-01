from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('channel/<int:id>/', views.channel),
    path('delete/<int:id>/', views.delete_message),
    path('logout/', views.logout_view),
    path('register/', views.register_view),
]
