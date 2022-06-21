from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
urlpatterns = [
    path('register', UserRegistrationView.as_view(),name="register"),
   path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
