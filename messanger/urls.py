from django.urls import path, include

from messanger import views

urlpatterns = [
    path('', views.messages),
    path('<int:pk>', views.get_delete_message),
    path('<str:username>', views.all_user_messages)
]
