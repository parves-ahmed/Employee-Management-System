from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.


@login_required(login_url='login/')
def index(request):
    context = {}
    questions = Question.objects.all()
    context['title'] = 'polls'
    context['questions'] = questions
    return render(request, 'poll/index.html', context)


@login_required(login_url='login/')
def details(request, id):
    context = {}
    question = Question.objects.get(id=id)
    context['question'] = question
    return render(request, 'poll/detail.html', context)


@login_required(login_url='login/')
def poll(request, id=None):
    if request.method == "GET":
        try:
            question = Question.objects.get(id=id)
        except:
            raise Http404

        context = {}
        context['question'] = question
        return render(request, 'poll/poll.html', context)

    if request.method == "POST":
        user_id = 1
        data = request.POST
        ret = Answer.objects.create(user_id=user_id, choice_id=data['choice'])
        if ret:
            return HttpResponse("success")
        else:
            return HttpResponse("Failed")




