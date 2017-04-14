from django.conf.urls import url


from . import views

app_name = 'task'
urlpatterns = [
    url(r'^$', views.TaskView.as_view(), name="task"),
    url(r'^create/$', views.create_task, name="create_task"),
    url(r'^remove/(\d+)/$', views.remove_task, name="remove_task"),
    url(r'^edit/(\d+)/$', views.edit_task, name="edit_task"),
    url(r'^is_done/$', views.is_done, name="is_done"),
]
