from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views import generic
from django.core.urlresolvers import reverse

from django.contrib import auth

from challenges.models import Challenge, User


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

#def index(request):
    #challenge_list = Challenge.objects.all()
    #context = {'challenge_list': challenge_list}
    #return render(request, 'challenges/index.html', context)
    

#def info(request, challenge_id):
    #challenge = get_object_or_404(Challenge, pk=challenge_id)
    #return render(request, 'challenges/info.html', {'challenge': challenge})
    
class IndexView(UserMixin, generic.ListView):
    model = Challenge
    template_name = 'challenges/index.html'
    context_object_name = 'challenge_list'


class InfoView(UserMixin, generic.DetailView):
    model = Challenge
    template_name = 'challenges/info.html'

    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            user = User.from_authuser(self.request.user)
            if user.got_points(self.get_object()):  # TODO: besser machen
                context['got_points'] = True
            if user == self.get_object().author:
                context['is_author'] = True
        if hasattr(self.request, 'error_message'):
            context['error_message'] = self.request.error_message
        if hasattr(self.request, 'success_message'):
            context['success_message'] = self.request.success_message
        return context

    def post(self, request, *args, **kwargs):
        try:
            submitted_solution = request.POST['solution']
            if self.get_object().check_solution(submitted_solution):
                self.request.success_message = "Success!"
            else:
                self.request.error_message = "Wrong..."
        except KeyError:
            self.request.error_message = "Something went wrong..."
        return self.get(request, *args, **kwargs)
    

def login(request):
    context = {}
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('challenges:index'))
        else:
            context['error_message'] = "Login failed!"
    except KeyError:
        pass
    return render(request, 'challenges/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('challenges:index'))

