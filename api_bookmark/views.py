from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from .serializers import BookMarkSerializer
from .models import BookMark
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from api_facility.models import Facility
from api_facility.serializers import FacilitySerializer

class BookMarkQuerySet(ModelViewSet):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer

    def get_queryset(self, query):
        queryset = super().get_queryset()
        if query.get('f_id') : 
            queryset = queryset.filter(user_id=query.get('user_id'), f_id=query.get('f_id'))
        else: #유저의 즐겨찾기 목록
            queryset = queryset.filter(user_id=query.get('user_id'),state=query.get('state'))
        return queryset


class BookMarkView(APIView):
    def get(self,request, **kwargs):
        if kwargs.get('user_id') is None: 
            return Response('user_id is required', status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.GET.get('f_id') is None: #즐겨찾기 목록
                query={'user_id':kwargs.get('user_id'),'state':'정상'}
                bookmark_queryset = BookMarkQuerySet().get_queryset(query)
                bm_serializer= BookMarkSerializer(bookmark_queryset,many=True)
                facilities = []
                for bm in bm_serializer.data:
                    item = dict(bm.items())
                    f_obj = Facility.objects.get(f_id=item.get('f_id'))
                    fc_serializer = FacilitySerializer(f_obj)
                    facilities.append(fc_serializer.data)
                #print(facilities)
                return Response({"bookmark_data":bm_serializer.data,
                                "facilities_data":facilities}, status=status.HTTP_200_OK)

            else: #해당 시설을 체크했는지 확인용
                query={'user_id':kwargs.get('user_id'),'f_id':request.GET.get('f_id')}
                bookmark_queryset = BookMarkQuerySet().get_queryset(query)
                try:
                    bookmark_queryset.get(state='정상') #state정상or해제
                    bookmark = True
                except:
                    bookmark = False
                return Response({"isMarked":bookmark},status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.data.get('user_id')
        f_id = request.data.get('f_id')
        try:
            bm_obj = BookMark.objects.get(user_id=user_id, f_id=f_id)
            bm_serializer = BookMarkSerializer(bm_obj, data=request.data)
        except:
            bm_serializer = BookMarkSerializer(data=request.data)
        if bm_serializer.is_valid():
            bm_serializer.save()
            return Response({'result': 'success', 'data':bm_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'result':'fail', 'data':bm_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


            