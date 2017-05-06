from django.http import Http404
from .models import Task


def correct_boundary(user, filter, end):
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


# def check_filter(filter):
#     if filter == "spend" or filter == "name" or filter == "done" \
#             or filter == "creating":
#         return filter
#     elif filter is None:
#         return "creating"
#     else:
#         raise Http404
