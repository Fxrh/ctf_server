from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views import generic
from django.core.urlresolvers import reverse

from django.contrib import auth

from challenges.models import Challenge, User, ChallengeCategory
from challenges.forms import InfoForm

def standardContext(request):
    if request.user.is_authenticated():
        return {'username': request.user.get_username()}
    return {}

class UserMixin:

    def get_context_data(self, **kwargs):
        context = super(UserMixin, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['username'] = self.request.user.get_username()
        return context


def generate_message(success):
    if success:
        return {'success_message': "Success!"}
    return {'error_message': "Wrong..."}

def index(request):
    context = standardContext(request)
    category_list = ChallengeCategory.objects.all()
    context['category_list'] = category_list
    return render(request, 'challenges/index.html', context)

def info_test_form(request, challenge, form, context):
    if form.isValid():
        submitted_solution = form.cleaned_data['try_solution']
        if challenge.check_solution(submitted_solution):
            context['success_msg'] = "Success!"
            if request.user.is_authenticated():
                user = User.from_authuser(request.user)
                if user != challenge.author:
                    challenge.set_solved(request.user)
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
    
# class IndexView(UserMixin, generic.ListView):
#     model = ChallengeCategory
#     template_name = 'challenges/index.html'
#     context_object_name = 'category_list'


# class InfoView(UserMixin, generic.DetailView):
#     model = Challenge
#     template_name = 'challenges/info.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(InfoView, self).get_context_data(**kwargs)
#         if self.request.user.is_authenticated():
#             user = User.from_authuser(self.request.user)
#             if user.got_points(self.get_object()):  # TODO: besser machen
#                 context['got_points'] = True
#             if user == self.get_object().author:
#                 context['is_author'] = True
#         if hasattr(self.request, 'error_message'):
#             context['error_message'] = self.request.error_message
#         if hasattr(self.request, 'success_message'):
#             context['success_message'] = self.request.success_message
#         return context
#
#     def post(self, request, *args, **kwargs):
#         try:
#             submitted_solution = request.POST['solution']
#             if self.get_object().check_solution(submitted_solution):
#                 self.request.success_message = "Success!"
#             else:
#                 self.request.error_message = "Wrong..."
#         except KeyError:
#             self.request.error_message = "Something went wrong..."
#         return self.get(request, *args, **kwargs)


class CreateView(UserMixin, generic.TemplateView):
    template_name = 'challenges/create.html'

    def post(self, request, *args, **kwargs):
        submitted_name = request.POST['name'].strip()
        self.request.correct_formatting = False
        self.request.does_not_yet_exist = True
        self.create_success = False
        if 3 <= len(submitted_name) <= 16:
            self.request.correct_formatting = True
        if Challenge.does_name_exist(submitted_name):
            self.request.does_not_yet_exist = False
#        if self.request.correct_formatting and self.request.does_not_yet_exist:

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)
        user = User.from_authuser(self.request.user)
        context['correct_formatting'] = self.request.correct_formatting
        context['does_not_yet_exist'] = self.request.does_not_yet_exist
        return context