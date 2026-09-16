from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate

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

    return redirect('login')

  return render(request,'register.html')

def login_view(request):
  if request.method=='POST':
    username=request.POST['username']
    password=request.POST['password']

    user = authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect('main')
    
  return render(request,'login.html',{'error': 'Invalid username or password'})
