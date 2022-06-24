from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/messages/', include('messanger.urls')),
]
