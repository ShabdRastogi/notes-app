from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from main.models import Notes, EmailVerificationOTP, PasswordResetOTP
from .serializers import NotesSerializer, RegisterSerializer, VerifyOTPSerializer, ResetPasswordSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView 
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample
import random
from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.cache import cache

class LoginSerializer(TokenObtainPairSerializer):
	pass


@extend_schema_view(
	post=extend_schema(
		request=LoginSerializer,
		examples=[
			OpenApiExample(
				'Login Example',
				value={
					'username': 'Test_user',
					'password': 'Test@123'
				},
				request_only=True
			)
		]
	)
)
class LoginApi(TokenObtainPairView):
  throttle_scope = 'login'
  serializer_class = LoginSerializer

@extend_schema(
  summary='Get all notes',
  description="Returns all notes belonging to the authenticated user.",
  responses={
    200: NotesSerializer(many=True),
    401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.')
  }
)
class GetNotesApi(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    cache_key = f"notes:user:{request.user.id}"
    cached_notes = cache.get(cache_key)
    if cached_notes is not None:
      return Response(cached_notes)
    notes = Notes.objects.filter(user=request.user)
    serializer = NotesSerializer(notes, many=True)
    cache.set(cache_key, serializer.data, timeout=300)
    return Response(serializer.data)


@extend_schema(
  summary='Create a note',
  description='Creates a note for the authenticated user',
  request=NotesSerializer,
	examples=[
		OpenApiExample(
			'Create Note Example',
			value={
				'title': 'Django REST Framework',
				'description': 'Learning APIView and JWT authentication.'
			},
			request_only=True
		)
	],
  responses={
    201: NotesSerializer,
    400: OpenApiResponse(description='Invalid note data'),
    401: OpenApiResponse(description='Authentication required'),
  }
)
class CreateNotesApi(APIView):
  permission_classes = [IsAuthenticated]

  def post(self,request):
    serializer = NotesSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      cache.delete(f"notes:user:{request.user.id}")
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
  summary="Get a single note",
  description="Returns a specific note belonging to the authenticated user.",
  responses={
    200: NotesSerializer,
    401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
    404: OpenApiResponse(description="Note not found."),
  },
)
class GetNoteApi(APIView):
  permission_classes = [IsAuthenticated]

  def get(self,request,id):
    note = get_object_or_404(Notes,id=id,user=request.user)
    serializer = NotesSerializer(note)
    return Response(serializer.data)


