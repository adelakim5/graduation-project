from django.shortcuts import render
import datetime
from django.http import HttpResponse
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def stream(request):
    notification = Notification.objects.filter(
        sent=False, user=request.user
    ).first()

    text = ''

    if notification:
        text = notification.text
        notification.sent = True
        notification.save()

    return HttpResponse(
        'data: %s\n\n' % text,
        content_type='text/event-stream'
    )
    
def send_notification(user, text):
    Notification.objects.create(
        user=user, text=text
    )