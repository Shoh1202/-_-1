from django.db import transaction
from .models import PerevalAdded, PerevalImage


class PerevalRepository:
    @staticmethod
    @transaction.atomic
    def create_pereval(validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        pereval = PerevalAdded.objects.create(
            beauty_title=validated_data.get('beauty_title', ''),
            title=validated_data['title'],
            other_titles=validated_data.get('other_titles', ''),
            connect=validated_data.get('connect', ''),
            add_time=validated_data['add_time'],

            user_email=user_data['email'],
            user_fam=user_data['fam'],
            user_name=user_data['name'],
            user_otc=user_data.get('otc', ''),
            user_phone=user_data['phone'],

            latitude=coords_data['latitude'],
            longitude=coords_data['longitude'],
            height=coords_data['height'],

            winter=level_data.get('winter', ''),
            summer=level_data.get('summer', ''),
            autumn=level_data.get('autumn', ''),
            spring=level_data.get('spring', ''),
        )

        images = [
            PerevalImage(
                pereval=pereval,
                data=image['data'],
                title=image['title']
            )
            for image in images_data
        ]
        PerevalImage.objects.bulk_create(images)

        return pereval