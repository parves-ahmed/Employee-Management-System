from django.urls import path

from polls.views import PollView
from . import views

urlpatterns = [
    path('add/', PollView.as_view(), name='poll_add'),
    path('<int:id>/edit/', PollView.as_view(), name='poll_edit'),
    path('<int:id>/delete/', PollView.as_view(), name='poll_delete'),
    path('poll/list/', views.index, name='polls'),
    path('<int:id>/details', views.details, name='poll_detail'),
    path('<int:id>/vote', views.poll, name='single_poll'),
    path('my_poll/list/', views.my_poll, name='my_polls'),
]