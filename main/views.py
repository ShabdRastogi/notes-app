from django.shortcuts import render,HttpResponse

# Create your views here.

def main(request):
  return render(request,'main.html') 

def register(request):
  return render(request,'register.html') 

def login(request):
  return render(request,'login.html')
