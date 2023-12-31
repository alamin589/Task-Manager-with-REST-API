from django.shortcuts import render, redirect
from .models import User,Task, TaskPhoto
from django.db.models import Q
from .models import Task
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.http import HttpResponse
from .forms import TaskForm, UserForm
from rest_framework import generics
from .serializers import TaskSerializer, TaskPhotoSerializer

class UserRegistration(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            # In a production system, you should hash the password before saving.
            form.save()
            return redirect('user-login')  # Correct the redirect URL
        return render(request, 'registration.html', {'form': form})

class UserLogin(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # In a production system, you should verify the password (e.g., by hashing and comparing).
        try:
            user = User.objects.get(username=username, password=password)
            return redirect('task-list')  # Correct the redirect URL
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

class TaskListView(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        filter_created_at = request.GET.get('created_at', '')
        filter_due_date = request.GET.get('due_date', '')
        filter_priority = request.GET.get('priority', '')
        filter_is_complete = request.GET.get('is_complete', '')

        tasks = Task.objects.order_by('-created_at')

        if search_query:
            tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        if filter_created_at:
            tasks = tasks.filter(created_at__date=filter_created_at)

        if filter_due_date:
            tasks = tasks.filter(due_date__date=filter_due_date)

        if filter_priority:
            tasks = tasks.filter(priority=filter_priority)

        if filter_is_complete:
            tasks = tasks.filter(is_complete=filter_is_complete)

        return render(request, 'task_list.html', {'tasks': tasks})

class TaskDetailView(View):
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            # Get the photos associated with the task
            photos = TaskPhoto.objects.filter(task=task)
            return render(request, 'task_detail.html', {'task': task, 'photos': photos})
        except Task.DoesNotExist:
            return HttpResponse(status=404)

class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'task_create.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save()

            # Handle photo upload
            photo_file = request.FILES.get('photo')
            if photo_file:
                TaskPhoto.objects.create(task=task, photo=photo_file)

            return redirect('task-list')
        else:
            return render(request, 'task_create.html', {'form': form})

class TaskUpdateView(View):
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            form = TaskForm(instance=task)
            
            # Get the photos associated with the task
            photos = TaskPhoto.objects.filter(task=task)
            
            return render(request, 'task_update.html', {'form': form, 'photos': photos})
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            form = TaskForm(request.POST, request.FILES, instance=task)

            if form.is_valid():
                updated_task = form.save()

                # Handle photo upload
                photo_file = request.FILES.get('photo')
                if photo_file:
                    TaskPhoto.objects.create(task=updated_task, photo=photo_file)

                return redirect('task-list')
            
            # If form is not valid, get the photos associated with the task
            photos = TaskPhoto.objects.filter(task=task)
            
            return render(request, 'task_update.html', {'form': form, 'photos': photos})
        except ObjectDoesNotExist:
            return HttpResponse(status=404)


class TaskDeleteView(View):
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            return render(request, 'task_delete.html', {'task': task})
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return redirect('task-list')
        except ObjectDoesNotExist:
            return HttpResponse(status=404)



class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskPhotoListCreateView(generics.ListCreateAPIView):
    queryset = TaskPhoto.objects.all()
    serializer_class = TaskPhotoSerializer

class TaskPhotoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskPhoto.objects.all()
    serializer_class = TaskPhotoSerializer
