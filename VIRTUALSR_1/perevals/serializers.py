from rest_framework import serializers
from .repository import PerevalRepository


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fam = serializers.CharField()
    name = serializers.CharField()
    otc = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField()


class CoordsSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    height = serializers.IntegerField()


class LevelSerializer(serializers.Serializer):
    winter = serializers.CharField(required=False, allow_blank=True)
    summer = serializers.CharField(required=False, allow_blank=True)
    autumn = serializers.CharField(required=False, allow_blank=True)
    spring = serializers.CharField(required=False, allow_blank=True)


class ImageSerializer(serializers.Serializer):
    data = serializers.CharField()
    title = serializers.CharField()


class SubmitDataSerializer(serializers.Serializer):
    beauty_title = serializers.CharField(required=False, allow_blank=True)
    title = serializers.CharField()
    other_titles = serializers.CharField(required=False, allow_blank=True)
    connect = serializers.CharField(required=False, allow_blank=True)
    add_time = serializers.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S', 'iso-8601']
    )

    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    def validate_images(self, value):
        if not value:
            raise serializers.ValidationError('Нужно передать хотя бы одну фотографию.')
        return value

    def create(self, validated_data):
        return PerevalRepository.create_pereval(validated_data)