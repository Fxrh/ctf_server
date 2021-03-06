from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext, loader
from django.views import generic
from django.core.urlresolvers import reverse
from django.core import exceptions

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from challenges.models import Challenge, User, ChallengeCategory
from challenges.forms import InfoForm, CreateChallengeForm, EditChallengeForm, EditAccountForm

from challenges import backend, settings

def standardContext(request):
    context = {}
    if request.user.is_authenticated():
        context['username'] = request.user.get_username()
        context['user'] = User.from_authuser(request.user)
    if settings.PRESENTATION_MODE:
        context['presentation_mode'] = True
    context['host_name'] = settings.HOST_NAME
    return context


def index(request):
    context = standardContext(request)
    context['is_index'] = True

    category_list = ChallengeCategory.objects.all()
    nonempty_category_list = []
    for category in category_list:
        if category.challenges().count() > 0:
            nonempty_category_list.append(category)

    num_nonempty_categories = len(nonempty_category_list)
    context["column_width"] = max(int(12 / max(1, num_nonempty_categories)), 2)
    cats = []

    for category in nonempty_category_list:
        challenge_list = []
        for challenge in category.challenges():
            c = {"id": challenge.id, "name": challenge.name, "points": challenge.points}
            if request.user.is_authenticated():
                u = User.from_authuser(request.user)
                c["solved"] = u.has_solved(challenge)
                c["is_author"] = u.is_author(challenge)
            challenge_list.append(c)
        cats.append({"name": category.name, "list": challenge_list})
    context['cats'] = cats
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

    if settings.PRESENTATION_MODE:
        context['solved_by'] = challenge.solved_by.filter(allow_create=False)
    else:
        context['solved_by'] = challenge.solved_by.all()
    context['author'] = challenge.author

    return render(request, 'challenges/info.html', context)


def ranking(request):
    context = standardContext(request)
    context['is_ranking'] = True
    users = User.getRanking(settings.PRESENTATION_MODE)

    context['users'] = users
    return render(request, 'challenges/ranking.html', context)


@login_required(login_url="challenges:login")
def myChallenges(request):
    context = standardContext(request)
    context['is_mychallenges'] = True
    user = User.from_authuser(request.user)

    context['challenges'] = user.created_challenges()
    return render(request, 'challenges/myChallenges.html', context)


def showAccount(request, user_id):
    context = standardContext(request)
    shown_user = get_object_or_404(User, pk=user_id)
    context['shown_user'] = shown_user
    context['shown_username'] = shown_user.authuser.get_username()

    if request.user.is_authenticated():
        user = User.from_authuser(request.user)
        if user == shown_user:
            context['own_account'] = True

    return render(request, 'challenges/account.html', context)


@login_required(login_url="challenges:login")
def createChallenge(request):
    context = standardContext(request)
    user = User.from_authuser(request.user)

    if not user.allow_create:
        raise exceptions.PermissionDenied()

    if request.method == "POST":
        form = CreateChallengeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['challenge_name'].strip()
            category = form.cleaned_data['category']
            if Challenge.objects.filter(name=name).count() > 0:
                context['error_msg'] = "A challenge with this name already exists."
            else:
                challenge = Challenge.create_challenge(name, 'SomeFlag', user, 100, category)
                try:
                    backend.create_challenge(challenge, user)
                except Exception as e:
                    challenge.delete()
                    raise e
                return redirect("challenges:edit", challenge_id=challenge.id)
        else:
            context['error_msg'] = "Bad data"
    else:
        form = CreateChallengeForm()
    context['form'] = form

    return render(request, 'challenges/create.html', context)


@login_required(login_url="challenges:login")
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
            form.save()
            if "points" in form.changed_data:
                print("Points changed, recalculating...")
                for user in User.objects.all():
                    if user.got_points(challenge):
                        user.recalculate_points()
            context["success_msg"] = 'Changes saved.'
        else:
            context["error_msg"] = 'Bad Data'
    else:
        form = EditChallengeForm(instance=challenge)
    context['form'] = form
    context['challenge'] = challenge

    return render(request, 'challenges/edit.html', context)


@login_required(login_url="challenges:login")
def editAccount(request):
    context = standardContext(request)
    user = User.from_authuser(request.user)

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            backend.update_keys_for_user(user)
            context["success_msg"] = 'Changes saved.'
    else:
        form = EditAccountForm(instance=user)
    context['form'] = form

    return render(request, 'challenges/editAccount.html', context)


def createAccount(request):
    if request.user.is_authenticated():
        return redirect("challenges:index")

    context = standardContext(request)
    if request.method == 'POST':
        form = auth.forms.UserCreationForm(request.POST)
        if form.is_valid():
            authuser = form.save()
            user = User.create_user(authuser)
            # not quite sure how to login the user automatically
            return redirect("challenges:login")
    else:
        form = auth.forms.UserCreationForm()
    context['form'] = form

    return render(request, 'challenges/createAccount.html', context)


