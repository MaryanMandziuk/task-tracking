from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from datetime import timedelta
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import MaterialSearchForm
from haystack.views import SearchView
import json

item_by_paginate = 9

class TaskSearchView(SearchView):
    def extra_context(self):
        return {'results': self.results}


class TaskView(generic.ListView):
    template_name = "task/task.html"
    context_object_name = "tasks"
    paginate_by = item_by_paginate
    # form_class = MaterialSearchForm

    def get_queryset(self):
        filter = self.kwargs['filter']
        if filter == None or filter == "creating":
            return Task.objects.filter(user=self.request.user)\
                .order_by("-created", "name")[:item_by_paginate]

        elif filter == "spend":
            return Task.objects.filter(user=self.request.user)\
                .order_by("-timer", "name")[:item_by_paginate]

        elif filter == "name":
            return Task.objects.filter(user=self.request.user)\
                .order_by("name", "-timer")[:item_by_paginate]

        elif filter == "done":
            return Task.objects.filter(user=self.request.user,
                done=True).order_by("-created", "name")[:item_by_paginate]


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskView, self).dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super(TaskView, self).get_context_data(**kwargs)
    #     context['form'] = MaterialSearchForm()
    #     # And so on for more models
    #     return context

@login_required
def create_task(request):
    name = request.POST.get('name', 'No name')
    description = request.POST.get('description', None)
    print("DESC: ", len(description))
    task = Task(user=request.user, name=name, description=description)
    task.save()
    return redirect("task:task")


@login_required
def remove_task(request, pk):
    task = Task.objects.get(user=request.user, pk=pk)
    task.delete()
    return HttpResponseRedirect(reverse("task:task"))


@login_required
def edit_task(request, pk):
    task = Task.objects.get(user=request.user, pk=pk)
    tasks = Task.objects.filter(user=request.user).order_by("created")[:9]
    if request.method == 'POST':
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        task.name = name
        task.description = description
        task.save()
        return HttpResponseRedirect(reverse("task:task"))
    return render(request, "task/edit_task.html", {'task':task, 'tasks':tasks})


@login_required
def is_done(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    id = request.GET.get('id', None)
    task = Task.objects.filter(user=request.user).get(pk=id)

    done = request.GET.get('done', False)
    print(done)
    if done == "1":
        task.done = True
    else:
        task.done = False
    task.save()
    data = {
        'done': done,
    }
    return JsonResponse(data)


@login_required
def timer(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    id = request.GET.get('id', None)
    task = Task.objects.filter(user=request.user).get(pk=id)
    timer = request.GET.get('timer', 0)

    task.timer = timedelta(seconds=int(timer))
    task.save()
    data = {
        'done': "done",
    }
    return JsonResponse(data)


@login_required
def timer_value(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    id = request.GET.get('id', None)
    task = Task.objects.filter(user=request.user).get(pk=id)
    data = {
        'timer': task.timer.total_seconds(),
    }
    return JsonResponse(data)


@login_required
def pagination_ajax(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    offset = request.GET.get('offset', 0)
    filter = request.GET.get('filter', 'creating')
    offset = int(offset)
    end = offset + item_by_paginate
    data = []
    if end <= Task.objects.filter(user=request.user).count() + item_by_paginate:
        tasks = None
        end = calculate_end(request.user, filter, end)
        print(offset, end)

        if filter == "spend":
            tasks = Task.objects.filter(user=request.user)\
                .order_by("-timer", "name")[offset:end]
            print(tasks)

        elif filter == "name":
            tasks = Task.objects.filter(user=request.user)\
                .order_by("name", "-timer")[offset:end]

        elif filter == "done":
            tasks = Task.objects.filter(user=request.user,
                done=True).order_by("-created", "name")[offset:end]

        else:
            tasks = Task.objects.filter(user=request.user)\
                .order_by("-created", "name")[offset:end]



        for task in tasks:
            data.append({
                'pk': task.pk,
                'name': task.name,
                'description': task.description,
                'created': str(task.created),
                'finished': str(task.finished),
                'done': str(task.done)
            })

    return HttpResponse(json.dumps(data), content_type='application/json')


def calculate_end(user, filter, end):
    count = 0
    if filter == "spend":
        count = Task.objects.filter(user=user).order_by("-timer", "name").count()
    elif filter == "name":
        count = Task.objects.filter(user=user).order_by("name", "-timer").count()
    elif filter == "done":
        count = Task.objects.filter(user=user).order_by("-created", "name").count()
    else:
        count = Task.objects.filter(user=user).order_by("-created", "name").count()

    if end > count:
        end = count
    return end
