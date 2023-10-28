from celery import Celery
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Task

celery = Celery('taskqueue_project')

@celery.task
def process_task(task_id):
    try:
        # Fetch the task from the database using the task_id
        task = Task.objects.get(id=task_id)

        # Update the task status to 'processing'
        task.status = 'processing'
        task.save()

        # Simulate task processing 
        import time
        time.sleep(5)  # Simulate a task that takes 5 seconds

        # After processing, update the task status to 'completed'
        task.status = 'completed'
        task.save()

        # Send a WebSocket message to update the task status
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'task_{task.id}',
            {
                'type': 'update_status',
                'status': task.status,
            }
        )
    except Task.DoesNotExist:
        # Handle the case where the task doesn't exist
        pass

