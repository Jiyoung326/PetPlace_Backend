from rest_framework.serializers import ModelSerializer
from .models import BookMark

class BookMarkSerializer(ModelSerializer):
    class Meta:
        model=BookMark
        fields = '__all__' 