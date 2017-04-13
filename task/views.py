from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Task


class TaskView(generic.ListView):
    template_name = "task/task.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.order_by("created")[:9]



def create_task(request):
    name = request.POST.get('name', None)
    description = request.POST.get('description', None)

    task = Task(name=name, description=description)
    task.save()
    return HttpResponseRedirect("/")

def remove_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return HttpResponseRedirect("/")


def edit_task(request, pk):
    task = Task.objects.get(pk=pk)
    print(task.description)
    tasks = Task.objects.order_by("created")[:9]
    if request.method == 'POST':
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        task.name = name
        task.description = description
        task.save()
        return HttpResponseRedirect("/")
    return render(request, "task/edit_task.html", {'task':task, 'tasks':tasks})
