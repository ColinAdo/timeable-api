from django.urls import path, re_path
from .views import (
    LogoutView,
    CustomTokenVerifyView,
    CustomProviderAuthView,
    CustomTokenRefreshView,
    CustomTokenObtainPairView,
    RegisterView,
)

urlpatterns = [
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth'
    ),
    path('register/', RegisterView.as_view(), name='register'),
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
]
