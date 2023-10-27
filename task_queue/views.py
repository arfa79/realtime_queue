from django.shortcuts import render

# Create your views here.
# taskqueue/views.py

from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
import redis
from celery import celery
from django.shortcuts import render
def submit_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the user to the task
            task.status = 'queued'  # Set the initial status

            # Save the task to the database
            task.save()
            #TODO1
            @celery.task
            def process_task(task_id):
            # Add your task processing code here
            # Fetch the task using task_id and update its status

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
                        # ...

                        return redirect('task-list')
                else:
                    form = TaskForm()

                return render(request, 'taskqueue/submit_task.html', {'form': form})
            #TODO2
            def submit_task(request):
                if request.method == 'POST':
                    form = TaskForm(request.POST)
                    if form is_valid():
                        task = form.save(commit=False)
                        task.user = request.user
                        task.status = 'queued'
                        task.save()

                        # Send the task to the Celery queue for processing
                        process_task.apply_async(args=[task.id])

                        # Update task status in Redis
                        redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
                        redis_key = f'task:{task.id}:status'
                        redis_client.set(redis_key, 'queued')

                        return redirect('task-list')
                else:
                    form = TaskForm()

                return render(request, 'taskqueue/submit_task.html', {'form': form})
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'taskqueue/task_list.html', {'tasks': tasks})