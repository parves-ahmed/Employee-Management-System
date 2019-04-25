from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import PollForm, ChoiceForm
from .models import *
from employee_management_system.decorators import admin_hr_required, admin_only

# Create your views here.


class PollView(View):
    decorators = [login_required, admin_hr_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Question, id=id)
            poll_form = PollForm(instance=question)
            choices = question.choice_set.all()
            choice_forms = [ChoiceForm(prefix=str(
                choice.id), instance=choice) for choice in choices]
            template = 'poll/edit_poll.html'
        else:
            poll_form = PollForm(instance=Question())
            choice_forms = [ChoiceForm(prefix=str(
                x), instance=Choice()) for x in range(3)]
            template = 'poll/new_poll.html'
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        context = {}
        if id:
            return self.put(request, id)
        poll_form = PollForm(request.POST, instance=Question())
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return HttpResponseRedirect('/poll/list/')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'poll/new_poll.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        context = {}
        question = get_object_or_404(Question, id=id)
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return redirect('polls_list')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'poll/edit_poll.html', context)

    @method_decorator(decorators)
    def delete(self, request, id=None):
        question = get_object_or_404(Question)
        question.delete()
        return redirect('polls_list')


@login_required(login_url='login/')
def index(request):
    context = {}
    questions = Question.objects.all()
    f_questions = Question.objects.filter(created_by__username=request.user)
    context['title'] = 'polls'
    context['questions'] = questions
    context['f_questions'] = f_questions
    return render(request, 'poll/index.html', context)


@login_required(login_url='login/')
def my_poll(request):
    context = {}
    f_questions = Question.objects.filter(created_by__username=request.user)
    context['title'] = 'polls'
    context['f_questions'] = f_questions
    return render(request, 'poll/my_poll.html', context)


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
        user_id = 8
        data = request.POST
        ret = Answer.objects.create(user_id=user_id, choice_id=data['choice'])

        if ret:
            return HttpResponseRedirect(reverse('polls'))
        else:
            return HttpResponse("Failed")




