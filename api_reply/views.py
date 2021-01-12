from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from .serializers import ReplySerializer
from api_user.serializers import UserSerializer
from .models import Reply
from api_user.models import User

# filter
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

class ReplyQuerySet(ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_queryset(self, query):
        queryset = super().get_queryset()
        queryset = queryset.filter(b_id=query, state='정상')
        return queryset

class MyReplyQuerySet(ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_queryset(self, user_id):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=user_id, state='정상')
        return queryset


# Create your views here.

class ReplyView(APIView):
    def post(self, request):
        reply_serializer = ReplySerializer(data=request.data)
        if reply_serializer.is_valid():
            reply_serializer.save()
            user_id = reply_serializer.data.get('user_id')
            user_serializer = UserSerializer(User.objects.get(user_id=user_id))
            nickname = {'nickname':user_serializer.data.get('nickname')}
            return Response({'result': 'success', 'data':dict(reply_serializer.data, **nickname)},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'result':'fail', 'data':reply_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, **kwargs):
        if kwargs.get('b_id') is None:
            if request.GET.get('user_id') is None:
                return Response('b_id is required', status=status.HTTP_400_BAD_REQUEST)
            else:#나의 댓글 가져오기
                user_id = request.GET.get('user_id')
                myreply_queryset = MyReplyQuerySet().get_queryset(user_id)
                reply_serializer = ReplySerializer(myreply_queryset,many=True)
                return Response({'count':myreply_queryset.count(),
                        'replies':reply_serializer.data}, status=status.HTTP_200_OK)

        else:
            b_id = kwargs.get('b_id')
            reply_queryset = ReplyQuerySet().get_queryset(b_id)
            reply_serializer = ReplySerializer(reply_queryset, many=True)
            for reply in reply_serializer.data:
                user_id = reply.get('user_id')
                user_serializer = UserSerializer(User.objects.get(user_id=user_id))
                #reply['nickname'] = user_serializer.data.get('nickname')
                nickname = {'nickname':user_serializer.data.get('nickname')}
                reply.update(nickname)
            return Response({'count':reply_queryset.count(),
                'replies':reply_serializer.data}, status=status.HTTP_200_OK)

    def put(self, request):
        if request.data.get('r_id') is None:
            return Response('r_id is required', ststus=status.HTTP_400_BAD_REQUEST)
        else:
            r_id = request.data.get('r_id')
            reply_obj = Reply.objects.get(r_id=r_id)
            reply_obj.content = request.data.get('content')
            reply_obj.update_date = request.data.get('update_date')
            reply_obj.save()
            return Response({
                'result':'success',
                'content':reply_obj.content
            }, status=status.HTTP_200_OK)

    def delete(self, request):
        if request.data.get('r_id') is None:
            return Response('r_id is required', ststus=status.HTTP_400_BAD_REQUEST)
        else:
            r_id = request.data.get('r_id')
            reply_obj = Reply.objects.get(r_id=r_id)
            reply_obj.update_date = request.data.get('update_date')
            reply_obj.state = request.data.get('state')
            reply_obj.save()
            return Response({
                'result':'success'
            }, status=status.HTTP_200_OK)
