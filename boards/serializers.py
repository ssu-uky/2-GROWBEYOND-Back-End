from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import PossibleBoard
from django.core.exceptions import ValidationError


# title에 띄어쓰기 금지
def validate_no_spaces(value):
    if ' ' in value:
        raise ValidationError("띄어쓰기 없이 입력해야 합니다.")
    return value


# title에 5단어 이상 금지
def validate_max_words(value):
    words = value.split(',')
    if len(words) > 6:
        raise serializers.ValidationError("5단어 이내로 입력해야합니다.")
    return value


class PossibleBoardSerializer(ModelSerializer):
    # title 함수 적용
    title = serializers.CharField(
        max_length=20,
        validators=[validate_no_spaces, validate_max_words]
    )
    
    class Meta:
        model = PossibleBoard
        fields = (
            "pk",
            "title",
            "name",
            "telephone",
            "email",
            "password",
            "description",
            "counsling",
            "file",
        )


# list를 위한 serializer
class PossibleBoardListSerializer(ModelSerializer):
    class Meta:
        model = PossibleBoard
        fields = (
            "pk",
            "title",
            "name",
            "created_at",
        )
