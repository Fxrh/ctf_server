from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext, loader
from django.views import generic
from django.core.urlresolvers import reverse

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from challenges.models import Challenge, User, ChallengeCategory
from challenges.forms import InfoForm, CreateChallengeForm, EditChallengeForm

def standardContext(request):
    if request.user.is_authenticated():
        return {'username': request.user.get_username()}
    return {}


def index(request):
    context = standardContext(request)
    category_list = ChallengeCategory.objects.all()
    context['category_list'] = category_list
    return render(request, 'challenges/index.html', context)


def info_test_form(request, challenge, form, context):
    if form.is_valid():
        submitted_solution = form.cleaned_data['try_solution']
        if challenge.check_solution(submitted_solution):
            context['success_msg'] = "Success!"
            if request.user.is_authenticated():
                user = User.from_authuser(request.user)
                if user != challenge.author:
                    challenge.set_solved(user)
        else:
            context['error_msg'] = "Sorry, wrong solution..."
    else:
        context['error_msg'] = "Bad data"
    return context


def info(request, challenge_id):
    context = standardContext(request)
    challenge = get_object_or_404(Challenge, pk=challenge_id)
    context['challenge'] = challenge

    if request.method == 'POST':
        form = InfoForm(request.POST)
        context = info_test_form(request, challenge, form, context)
    else:
        form = InfoForm()
    context['form'] = form

    if request.user.is_authenticated():
        user = User.from_authuser(request.user)
        if user.got_points(challenge):
            context['got_points'] = True
        if user == challenge.author:
            context['is_author'] = True

    return render(request, 'challenges/info.html', context)


@login_required
def createChallenge(request):
    context = standardContext(request)
    user = User.from_authuser(request.user)

    if request.method == "POST":
        form = CreateChallengeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['challenge_name'].strip()
            category = form.cleaned_data['category']
            if Challenge.objects.filter(name=name).count() > 0:
                context['error_msg'] = "A challenge with this name already exists."
            else:
                challenge = Challenge.create_challenge(name, 'SomeFlag', user, 100, category )
                return redirect("challenges:info", challenge_id=challenge.id)
        else:
            context['error_msg'] = "Bad data"
    else:
        form = CreateChallengeForm()
    context['form'] = form

    return render(request, 'challenges/create.html', context)


@login_required
def editChallenge(request, challenge_id):
    context = standardContext(request)
    user = User.from_authuser(request.user)
    challenge = get_object_or_404(Challenge, pk=challenge_id)
    is_published_before = challenge.is_published

    if challenge.author != user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = EditChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            is_published = form.cleaned_data['is_published']
            print( "Before: {0}, After: {1}".format(is_published_before, is_published) )
            if (not is_published) and is_published_before:
                context["error_msg"] = 'Cannot unpublish a challenge!'
                challenge = Challenge.objects.get(id=challenge_id)
            else:
                form.save()
                context["success_msg"] = 'Changes saved.'
        else:
            context["error_msg"] = 'Bad Data'
    else:
        form = EditChallengeForm(instance=challenge)
    context['form'] = form
    context['challenge'] = challenge

    return render(request, 'challenges/edit.html', context)