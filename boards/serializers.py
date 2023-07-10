from rest_framework.serializers import ModelSerializer
from .models import PossibleBoard
from django.core.exceptions import ValidationError


class PossibleBoardSerializer(ModelSerializer):
    
    class Meta:
        model = PossibleBoard
        fields = "__all__"