@extend_schema(
  summary="Update a note",
  description="Partially updates a specific note belonging to the authenticated user.",
  request=NotesSerializer,
	examples=[
		OpenApiExample(
			'Update Note Example',
			value={
				'title': 'Django REST Framework Updated',
				'description': 'Updated notes about APIView and JWT authentication.'
			},
			request_only=True
		)
	],
  responses={
    200: NotesSerializer,
    400: OpenApiResponse(description="Invalid note data."),
    401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
    404: OpenApiResponse(description="Note not found."),
  },
)
class UpdateNoteApi(APIView):
  permission_classes = [IsAuthenticated]

  def patch(self,request,id):
    note = get_object_or_404(Notes,id=id,user=request.user)
    serializer = NotesSerializer(note,data=request.data,partial=True)
    if serializer.is_valid():
      serializer.save()
      cache.delete(f"notes:user:{request.user.id}")
      return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
  responses={
    204: {'description': 'Note deleted successfully'},
    401: {'description': 'Authentication required'},
    404: {'description': 'Note not found'},
  }
)
class DeleteNoteApi(APIView):
  permission_classes = [IsAuthenticated]

  def delete(self, request, id):
    note = get_object_or_404(Notes,id=id,user=request.user)
    note.delete()
    cache.delete(f"notes:user:{request.user.id}")
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
	request=RegisterSerializer,
	examples=[
		OpenApiExample(
			'Register Example',
			value={
				'username': 'Test_user',
				'email': 'testuser@example.com',
				'password': 'Test@123'
			},
			request_only=True
		)
	],
	responses={
    201: OpenApiResponse(description="User registered successfully"),
    400: OpenApiResponse(description="Invalid registration data"),
  }
)
class RegisterApi(APIView):

  def post(self,request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      user.is_active = False
      user.save()

      otp = str(random.randint(100000, 999999))
      cache_key = f"otp:email_verification:{user.email}"
      cache.set(cache_key,otp,timeout=300)

      send_mail(
        'Email Verification OTP',
        f'''
Hello {user.username},
Your email verification OTP is:
{otp}
This OTP is valid for 5 minutes.
If you did not create this account, please ignore this email.
''',
        None,
        [user.email],
        fail_silently=False
      )

      return Response(
        {'message':'OTP sent to the mail'},
        status=status.HTTP_201_CREATED
      )

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
  summary="Verify email",
  description="Verifies the user's email using the OTP sent during registration.",
  request={
    'application/json': {
      'type': 'object',
      'properties': {
        'email': {
          'type': 'string',
          'format': 'email'
        },
        'otp': {
          'type': 'string',
          'example': '123456'
        },
      },
      'required': ['email','otp'],
    }
  },
	examples=[
		OpenApiExample(
			'Verify Email Example',
			value={
				'email': 'testuser@example.com',
				'otp': '123456'
			},
			request_only=True
		)
	],
	responses={
    200: OpenApiResponse(
      description="Email verified successfully."
    ),
    400: OpenApiResponse(
      description="Invalid or expired OTP."
    ),
    404: OpenApiResponse(
      description="User not found."
    ),
  },
)
class VerifyEmailApi(APIView):

  def post(self,request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    if not email or not otp:
      return Response(
        {'error':'Email and OTP are required.'},
        status=status.HTTP_400_BAD_REQUEST
      )
    try:
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      return Response({'error': 'User not found.'},status=status.HTTP_404_NOT_FOUND)

    cache_key = f"otp:email_verification:{email}"
    stored_otp = cache.get(cache_key)

    if stored_otp is None:
      return Response(
        {'error': 'OTP has expired or does not exist.'},
        status=status.HTTP_400_BAD_REQUEST
      )

    if stored_otp != otp:
      return Response(
        {'error': 'Invalid OTP.'},
        status=status.HTTP_400_BAD_REQUEST
      )

    user.is_active = True
    user.save()

    cache.delete(cache_key)

    return Response(
        {'message': 'Email verified successfully.'},
        status=status.HTTP_200_OK
    )


@extend_schema(
  summary="Logout user",
  description=(
    "Logs out the authenticated user by blacklisting "
    "the provided refresh token."
  ),
  request={
    'application/json': {
      'type': 'object',
      'properties': {
        'refresh': {
          'type': 'string',
          'description': 'JWT refresh token.'
        }
      },
      'required': ['refresh'],
    }
  },
	examples=[
		OpenApiExample(
			'Logout Example',
			value={
				'refresh': 'your_refresh_token'
			},
			request_only=True
		)
	],
	responses={
    205: OpenApiResponse(
      description="Successfully logged out."
    ),
    400: OpenApiResponse(
      description="Invalid or missing refresh token."
    ),
    401: OpenApiResponse(
      description="Authentication credentials were not provided or are invalid."
    ),
  },
)
class LogoutApi(APIView):
  permission_classes = [IsAuthenticated]

  def post(self,request):
    try:
      refresh_token = request.data["refresh"]
      token = RefreshToken(refresh_token)
      token.blacklist()

      return Response(
        {'message':"Successfully Logged out"},
        status=status.HTTP_205_RESET_CONTENT
      )

    except:
      return Response(
        {'error':'Invalid refresh token'},
        status=status.HTTP_400_BAD_REQUEST
      )


@extend_schema(
  summary="Verify password reset OTP",
  description="Verifies the OTP sent to the user's email for password reset.",
  request=VerifyOTPSerializer,
	examples=[
		OpenApiExample(
			'Verify OTP Example',
			value={
				'email': 'testuser@example.com',
				'otp': '123456'
			},
			request_only=True
		)
	],
	responses={
    200: OpenApiResponse(
      description="OTP verified successfully"
    ),
    400: OpenApiResponse(
      description="Invalid email, invalid OTP, or expired OTP"
    ),
  }
)
class VerifyOTPApi(APIView):
  throttle_scope = 'otp'

  def post(self, request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    if not email or not otp:
      return Response(
      {'error': 'Email and OTP are required.'},
      status=status.HTTP_400_BAD_REQUEST
    )

    try:
      user = User.objects.get(email=email)

    except User.DoesNotExist:
      return Response(
        {'error': 'Invalid email.'},
        status=status.HTTP_400_BAD_REQUEST
      )

    cache_key = f"otp:password_reset:{email}"

    stored_otp = cache.get(cache_key)

    if stored_otp is None:
      return Response(
        {'error': 'OTP has expired or does not exist.'},
        status=status.HTTP_400_BAD_REQUEST
      )

    if stored_otp != otp:
      return Response(
        {'error': 'Invalid OTP.'},
        status=status.HTTP_400_BAD_REQUEST
      )

    verified_key = f"otp:password_reset_verified:{email}"

    cache.set(
      verified_key,
      True,
      timeout=300
    )

    cache.delete(cache_key)

    return Response(
      {'message': 'OTP verified successfully.'},
      status=status.HTTP_200_OK
    )


@extend_schema(
  summary="Forgot password",
  description="Sends a password reset OTP to the user's registered email.",
  request={
    'application/json': {
      'type': 'object',
      'properties': {
        'email': {
          'type': 'string',
          'format': 'email'
        }
      },
      'required': ['email'],
    }
  },
	examples=[
		OpenApiExample(
			'Forgot Password Example',
			value={
				'email': 'testuser@example.com'
			},
			request_only=True
		)
	],
	responses={
    200: OpenApiResponse(
      description="OTP sent successfully."
    ),
    404: OpenApiResponse(
      description="User not found."
    ),
  }
)
class ForgotPasswordApi(APIView):
  throttle_scope = 'password_reset'
  def post(self,request):
    email = request.data.get('email')

    if not email:
      return Response(
        {'error':'Email is required.'},
        status=status.HTTP_400_BAD_REQUEST
      )

    try:
      user = User.objects.get(email=email)

    except User.DoesNotExist:
      return Response(
        {'error':'User not found.'},
        status=status.HTTP_404_NOT_FOUND
      )

    otp = str(random.randint(100000, 999999))

    cache_key = f"otp:password_reset:{user.email}"
    cache.set(cache_key,otp,timeout=300)

    send_mail(
      'Password Reset OTP',
      f'''
Hello {user.username},

Your password reset OTP is:

{otp}

This OTP is valid for 5 minutes.

If you did not request a password reset, please ignore this email.
''',
      None,
      [user.email],
      fail_silently=False
    )

    return Response(
      {'message':'OTP sent to the mail'},
      status=status.HTTP_200_OK
    )


@extend_schema(
  summary="Reset password",
  description="Resets the user's password after successful OTP verification.",
  request=ResetPasswordSerializer,
	examples=[
		OpenApiExample(
			'Reset Password Example',
			value={
				'email': 'testuser@example.com',
				'new_password': 'NewPass@123'
			},
			request_only=True
		)
	],
	responses={
    200: OpenApiResponse(
      description="Password reset successfully."
    ),
    400: OpenApiResponse(
      description="OTP has not been verified or password reset is not allowed."
    ),
    404: OpenApiResponse(
      description="User not found."
    ),
  }
)
class ResetPasswordApi(APIView):

  def post(self, request):
    serializer = ResetPasswordSerializer(data=request.data)

    if not serializer.is_valid():
      return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
      )

    email = serializer.validated_data['email']
    new_password = serializer.validated_data['new_password']

    try:
      user = User.objects.get(email=email)

    except User.DoesNotExist:
      return Response(
        {'error': 'User not found.'},
        status=status.HTTP_404_NOT_FOUND
      )

    verified_key = f"otp:password_reset_verified:{email}"
    verified = cache.get(verified_key)
    if not verified:
      return Response(
        {'error': 'OTP has not been verified or verification has expired.'},
        status=status.HTTP_400_BAD_REQUEST
      )

    user.set_password(new_password)
    user.save()

    cache.delete(verified_key)

    return Response(
      {'message': 'Password reset successfully.'},
      status=status.HTTP_200_OK
    )