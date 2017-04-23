from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse, HttpResponse, \
                        HttpResponseBadRequest, Http404
from datetime import timedelta
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from haystack.views import SearchView
import json

ITEM_BY_PAGINATION = 9


class TaskSearchView(SearchView):
    def extra_context(self):
        return {'results': self.results, 'filter': "creating"}


class TaskView(generic.ListView):
    template_name = "base.html"
    context_object_name = "tasks"
    paginate_by = ITEM_BY_PAGINATION

    def get_queryset(self):
        filter = self.kwargs['filter']
        if not check_filter(filter):
            raise Http404
        return Task.objects.filter(user=self.request.user)\
            .order_by(*filter_args(filter))[:ITEM_BY_PAGINATION]

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        filter = self.kwargs['filter']
        if filter is None:
            filter = "creating"
        context['filter'] = filter
        return context


@login_required
def create_task(request, filter):
    name = request.POST.get('name', 'No name')
    description = request.POST.get('description', None)
    task = Task(user=request.user, name=name, description=description)
    task.save()
    print(filter, "create_task")
    return redirect("task:task", filter=filter)


@login_required
def remove_task(request, pk, filter):
    task = Task.objects.get(user=request.user, pk=pk)
    task.delete()
    return redirect("task:task", filter=filter)


@login_required
def edit_task(request, pk, filter):
    task = Task.objects.get(user=request.user, pk=pk)
    tasks = Task.objects.filter(user=request.user) \
        .order_by(*filter_args(filter))[:ITEM_BY_PAGINATION]
    if request.method == 'POST':
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        task.name = name
        task.description = description
        task.save()
        return redirect("task:task", filter=filter)
    return render(request, "task/edit_task.html", {
        'task': task,
        'tasks': tasks,
        'filter': filter
    })


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
    filter = request.GET.get('filter', None)
    offset = int(offset)
    end = offset + ITEM_BY_PAGINATION
    data = []
    if end <= Task.objects.filter(user=request.user).count() \
            + ITEM_BY_PAGINATION:
        tasks = None
        end = calculate_end(request.user, filter, end)
        tasks = Task.objects.filter(user=request.user)\
            .order_by(*filter_args(filter))[offset:end]

        for task in tasks:
            data.append({
                'pk': task.pk,
                'name': task.name,
                'description': task.description,
                'timer': task.timer.total_seconds(),
                'created': str(task.created),
                'finished': str(task.finished),
                'done': str(task.done),
                'filter': filter
            })

    return HttpResponse(json.dumps(data), content_type='application/json')


def calculate_end(user, filter, end):
    count = Task.objects.filter(user=user) \
        .order_by(*filter_args(filter)).count()
    if end > count:
        end = count
    return end


def filter_args(filter):
    if filter == "spend":
        return ("-timer", "name")
    elif filter == "name":
        return ("name", "-timer")
    elif filter == "done":
        return ("-created", "name")
    else:
        return ("-created", "name")


def check_filter(filter):
    if filter == "spend" or filter == "name" or filter == "done" \
            or filter == "creating" or filter is None:
        return True
    return False
