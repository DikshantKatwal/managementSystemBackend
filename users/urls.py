from django.urls import path
from knox import views as knox_views

from .api import *

urlpatterns = [
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('user/', GetUserDetails.as_view(), name='get_user_details'),
    path('user/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
