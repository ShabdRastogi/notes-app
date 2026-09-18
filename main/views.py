from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import Notes
import re
from django.contrib import messages

def main(request):
    if not request.user.is_authenticated:
      return redirect('login')
    return render(request,'main.html')

def register_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    username_pattern = r'^[a-zA-Z0-9_-]{3,16}$'
    if not re.match(username_pattern,username):
      return render(request,'register.html',{
        'error':'Username must be 3 to 16 characters and use only letters, numbers, _ or -.'
      })

    password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@$!%*?&])[A-Za-z0-9@$!%*?&]{8,}$'
    if not re.match(password_pattern,password):
      return render(request,'register.html',{
        "error":'Password must have 8+ characters, one uppercase letter, and one special symbol.'
      })
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

    messages.success(request,'Registration successful!')

    return redirect('login')

  return render(request,'register.html')

def login_view(request):
  if request.method=='POST':
    username=request.POST['username']
    password=request.POST['password']

    user = authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      messages.success(request,'Login successful!')
      return redirect('main')
    return render(request,'login.html',{'error': 'Invalid username or password'}) 
    
  return render(request,'login.html')

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request,'logout.html')
@login_required
def notes_view(request):
  notes=Notes.objects.filter(user=request.user)
  return render(request,'main.html',{'notes':notes})

@login_required
def create_note(request):
  if request.method == 'POST':
    title = request.POST['title']
    description = request.POST['description']
    image=request.FILES.get('image')
    Notes.objects.create(user=request.user,title=title,description=description,image=image)

    return redirect('notes')
  return render(request,'create_note.html')

@login_required
def edit_note(request,id):
  note=Notes.objects.get(id=id,user=request.user)
  if request.method == 'POST':
    note.title=request.POST['title']
    note.description=request.POST['description']
    image=request.FILES.get('image')
    if image:
      if note.image:
        note.image.delete(save=False)
      note.image=image
    note.save()
    return redirect('notes')
  return render(request,'edit_note.html',{'note':note})


@login_required
def delete_note(request,id):
  note=Notes.objects.get(id=id,user=request.user)
  if request.method == 'POST':
    note.delete()
    return redirect('notes')

  return render(request,'delete_note.html',{'note':note})

@login_required
def delete_image(request,id):
  note=Notes.objects.get(id=id,user=request.user)
  if request.method == 'POST' and note.image:
    note.image.delete(save=False)
    note.image=None
    note.save()
  return redirect('edit_note',id=id)