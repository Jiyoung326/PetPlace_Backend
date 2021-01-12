from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from .serializers import FacilitySerializer
from .models import Facility
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from haversine import haversine

class FacilityQuerySet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    def get_queryset(self,query):
        queryset = super().get_queryset()
        if query.get('qry'):
            queryset = queryset.filter(f_id__contains=query['category'],gu__contains=query['gu']
                            ,title__contains=query['qry']) 
        else:
            queryset = queryset.filter(f_id__contains=query['category'],gu__contains=query['gu'])
        return queryset

class FacilityView(APIView):
    def get(self,request, **kwargs):

        if kwargs.get('category') is None or request.GET.get('gu') is None: #카테고리,구 없을 때
            return Response('카테고리,구 파라미터 필요',status=status.HTTP_400_BAD_REQUEST)
        else: #카테고리,구 넘어옴
            if request.GET.get('lat') and request.GET.get('long'): #위도, 경도 파라미터 옴.
                query = {'category':kwargs.get('category'),'gu':request.GET.get('gu')}
                fac_queryset = FacilityQuerySet().get_queryset(query)
                fac_all_serializer = FacilitySerializer(fac_queryset,many=True)
                currLocation = (float(request.GET.get('lat')),float(request.GET.get('long')))
                print(">>>>>>>>>>>>현재위도,경도 "+str(currLocation))
                temp = []
                for fac in fac_all_serializer.data:
                    item = dict(fac.items())
                    facLocation = (item['latitude'],item['longitude'])
                    #print(">>>>>>>>>>>>시설위도,경도 "+str(facLocation))
                    distance = haversine(currLocation,facLocation)
                    #print(">>>>>>>>>>>>거리 "+str(distance))
                    item['distance']=distance
                    temp.append(dict(item))
                temp = sorted(temp, key=lambda x: x['distance'])
                
                return Response(temp, status=status.HTTP_200_OK)

            elif request.GET.get('qry'): #서치로 가져오기
                query = {'category':kwargs.get('category'),'gu':request.GET.get('gu'), 'qry':request.GET.get('qry')}
                fac_queryset = FacilityQuerySet().get_queryset(query)
                fac_all_serializer = FacilitySerializer(fac_queryset,many=True)

                return Response(fac_all_serializer.data, status=status.HTTP_200_OK)
            
            else : #경도,위도 안 넘어옴 '구'로만 가져오기
                query = {'category':kwargs.get('category'),'gu':request.GET.get('gu')}
                fac_queryset = FacilityQuerySet().get_queryset(query)
                fac_all_serializer = FacilitySerializer(fac_queryset,many=True)

                return Response(fac_all_serializer.data, status=status.HTTP_200_OK)
                

            





