from django import forms
from haystack.forms import SearchForm


class MaterialSearchForm(SearchForm):
    q = forms.CharField(required=False, label=('Search'),
                        widget=forms.TextInput(attrs={
                        'type': 'search',
                        'class': 'mdl-textfield__input',
                        'name': 'q',
                        'id': 'id_q'
                        }))
