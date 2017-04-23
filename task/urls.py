from django.conf.urls import url
from .views import TaskSearchView

from . import views

app_name = 'task'
urlpatterns = [
    url(r'^(?:(?P<filter>(\w+)))?$', views.TaskView.as_view(), name="task"),
    url(r'^(?:(?P<filter>(\w+))/)?create/$',
        views.create_task, name="create_task"),
    url(r'^(?:(?P<filter>(\w+))/)?remove/(?P<pk>(\d+))/$',
        views.remove_task, name="remove_task"),
    url(r'^(?:(?P<filter>(\w+))/)?edit/(?P<pk>(\d+))/$',
        views.edit_task, name="edit_task"),
    url(r'^(?:search/)?is_done/$', views.is_done, name="is_done"),
    url(r'^(?:search/)?timer/$', views.timer, name="timer"),
    url(r'^(?:search/)?timer_value/$', views.timer_value, name="timer_value"),
    url(r'^pagination_ajax/$', views.pagination_ajax, name='pagination_ajax'),
    url(r'search/', TaskSearchView(), name='haystack_search'),
]
