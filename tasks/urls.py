from django.urls import path
from tasks.views import *

urlpatterns = [
    path('', TaskData.as_view(), name='task-data'),
    path('<int:id>/', TaskDetail.as_view(), name='task-detail'),
]

