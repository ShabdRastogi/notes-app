from django.urls import path 
from . import views

urlpatterns =[
  path("",views.main,name='main'),
  path("register/",views.register_view,name='register'),
  path("login/",views.login_view,name='login'),
  path("notes/",views.notes_view,name='notes'),
  path("notes/create/",views.create_note,name='create_note'),
  path('logout/',views.logout_view,name='logout'),
  path("notes/edit/<int:note_number>/",views.edit_note,name='edit_note'),
  path("notes/delete/<int:note_number>",views.delete_note,name='delete_note'),
  path('delete-image/<int:note_number>/',views.delete_image,name='delete_image'),
]