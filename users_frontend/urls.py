
from django.urls import path
from .views import Login,Register,Profile


urlpatterns = [
    path('',Login,name="login"),
    path('register',Register,name="register"),
    path('profile',Profile,name="profile"),

]