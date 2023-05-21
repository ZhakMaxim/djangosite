"""MarkingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import rest_framework_simplejwt
from rest_framework_simplejwt import views
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from edushedule.views import *

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'id', ScheduleViewSet)
router.register(r'student', StudentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('token/obtain/', rest_framework_simplejwt.views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', rest_framework_simplejwt.views.TokenRefreshView.as_view(), name='token_refresh'),
    path('eduschedule/api/v1/register', UserRegistrationView.as_view(), name='register'),
    path('eduschedule/api/v1/login', UserAuthorizationView.as_view(), name='login'),
    # path('eduschedule/users', UserListView.as_view(), name='users'),
    path('eduschedule/api/v1/', include(router.urls), name='events'),
    path('eduschedule/api/v1/events/photo/<int:event_id>/', EventPhotoView.as_view(), name='event-photo'),
    path('eduschedule/api/v1/students', StudentListView.as_view()),
    path('eduschedule/api/v1/students/<int:pk>/', StudentMarksListView.as_view({'get': 'list'})),
    # path('eduschedule/api/v1/students/<int:pk>', StudentMarkDetailView.as_view()),
    path('eduschedule/api/v1/marks/<int:pk>/create', StudentMarkDetailView.as_view()),
    path('eduschedule/api/v1/marks/<int:pk>/', MarkDetailView.as_view()),
    path('eduschedule/api/v1/schedule/<int:pk>/', ScheduleListView.as_view({'get': 'list'})),
    path('eduschedule/api/v1/schedule/', include(router.urls)),
]


