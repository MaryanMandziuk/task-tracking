from django.conf.urls import url

from . import views

app_name = 'task'
urlpatterns = [
    url(r'^(?:(?P<filter>(creating|done|spend|name))/)?$',
        views.TaskView.as_view(), name="task"),
    url(r'^(?:(?P<filter>(creating|done|spend|name))/)?create/$',
        views.create_task, name="create_task"),
    url(r'^(?:(?P<filter>(creating|done|spend|name))/)?remove/(?P<pk>(\d+))/$',
        views.remove_task, name="remove_task"),
    url(r'^(?:(?P<filter>(creating|done|spend|name))/)?edit/(?P<pk>(\d+))/$',
        views.edit_task, name="edit_task"),
    url(r'^(?:.*/)?is_done/$',
        views.is_done, name="is_done"),
    url(r'^(?:.*/)?timer/$',
        views.timer, name="timer"),
    url(r'^(?:.*/)?timer_value/$',
        views.timer_value, name="timer_value"),
    url(r'^(?:.*/)?pagination_ajax/$',
        views.pagination_ajax, name='pagination_ajax'),
    url(r'^search/edit/(?P<pk>(\d+))/(?P<query>(.*))$',
        views.edit_search, name='edit_search'),
    url(r'search/remove/(?P<pk>(\d+))/(?P<query>(.*))$',
        views.remove_search, name='remove_search'),
    url(r'^search/(?:(?P<query>(.*)))?', views.search, name='search'),


]
