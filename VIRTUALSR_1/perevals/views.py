from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PerevalAdded
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
class SubmitDataView(APIView):

    def get(self, request, id=None):
        if id:
            try:
                pereval = PerevalAdded.objects.get(id=id)
            except PerevalAdded.DoesNotExist:
                return Response(
                    {"message": "Запись с таким id не найдена"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = PerevalSerializer(pereval)
            return Response(serializer.data, status=status.HTTP_200_OK)

        user_email = request.query_params.get("user__email")

        if user_email:
            perevals = PerevalAdded.objects.filter(user__email=user_email)
            serializer = PerevalSerializer(perevals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": "Укажите id или user__email"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, id=None):
        if not id:
            return Response(
                {
                    "state": 0,
                    "message": "Не указан id записи"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pereval = PerevalAdded.objects.get(id=id)
        except PerevalAdded.DoesNotExist:
            return Response(
                {
                    "state": 0,
                    "message": "Запись с таким id не найдена"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if pereval.status != "new":
            return Response(
                {
                    "state": 0,
                    "message": "Редактирование запрещено: запись не в статусе new"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()

        if "user" in data:
            data.pop("user")

        serializer = PerevalSerializer(
            pereval,
            data=data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "state": 1,
                    "message": "Запись успешно обновлена"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "state": 0,
                "message": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )