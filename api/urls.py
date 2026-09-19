from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

urlpatterns = [
  path('register/',views.RegisterApi.as_view(),name='api_register'),
  path('login/',views.LoginApi.as_view(),name='api_login'),
  path('token/refresh/',TokenRefreshView.as_view(),name='token-refresh'),
  path('notes/',views.GetNotesApi.as_view(),name='get-notes'),
  path('notes/create/',views.CreateNotesApi.as_view(),name='create-notes'),
  path('notes/<int:id>/',views.GetNoteApi.as_view(),name='get-note'),
  path('notes/update/<int:id>/',views.UpdateNoteApi.as_view(),name='update-note'),
  path('notes/delete/<int:id>/',views.DeleteNoteApi.as_view(),name='delete-note'),
  path('logout/',views.LogoutApi.as_view(),name='api_logout'),
  path('forgot-password/',views.ForgotPasswordApi.as_view(),name='forgot-password'),
  path('verify-otp/',views.VerifyOTPApi.as_view(),name='verify-otp'),
  path('reset-password/',views.ResetPasswordApi.as_view(),name='reset-password'),
  path('verify-email/',views.VerifyEmailApi.as_view(),name='verify-email'),
]
