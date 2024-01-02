from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Below is the adim url. This is where you can access the admin panel.
    path('admin/', admin.site.urls),

    # Below is the url for the authentication app. Add the 'api/authentication' 
    # in your link address then the other authentication urls to visit its page.
    path('api/user/', include('authentication.urls')),
]
