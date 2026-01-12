from django.urls import path
from habits.views import *

urlpatterns = [
    path('', HabitData.as_view(), name='habit-list-create'),
    path('<int:id>/', HabitDetail.as_view(), name='habit-detail'),
    path('<int:habit_id>/logs/', HabitLogData.as_view(), name='habitlog-data'),
]