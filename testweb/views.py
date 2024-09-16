from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.urls import reverse

def redirect_home(request):
    return redirect('home', username=request.user.username)

def home_view(request, username):
    return render(request, 'home/index.html', {'username': username})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        username = self.request.user.username
        return reverse('home', kwargs={'username': username})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('home', username=user.username)
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def default_page(request):
    return render(request, 'default_page.html')