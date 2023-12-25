from django.urls import path
from .views import RegisterUserView, LoginUserView, UserView, LogoutView, ResetPasswordView

urlpatterns = [
    # This is the url for the register page. Add the 'register-account' in your link
    path('register-account/', RegisterUserView.as_view(), name='register'),

    # This is the url for the login page. Add the '' in your link.
    path('login/', LoginUserView.as_view(), name='login'),

    # This is the url for the user page. Add the 'user' in your link.
    path('user-details/', UserView.as_view(), name='user'),

    # This is the url for the logout page. Add the 'logout' in your link.
    path('logout/', LogoutView.as_view(), name='logout'),

    # This is the url for the reset password page. Add the 'reset-password' in your link.
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]