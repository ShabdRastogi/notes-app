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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes(request):
  notes =Notes.objects.filter(user=request.user)
  serializer = NotesSerializer(notes,many=True)
  return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_notes(request):
  serializer = NotesSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save(user=request.user)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note(request,id):
  note = get_object_or_404(Notes,id=id,user=request.user)
  serializer = NotesSerializer(note)
  return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_note(request,id):
  note= get_object_or_404(Notes,id=id, user=request.user)
  serializer = NotesSerializer(note,data=request.data,partial=True)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_note(request,id):
  note =get_object_or_404(Notes,id=id,user=request.user)
  note.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def register(request):
  serializer = RegisterSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(
      {'message':'User registered successfully'},
      status=status.HTTP_201_CREATED)
  
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
