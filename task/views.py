from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import JsonResponse, HttpResponse, \
                        HttpResponseBadRequest, Http404
from datetime import timedelta
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from haystack.query import SearchQuerySet
from .utils import calculate_end, filter_args, check_filter
import json

ITEM_BY_PAGINATION = 9


class TaskView(generic.ListView):
    template_name = "task/task.html"
    context_object_name = "tasks"
    paginate_by = ITEM_BY_PAGINATION

    def get_queryset(self):
        filter = self.kwargs['filter']
        if not check_filter(filter):
            raise Http404
        if filter == "done":
            return Task.objects.filter(user=self.request.user, done=True)\
                .order_by(*filter_args(filter))[:ITEM_BY_PAGINATION]
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
    return redirect("task:task", filter=filter)


@login_required
def remove_task(request, pk, filter):
    task = get_object_or_404(Task, user=request.user, pk=pk)
    task.delete()
    return redirect("task:task", filter=filter)


@login_required
def edit_task(request, pk, filter):
    task = get_object_or_404(Task, user=request.user, pk=pk)
    if filter == "done":
        tasks = Task.objects.filter(user=request.user, done=True)\
            .order_by(*filter_args(filter))[:ITEM_BY_PAGINATION]
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
    task = get_object_or_404(Task, user=request.user, pk=id)
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


@login_required
def timer(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    id = request.GET.get('id', None)
    task = get_object_or_404(Task, user=request.user, pk=id)
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
    task = get_object_or_404(Task, user=request.user, pk=id)
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


@login_required
def search(request, query):
    if query == "":
        query = request.GET.get('q', "")
    sqs = SearchQuerySet().filter(author=request.user).auto_query(query)
    sqs = sqs.load_all()
    return render(request, "search/search.html", {
        "results": sqs, "query": query})


@login_required
def edit_search(request, pk, query):
    sqs = SearchQuerySet().filter(author=request.user).auto_query(query)
    sqs = sqs.load_all()
    task = get_object_or_404(Task, user=request.user, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        task.name = name
        task.description = description
        task.save()
        return redirect("task:search", query)

    return render(request, "search/edit.html", {
        "results": sqs, "query": query, "task": task})


@login_required
def remove_search(request, pk, query):
    task = get_object_or_404(Task, user=request.user, pk=pk)
    task.delete()
    return redirect("task:search", query=query)
