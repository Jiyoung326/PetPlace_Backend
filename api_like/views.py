from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LikeSerializer
from rest_framework import status
from .models import Like

# filter
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

class LikeQuerySet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self, query):
        queryset = super().get_queryset()
        queryset = queryset.filter(b_id=query, state='정상')
        return queryset

# Create your views here.

class LikeView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('b_id') is None:
            return Response('b_id is required', status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.GET.get('user_id') is None:
                return Response('user_id is required', status=status.HTTP_400_BAD_REQUEST)
            else:
                user_id = request.GET.get('user_id')
                b_id = kwargs.get('b_id')
                like_queryset = LikeQuerySet().get_queryset(b_id)
                try:
                    like_queryset.get(user_id=user_id)
                    user_like = True
                except:
                    user_like = False
                return Response({'count':like_queryset.count(),
                    'user_like':user_like}, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.data.get('user_id')
        b_id = request.data.get('b_id')
        try:
            like_obj = Like.objects.get(user_id=user_id, b_id=b_id)
            like_serializer = LikeSerializer(like_obj, data=request.data)
        except:
            like_serializer = LikeSerializer(data=request.data)
        if like_serializer.is_valid():
            like_serializer.save()
            return Response({'result': 'success', 'data':like_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'result':'fail', 'data':like_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
