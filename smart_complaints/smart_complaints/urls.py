from django.contrib import admin
from django.urls import path, include
from users.views import home_redirect

urlpatterns = [
    path('', home_redirect),
    path('', include('users.urls')),
    path('complaints/', include('complaints.urls')), 
    path('dashboard/', include(('users.urls', 'users'), namespace='users')),
    # path('complaints/', include(('complaints.urls', 'complaints'), namespace='complaints')),
]



