from django.urls import path 
from . import views

urlpatterns = [
  path('notes/',views.get_notes,name='get-notes'),
  path('notes/create/',views.create_notes,name='create-notes'),
  path('notes/<int:id>/',views.get_note,name='get-note'),
  path('notes/update/<int:id>/',views.update_note,name='update-note'),
  path('notes/delete/<int:id>/',views.delete_note,name='delete-note'),
]