# This code block is defining the URL patterns for a Django web application. Each `path` function maps
# a URL pattern to a specific view function within the Django application. Here's a breakdown of what
# each path is doing:

from django.urls import path,include
from . import views
# from .views import myview
# from rest_framework.routers import DefaultRouter
# from .views import LoginViewSet

# router = DefaultRouter()
# router.register(r'login', LoginViewSet)


urlpatterns = [
    
    # path('register/', views.register_view, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # path('api/', include(router.urls)),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),
    
    
    path('',views.home, name='home'),
    path('room/<str:pk>/',views.room, name='room'),
    path('profile/<str:pk>/', views.userprofile, name='user-profile'),
    # path('upload/', views.upload_profile, name='upload-profile'),
    
    
    path('create-room/',views.create_room, name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/',views.deleteMessage, name='delete-message'),
    
    
    path('update-user/',views.updateUser, name='update-user'),
    path('topic/',views.topic_room, name='topic'),
    path('activity/',views.activityPage, name='activity'),
    
    # path('myview/', myview.as_view(), name='my-view'),
    # path('', Home.as_view(), name='home'),
]
