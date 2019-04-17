from django.http import HttpResponseRedirect
from django.urls import reverse


def admin_hr_required(view_func):
    def wrap(request, *args, **kwargs):
        allowed_role = ["Admin", "HR"]
        if request.role in allowed_role:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('employee_list'))
    return wrap


def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.role == 'Admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('employee_list'))
    return wrap