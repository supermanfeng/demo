from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

from user.forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
        else:
            return render(request, 'register.html', {'error': form.errors})
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html', {})


def user_info(request):
    return render(request, 'user_info.html', {})


def logout(request):
    return render(request, 'logout.html', {})
