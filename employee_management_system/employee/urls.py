from django.urls import path
from . import views

urlpatterns = [
    path('home', views.employee_list, name='employee_list'),
    path('<int:id>/employee_details', views.employee_details, name='employee_details'),
    path('add', views.employee_add, name='employee_add'),
    path('<int:id>/update', views.employee_update, name='employee_update'),
    path('<int:id>/delete', views.employee_delete, name='employee_delete')

]