from django.views import generic

from .forms import UserCreationForm


class SignUpView(generic.CreateView):

    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = '/login/'
