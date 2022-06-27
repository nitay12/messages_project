from django.urls import path, include

from messenger import views

urlpatterns = [
    path('', views.messages),
    path('<str:username>', views.all_user_messages, name='user_messages'),
    path('<str:username>/<int:pk>', views.get_delete_message, name='one_message')
]
