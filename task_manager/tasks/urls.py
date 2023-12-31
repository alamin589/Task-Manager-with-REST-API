# urls.py
from django.urls import path
from .views import UserRegistration, UserLogin
from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskPhotoListCreateView,
    TaskPhotoRetrieveUpdateDestroyView,
)
urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('taskslist/', TaskListView.as_view(), name='task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('api/tasks/', TaskListCreateView.as_view(), name='api-task-list-create'),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='api-task-retrieve-update-destroy'),
    path('api/task-photos/', TaskPhotoListCreateView.as_view(), name='api-task-photo-list-create'),
    path('api/task-photos/<int:pk>/', TaskPhotoRetrieveUpdateDestroyView.as_view(), name='api-task-photo-retrieve-update-destroy'),


]
