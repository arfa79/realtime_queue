from django.shortcuts import render

# Create your views here.
# taskqueue/views.py

from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
import redis
from celery import Celery
from django.shortcuts import render
from rest_framework import generics
from .serializers import TaskSerializer

def submit_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.status = 'queued'
            task.save()

            # Send the task to the Celery queue for processing
            process_task.apply_async(args=[task.id])

            # TODO: Update task status in Redis
            redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
            redis_key = f'task:{task.id}:status'
            redis_client.set(redis_key, 'queued')

            return redirect('task-list')
    else:
        form = TaskForm()

    return render(request, 'task_queue/submit_task.html', {'form': form})
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_queue/task_list.html', {'tasks': tasks})
class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer()

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer()