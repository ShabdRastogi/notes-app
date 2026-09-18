from django.urls import path 
from . import views

urlpatterns = [
  path('notes/',views.get_notes,name='get-notes'),
  path('notes/create/',views.create_notes,name='create-notes'),
]