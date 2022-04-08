from django.urls import path
from basic import consumers

urlrouter = [
    path('chat/', consumers.ChatConsumer.as_asgi())
]
