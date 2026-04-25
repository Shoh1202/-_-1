from django.urls import path
from .views import SubmitDataAPIView
from .views import SubmitDataView

urlpatterns = [
    path('submitData', SubmitDataAPIView.as_view(), name='submit_data_no_slash'),
    path('submitData/', SubmitDataAPIView.as_view(), name='submit_data'),
    path('submitData/<int:id>', SubmitDataView.as_view(), name='submit_data_detail'),
]