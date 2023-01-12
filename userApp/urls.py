from django.urls import path

from userApp.views import UserDetails,Register,AllUsers, PasswordLogin, LogOutApi
# from userApp import views

urlpatterns = [
    path('user/<int:id>/', UserDetails.as_view()),
    path('register/', Register.as_view()),
    path('allUsers/', AllUsers.as_view()),
    path('login_password/', PasswordLogin.as_view()),
    path('logout/', LogOutApi.as_view())

]
