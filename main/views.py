from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from . forms import RegisterForm
from django.contrib.auth import login

def main(request):
  return render(request,'main.html') 

def register_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    if password != confirm_password:
      return render(
        request,
        'register.html',
        {'error': 'Passwords do not match'}
      )
    if User.objects.filter(username=username).exists():
      return render(
        request,
        'register.html',
        {'error': 'Username already exists'}
      )

    user = User.objects.create_user(
      username=username,
      password=password
    )

    login(request,user)
    return redirect('main')

  return render(request,'register.html')

def login_view(request):
  return render(request,'login.html')
