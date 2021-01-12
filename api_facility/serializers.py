from rest_framework.serializers import ModelSerializer
from .models import Facility

class FacilitySerializer(ModelSerializer):
    class Meta:
        model=Facility
        fields = '__all__' #필요한 것만 보려면 튜플로 나열하기 ('id','address'...,'tel')