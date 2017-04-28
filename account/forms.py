from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    use_required_attribute = False
    password1 = forms.CharField(min_length=8,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'mdl-textfield__input',
                                    'style': 'color: white;',
                                    'id': 'password1',
                                    'for': 'password1'
                                    }))
    password2 = forms.CharField(min_length=8,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'mdl-textfield__input',
                                    'style': 'color: white;',
                                    'id': 'password2',
                                    'for': 'password2'
                                    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mdl-textfield__input',
        'style': 'color: white;',
        'id': 'email',
        'type': 'email',
    }))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']


class MaterialLoginForm(forms.Form):
    use_required_attribute = False
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mdl-textfield__input',
        'style': 'color: white;',
        'id': 'email',
        'type': 'email',
    }))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'mdl-textfield__input',
        'style': 'color: white;',
        'id': 'password',
        'for': 'password'
    }))


class EmailForm(PasswordResetForm):
    use_required_attribute = False
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mdl-textfield__input',
        'style': 'color: white;',
        'id': 'email',
        'type': 'email',
    }))


class PasswordForm(SetPasswordForm):
    use_required_attribute = False
    new_password1 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'mdl-textfield__input',
            'style': 'color: white;',
            'id': 'new_password1',
            'for': 'new_password1'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'mdl-textfield__input',
            'style': 'color: white;',
            'id': 'new_password2',
            'for': 'new_password2'
        }),
    )
