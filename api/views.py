from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from dashboard.models import *

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def domains(request):
  if request.method == 'GET':
    domains = Domain.objects.all()
    serializer = DomainSerializer(domains, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    user = request.user.profile
    data = request.data
    cat = Category.objects.get(id=data['cat_id'])
    domain = Domain.objects.create(
      owner=user,
      domain=data['domain'],
      freq = data['freq'],
      cat_id=cat
    )
    domain.save()
    serializer = DomainSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCategory(request):
  category = Category.objects.all()
  serializer = CategorySerializer(category, many=True)
  return Response(serializer.data)
