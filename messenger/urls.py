from django.urls import path, include

from messenger import views

urlpatterns = [
    path('', views.MessagesView.as_view()),
    path('<str:username>', views.all_user_messages, name='user_messages'),
    path('<str:username>/<int:pk>', views.OneMessageView.as_view(), name='one_message')
]
