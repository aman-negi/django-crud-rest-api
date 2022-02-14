
from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView,UpdateView,DeleteView


urlpatterns = [
    path('api/register',RegisterView.as_view()),
    path('api/login',LoginView.as_view()),
    path('api/user',UserView.as_view()),
    path('api/update',UpdateView.as_view()),
    path('api/logout',LogoutView.as_view()),
    path('api/delete',DeleteView.as_view()),
    
]