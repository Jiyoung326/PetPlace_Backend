from rest_framework.serializers import ModelSerializer
from .models import PhotoBoard

class PhotoAllSerializer(ModelSerializer):
    class Meta:
        model=PhotoBoard
        fields = ('b_id', 'image') #필요한 것만 보려면 튜플로 나열하기 ('id','address'...,'tel')

class PhotoDetailSerializer(ModelSerializer):
    class Meta:
        model=PhotoBoard
        fields = '__all__'

class PhotoMySerializer(ModelSerializer):
    class Meta:
        model=PhotoBoard
        fields = ('b_id','title','regdate','image')