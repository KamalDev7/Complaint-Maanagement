from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/staff/', views.staff_dashboard, name='staff_dashboard'),
    # path('delete/<int:id>/',views.delete)
]
