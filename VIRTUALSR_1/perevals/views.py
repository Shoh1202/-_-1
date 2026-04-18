from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SubmitDataSerializer


def format_errors(errors):
    messages = []

    if isinstance(errors, dict):
        for field, value in errors.items():
            if isinstance(value, dict):
                nested = format_errors(value)
                messages.append(f'{field}: {nested}')
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, (dict, list)):
                        messages.append(f'{field}: {format_errors(item)}')
                    else:
                        messages.append(f'{field}: {item}')
            else:
                messages.append(f'{field}: {value}')
    elif isinstance(errors, list):
        for item in errors:
            if isinstance(item, (dict, list)):
                messages.append(format_errors(item))
            else:
                messages.append(str(item))
    else:
        messages.append(str(errors))

    return '; '.join(messages)


class SubmitDataAPIView(APIView):
    def post(self, request):
        serializer = SubmitDataSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'status': 400,
                    'message': format_errors(serializer.errors),
                    'id': None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pereval = serializer.save()

            return Response(
                {
                    'status': 200,
                    'message': 'Отправлено успешно',
                    'id': pereval.id
                },
                status=status.HTTP_200_OK
            )

        except DatabaseError:
            return Response(
                {
                    'status': 500,
                    'message': 'Ошибка подключения к базе данных',
                    'id': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {
                    'status': 500,
                    'message': str(e),
                    'id': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )