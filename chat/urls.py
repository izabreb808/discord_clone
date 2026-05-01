from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('channel/<int:id>/', views.channel),
    path('channel/<int:id>/join/', views.join_channel),
    path('channels/new/', views.create_channel),
    path('delete/<int:id>/', views.delete_message),
    path('profile/', views.edit_profile),
    path('block/<int:id>/', views.block_user),
    path('unblock/<int:id>/', views.unblock_user),
    path('dm/<int:user_id>/', views.direct_messages),
    path('logout/', views.logout_view),
    path('register/', views.register_view),
]
