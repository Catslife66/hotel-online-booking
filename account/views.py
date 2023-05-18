from django.conf import settings
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        next_url = request.POST.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect('/')

    context = {'form': form}
    return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You have logged out.')
    return redirect('account:login')


def register_view(request):
    User = get_user_model()

    class AccountUserCreationForm(UserCreationForm):
        class Meta(UserCreationForm.Meta):
            model = User

    if request.method == 'POST':
        form =AccountUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = AccountUserCreationForm()
    context = {'form': form}
    return render(request, 'account/register.html', context)

