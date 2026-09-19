from django.urls import path 
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
  path('register/', views.register, name='api_register'),
  path('login/',TokenObtainPairView.as_view(),name='token-obtain-pair'),
  path('token/refresh/',TokenRefreshView.as_view(),name='token-refresh'),
  path('notes/',views.get_notes,name='get-notes'),
  path('notes/create/',views.create_notes,name='create-notes'),
  path('notes/<int:id>/',views.get_note,name='get-note'),
  path('notes/update/<int:id>/',views.update_note,name='update-note'),
  path('notes/delete/<int:id>/',views.delete_note,name='delete-note'),
  path('logout/',views.LogoutApi.as_view(),name='api_logout'),
]
