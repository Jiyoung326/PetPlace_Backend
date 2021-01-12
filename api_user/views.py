from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User

# Create your views here.
class UserView(APIView):
    def get(self, request):
        if request.GET.get('user_id') is None and request.GET.get('nickname') is None:
            return Response('user_id or nickname is required', status=status.HTTP_400_BAD_REQUEST)
        elif request.GET.get('user_id') is not None and request.GET.get('nickname') is None:
            user_id = request.GET.get('user_id')
            user_serializer = UserSerializer(User.objects.get(user_id=user_id))
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        elif request.GET.get('user_id') is None and request.GET.get('nickname') is not None:
            nickname = request.GET.get('nickname')
            try:
                user_serializer = UserSerializer(User.objects.get(nickname=nickname))
                nick_exist = True
            except:
                nick_exist = False
            return Response({'nick_exist':nick_exist}, status=status.HTTP_200_OK)
        else:
            return Response('bad request', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'result': 'success', 'data':user_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'result':'fail', 'data':user_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, **kwargs):
        # print("유저아이디",kwargs.get('u_id'))
        # print("넘어온Body데이터",request.data)
        user_obj = User.objects.get(user_id=kwargs.get('u_id'))
        user_put_serializer = UserSerializer(user_obj,data=request.data)
        print(user_put_serializer)
        if user_put_serializer.is_valid():
            user_put_serializer.save()
            return Response({'result':'success',
                'data': user_put_serializer.data}, status=status.HTTP_200_OK)
        else :
            return Response({'result':'fail',
                'data': user_put_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
