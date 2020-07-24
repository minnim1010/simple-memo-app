from json import loads
from base64 import b64decode
import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import permission_classes, api_view
from rest_framework import permissions
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt import serializers as jwt_serializers

from memo.models import Memo

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user

class AlreadyLogoutRefresh(permissions.BasePermission):
    """
    Use logouted user's refresh token to get new access token
    always not allowed it
    """
    def has_permission(self, request, view):
        try:
            token = request.data['refresh']
        except:
            # refresh field is missing
            return False
        info = GetTokenInfo(token)
        token = cache.get(key=info['jti'])
        return token == None

class AlreadyLogoutAccess(permissions.BasePermission):
    """
    Use logouted user's refresh token to get new access token
    always not allowed it
    """
    def has_permission(self, request, view):
        try:
            token = request.META['HTTP_AUTHORIZATION']
        except:
            # access field is missing
            return False
        info = GetTokenInfo(token)
        token = cache.get(key=info['jti'])
        return token == None

def GetTokenInfo(token):
    """
    :param token: JWT token(access, refresh)
    :return: JSON data of token's body
    """
    infoString = b64decode((lambda s: s+(4-len(s)%4)%4*"=")(token.split('.')[1]))
    return loads(infoString)

def BlackListedToken(refresh):
    """
    :param refresh: refresh JWT token
    :return: blacklisted token
    """
    info = GetTokenInfo(refresh)
    timeout = datetime.datetime.fromtimestamp(int(info['exp'])) - datetime.datetime.now()
    token = cache.get_or_set(key=info['jti'], default=refresh, timeout=timeout.seconds)
    return token

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def Logout(request):
    try:
        access = request.META['HTTP_AUTHORIZATION']
        refresh = request.data['refresh']
    except:
        content = {
            'status' : 'refresh or access token is missing'
        }
        return Response(content)
    BlackListedToken(refresh)
    BlackListedToken(access)
    content = {
        'status': 'request was permitted'
    }
    return Response(content)

@api_view(['GET', 'POST'])
def Login(request):
    pass

class TokenRefreshView(TokenViewBase):
    permission_classes = (AlreadyLogoutRefresh, )
    serializer_class = jwt_serializers.TokenRefreshSerializer
