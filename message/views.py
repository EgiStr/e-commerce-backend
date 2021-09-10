import threading
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import asyncio
from sercives.firebase.firestore import sendMessage

# Create your views here.
async def follow_up_task(task: asyncio.Task):
    if task.done():
        print('update_all task completed: {}'.format(task.result()))
    else:
        print('task not completed after 5 seconds, aborting')
        task.cancel()

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def sendMessageApiView(request):
    if request.method == "POST":
        # Once the task is created, it will begin running in parallel
        sendMessage(request.user,request.data)
        
        return Response(status=status.HTTP_200_OK)
