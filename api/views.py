from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from dashboard.models import *
from dashboard.forms import *

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def domains(request):
  if request.method == 'GET':
    profile = request.user.profile
    # Get all domains list
    domains = Domain.objects.all().filter(owner=profile)
    # Serialize JSON data
    serializer = DomainSerializer(domains, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    # Request user profile since we need to get all domain from that User
    profile = request.user.profile
    # Put all POST data into variable
    data = request.data
    # Get which category id that need to be used
    cat = Category.objects.get(id=data['cat_id'])
    # Get all domain list
    tempdomain_list = profile.domain_set.all()
    # Put POST data into temporary variable
    tempdomain_data = data['domain']
    # Declare domainstatus to be added into Domain Model
    domainstatus = False
    # Checking is it POST data is inside tempdomain_list
    for x in tempdomain_list:
      if tempdomain_data in x.domain:
        try:
          item = Domain.objects.get(id=x.id)
          if item.freq < int(data['freq']): # Check if any changes
            # item.freq = item.freq + int(data['freq']) # Should not added because it will create redudancy
            item.freq = int(data['freq'])
            item.save()
            domainstatus = True
            break
          else:
            domainstatus = True
            break
        except TypeError:
          print(tempdomain_data) 
    # If is not inside tempdomain_list then Create new domain into Domain Model
    if domainstatus == False:
      domain = Domain.objects.create(
        owner = profile,
        domain = data['domain'],
        freq = data['freq'],
        cat_id = cat
      )
      domain.save()
    
    serializer = DomainSerializer(data=request.data)
    # Checking POST data is CREATED or BAD REQUEST
    if serializer.is_valid():
        # serializer.save() # not applicable since we do not create new POST data from serializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCategory(request):
  # Get all category list
  category = Category.objects.all()
  # Serialize JSON data
  serializer = CategorySerializer(category, many=True)
  return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whitelist(request):
  """
  List all whitelist, or create a new whitelist
  """
  if request.method == 'GET':
    # Request user profile since we need to get all whitelist from that User
    profile = request.user.profile
    # Get all whitelist domain from the USER
    domain_whitelist = profile.whitelist_set.all()
    # domain_whitelist = Whitelist.objects.all()
    # Serialize JSON data
    serializer = WhitelistSerializer(domain_whitelist, many=True)
    return Response(serializer.data)
  
  elif request.method == 'POST':
    profile = request.user.profile
    data = request.data
    form_whitelist = WhitelistForm(instance=profile)
    form_whitelist = WhitelistForm(request.POST)
    if form_whitelist.is_valid():
      whitelist = form_whitelist.save(commit=False)
      whitelist.owner = profile
      whitelist.save()
      return Response(status=status.HTTP_201_CREATED)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBlacklist(request):
  # Request user profile since we need to get all blacklist from that User
  profile = request.user.profile
  # Get all blacklist domain from the USER
  domain_blacklist = profile.blacklist_set.all()
  # domain_blacklist = Blacklist.objects.all()
  # Serialize JSON data
  serializer = BlacklistSerializer(domain_blacklist, many=True)
  return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfileConfig(request):
  # Request user profile
  profile = request.user.profile
  settings = profileConfig.objects.all().filter(owner=profile)
  serializer = profileConfigSerializer(settings, many=True)
  return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def putWebFilter(request, pk):
  """Update webfilter status"""
  try:
    setting = profileConfig.objects.get(id=pk)
  except setting.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  serializer = profileConfigSerializer(setting, data=request.data)
  if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  