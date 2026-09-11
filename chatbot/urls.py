from django.urls import path
from . import views

urlpatterns = [
    path('reply/', views.chatbot_response, name='chatbot_reply'),
]
