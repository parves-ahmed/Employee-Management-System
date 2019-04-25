"""employee_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from employee.views import user_login, success, user_logout, ProfileUpdate, MyProfile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
    path('', include('employee.urls')),

    path('login/', user_login, name='user_login'),
    path('success', success, name='user_success'),
    path('logout', user_logout, name='user_logout'),
    path('profile', MyProfile.as_view(), name='my_profile'),
    path('profile_update', ProfileUpdate.as_view(), name='update_profile'),
]
