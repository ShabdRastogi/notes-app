from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 
from django.shortcuts import get_list_or_404 
from main.models import Notes
from .serializers import NotesSerializer 


@api_view(['GET'])
def get_notes(request):
  notes =Notes.objects.all()
  serializer = NotesSerializer(notes,many=True)
  return Response(serializer.data)


@api_view(['POST'])
def create_notes(request):
  serializer = NotesSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data,status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





