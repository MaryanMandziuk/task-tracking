from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import EmailForm, PasswordForm

app_name = 'account'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='account:login'),
        name='logout'),
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='account/reset.html',
            email_template_name='account/reset_email.html',
            success_url=reverse_lazy('account:reset_done'),
            form_class=EmailForm),
        name='reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='account/reset_done.html'),
        name='reset_done'),
    url(r'^reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/reset_confirm.html',
            form_class=PasswordForm,
            success_url=reverse_lazy('account:reset_complete')),
        name='reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='account/reset_complete.html'),
        name='reset_complete'),

]
