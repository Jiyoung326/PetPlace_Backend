from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from .serializers import PhotoAllSerializer
from .serializers import PhotoDetailSerializer
from .serializers import PhotoMySerializer
from api_user.serializers import UserSerializer
from .models import PhotoBoard
from api_user.models import User

# filter
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

class PhotoQuerySet(ModelViewSet):
    queryset = PhotoBoard.objects.all()
    serializer_class = PhotoAllSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(state='정상')
        return queryset

class MyPhotoQuerySet(ModelViewSet):
    queryset = PhotoBoard.objects.all()
    serializer_class = PhotoMySerializer

    def get_queryset(self,user_id):
        queryset = super().get_queryset()
        queryset = queryset.filter(state='정상',user_id=user_id)
        return queryset

# Create your views here.

class PhotoView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('b_id') is None:
            if request.GET.get('user_id') is None:
                page = int(request.GET.get('page'))
                photo_queryset = PhotoQuerySet().get_queryset()[(page-1)*15:page*15]
                photo_all_serializer = PhotoAllSerializer(photo_queryset, many=True)
                return Response({'count':photo_queryset.count(),
                    'photos':photo_all_serializer.data}, status=status.HTTP_200_OK)
            else:#내 글 목록용
                user_id = request.GET.get('user_id')
                photo_queryset = MyPhotoQuerySet().get_queryset(user_id=user_id)
                photo_serializer = PhotoMySerializer(photo_queryset,many=True)
                return Response({'count':photo_queryset.count(),
                        'photos':photo_serializer.data}, status=status.HTTP_200_OK)
        else:
            b_id = kwargs.get('b_id')
            photo_detail_serializer = PhotoDetailSerializer(PhotoBoard.objects.get(b_id=b_id))
            user_id = photo_detail_serializer.data.get('user_id')
            user_serializer = UserSerializer(User.objects.get(user_id=user_id))
            nickname = {'nickname':user_serializer.data.get('nickname')}
            return Response(dict(photo_detail_serializer.data, **nickname), status=status.HTTP_200_OK)
            


    def post(self, request):
        photo_write_serializer = PhotoDetailSerializer(data=request.data)
        if photo_write_serializer.is_valid():
            photo_write_serializer.save()
            return Response({'result': 'success', 'data':photo_write_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'result':'fail', 'data':photo_write_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if request.data.get('b_id') is None:
            return Response('b_id is required', ststus=status.HTTP_400_BAD_REQUEST)
        else:
            b_id = request.data.get('b_id')
            photo_obj = PhotoBoard.objects.get(b_id=b_id)
            photo_obj.title = request.data.get('title')
            photo_obj.content = request.data.get('content')
            if request.data.get('image') is not None:
                image = request.data.get('image')
                photo_obj.image = image
            photo_obj.update_date = request.data.get('update_date')
            photo_obj.save()
            return Response({
                'result':'success'
            }, status=status.HTTP_200_OK)

    def delete(self, request):
        if request.data.get('b_id') is None:
            return Response('b_id is required', ststus=status.HTTP_400_BAD_REQUEST)
        else:
            b_id = request.data.get('b_id')
            photo_obj = PhotoBoard.objects.get(b_id=b_id)
            photo_obj.update_date = request.data.get('update_date')
            photo_obj.state = request.data.get('state')
            photo_obj.save()
            return Response({
                'result':'success'
            }, status=status.HTTP_200_OK)