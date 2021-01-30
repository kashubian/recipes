from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name="accounts/password_change_form.html", success_url=reverse_lazy('accounts:password_change_done')), name='change_password'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name='password_change_done'),
    path('account-activation-sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('account-activated/', views.account_activated, name='account_activated'),
    path('account-activation-failed/', views.activation_failed, name='account_activation_failed')
]
