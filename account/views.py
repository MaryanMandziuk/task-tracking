from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import MaterialLoginForm, UserRegistrationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User


def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                return render(request, 'account/register_failed.html', {
                              'email': email})
            new_user.username = form.cleaned_data['email']
            new_user.set_password(form.cleaned_data['password2'])
            new_user.save()
            return render(request, 'account/register_done.html', {
                                    'new_user': new_user})
        else:
            inccorect_input = "Incorrect inputs data, please put them \
                                carefully"
            return render(request, 'account/register.html', {'form': form,
                          "inccorect_input": inccorect_input})
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = MaterialLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'],
                                password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('task:task')
            else:
                error = 'Invalid login'
                return render(request,
                              'account/login.html',
                              {'form': form, 'error': error})

    else:
        form = MaterialLoginForm()
    return render(request, 'account/login.html', {'form': form})
