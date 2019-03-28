from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='polls'),
    path('<int:id>/details', views.details, name='poll_detail'),
    path('<int:id>/vote', views.poll, name='single_poll'),
]