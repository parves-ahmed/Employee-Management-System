from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserForm
from .models import *
from employee_management_system.decorators import admin_hr_required, admin_only

# Create your views here.


def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            context['error'] = 'Provide valid info'
            return render(request, 'auth/login.html', context)
    else:
        return render(request, 'auth/login.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'auth/success.html', context)


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))


@login_required(login_url='login/')
def employee_list(request):
    print(request.role)
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Employees'
    return render(request, 'employee/employee_list.html', context)


@login_required(login_url='login/')
def employee_details(request, id):
    context = {}
    context['user'] = get_object_or_404(User, id=id)
    return render(request, 'employee/employee_details.html', context)


@login_required(login_url='login/')
@admin_only
def employee_add(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/employee_add.html', {'user_form': user_form})
    else:
        user_form = UserForm()
        return render(request, 'employee/employee_add.html', {'user_form': user_form})


@login_required(login_url='login/')
def employee_update(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/employee_update.html', {'user_form': user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'employee/employee_update.html', {'user_form': user_form})


@login_required(login_url='login/')
def employee_delete(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {}
        context['user'] = user
        return render(request, 'employee/employee_delete.html', context)