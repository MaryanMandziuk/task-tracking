# from django.forms import ModelForm, Textarea, TextInput
# from .models import Task
#
#
# class TaskForm(ModelForm):
#     class Meta:
#         model = Task
#         fields = ('name', 'description')
#         widgets = {
#             'name': TextInput(attrs={
#                 'class': 'mdl-textfield__input',
#                 'style': 'color: white;',
#                 'id': 'name',
#                 'type': 'text',
#                 'name': 'name'
#                 }),
#             'description': Textarea(attrs={
#                 'class': 'mdl-textfield__input',
#                 'style': 'color: white;',
#                 'id': 'description',
#                 'type': 'text',
#                 'name': 'description',
#                 'rows': '3',
#                 'maxrows': '6'
#             })
#         }
