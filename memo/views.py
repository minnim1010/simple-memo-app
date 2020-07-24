from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import serializers, generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.views import AlreadyLogoutAccess, IsOwnerOrReadOnly
from memo.models import Memo


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = '__all__'

@permission_classes((IsAuthenticated, AlreadyLogoutAccess))
class ListMemo(generics.ListCreateAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer

    def create(self, request, *args, **kwargs):
        serializer = MemoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['author'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@permission_classes((IsAuthenticated, IsOwnerOrReadOnly, AlreadyLogoutAccess))
class DetailMemo(generics.RetrieveUpdateDestroyAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer