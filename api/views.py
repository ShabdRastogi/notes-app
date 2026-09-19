from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response 
from rest_framework import status 
from django.shortcuts import get_object_or_404 
from main.models import Notes
from .serializers import NotesSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
  summary='Get all notes',
  description="Returns all notes belonging to the authenticated user.",
  responses={
    200: NotesSerializer,
    401: OpenApiResponse(description = 'Authentication credentials were not provided or are invalid.')
  }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes(request):
  notes =Notes.objects.filter(user=request.user)
  serializer = NotesSerializer(notes,many=True)
  return Response(serializer.data)

@extend_schema(
  summary='Create a note',
  description='Creates a note for the authenticated user',
  request=NotesSerializer,
  responses={
    201: NotesSerializer,
    400: OpenApiResponse(description= 'Invalid note data'),
    401: OpenApiResponse(description= 'Authentication required'),
  }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_notes(request):
  serializer = NotesSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save(user=request.user)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
  summary="Get a single note",
  description="Returns a specific note belonging to the authenticated user.",
  responses={
    200: NotesSerializer,
    401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
    404: OpenApiResponse(description="Note not found."),
  },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note(request,id):
  note = get_object_or_404(Notes,id=id,user=request.user)
  serializer = NotesSerializer(note)
  return Response(serializer.data)

@extend_schema(
  summary="Update a note",
  description="Partially updates a specific note belonging to the authenticated user.",
  request=NotesSerializer,
  responses={
    200: NotesSerializer,
    400: OpenApiResponse(description="Invalid note data."),
    401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
    404: OpenApiResponse(description="Note not found."),
  },
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_note(request,id):
  note= get_object_or_404(Notes,id=id, user=request.user)
  serializer = NotesSerializer(note,data=request.data,partial=True)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
  responses={
    204: {'description': 'Note deleted successfully'},
    401: {'description': 'Authentication required'},
    404: {'description': 'Note not found'},
  }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_note(request,id):
  note =get_object_or_404(Notes,id=id,user=request.user)
  note.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
  request=RegisterSerializer,
  responses={
    201: OpenApiResponse(description="User registered successfully"),
    400: OpenApiResponse(description="Invalid registration data"),
  }
)
@api_view(['POST'])
def register(request):
  serializer = RegisterSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(
      {'message':'User registered successfully'},
      status=status.HTTP_201_CREATED)
  
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


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
  permission_classes =[IsAuthenticated]
  def post(self,request):
    try:
      refresh_token=request.data["refresh"]
      token=RefreshToken(refresh_token)
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