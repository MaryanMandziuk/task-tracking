from django.conf.urls import url


from . import views

app_name = 'task'
urlpatterns = [
    url(r'^(?:(?P<filter>(\w+)))?$', views.TaskView.as_view(), name="task"),
    url(r'^create/$', views.create_task, name="create_task"),
    url(r'^remove/(\d+)/$', views.remove_task, name="remove_task"),
    url(r'^edit/(\d+)/$', views.edit_task, name="edit_task"),
    url(r'^is_done/$', views.is_done, name="is_done"),
    url(r'^timer/$', views.timer, name="timer"),
    url(r'^timer_value/$', views.timer_value, name="timer_value"),
    url(r'^pagination_ajax/$', views.pagination_ajax, name='pagination_ajax'),
]
