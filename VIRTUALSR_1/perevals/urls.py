from django.urls import path
from .views import SubmitDataAPIView

urlpatterns = [
    path('submitData', SubmitDataAPIView.as_view(), name='submit_data_no_slash'),
    path('submitData/', SubmitDataAPIView.as_view(), name='submit_data'),
]