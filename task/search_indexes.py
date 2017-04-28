from haystack import indexes
from .models import Task


class TaskIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')

    def get_model(self):
        return Task

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
