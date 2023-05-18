from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import RegisterForm
from .models import ConfirmationCode


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_staff:
                confirmation_code = ConfirmationCode.objects.get(user=user)

                if not confirmation_code.confirmed:
                    return render(request, 'email_notification.html')

            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': True, 'username': username})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'email_notification.html')
        else:
            return render(request, 'register.html', {'form': form})


def email_confirmation_view(request):
    confirmation_code = ConfirmationCode.objects.get(code=request.GET['confirmation_code'])
    confirmation_code.confirmed = True

    confirmation_code.save()

    user = User.objects.get(pk=confirmation_code.user.id)

    login(request, user)
    return redirect('/')
