from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from datetime import timedelta
from .models import Task


class TaskView(generic.ListView):
    template_name = "task/task.html"
    context_object_name = "tasks"

    def get_queryset(self):
        # return Task.objects.order_by("created")[:9]


        filter = self.kwargs['filter']
        if filter == None or filter == "creating":
            return Task.objects.order_by("-created")[:9]

        elif filter == "spend":
            return Task.objects.order_by("-timer")[:9]

        elif filter == "name":
            return Task.objects.order_by("name")[:9]

        elif filter == "done":
            return Task.objects.filter(done=True)




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


def is_done(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)

    done = request.GET.get('done', False)
    if done == "1":
        task.done = True
    else:
        task.done = False
    task.save()
    data = {
        'done': done,
    }
    return JsonResponse(data)


def timer(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    timer = request.GET.get('timer', 0)

    task.timer = timedelta(seconds=int(timer))
    task.save()
    data = {
        'done': "done",
    }
    return JsonResponse(data)


def timer_value(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    data = {
        'timer': task.timer.total_seconds(),
    }
    return JsonResponse(data)
