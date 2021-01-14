from django.views import generic

from .forms import SignUpForm


class SignUpView(generic.CreateView):

    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = '/login/'
