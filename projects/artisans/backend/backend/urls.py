from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Below is the adim url. This is where you can access the admin panel.
    path('admin/', admin.site.urls),

    # Below is the url for the authentication app. Add the 'api/authentication' 
    # in your link address then the other authentication urls to visit its page.
    path('api/user/', include('authentication.urls')),

    # Use this link to login with google
    # Enter --> "http://127.0.0.1:8000/accounts/login/"
    path('accounts/', include('allauth.urls')),
]
