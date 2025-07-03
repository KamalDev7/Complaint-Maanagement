from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('my/', views.my_complaints, name='my_complaints'),
    path('admin-dashboard/', views.admin_complaint_list, name='admin_complaints'),
    path('assign/<int:complaint_id>/', views.assign_complaint, name='assign_complaint'),
    path('admin-update/<int:complaint_id>/', views.update_complaint, name='update_complaint'),
    path('user-history/', views.user_history_view, name='user_history'),
    path('dashboard/staff/', views.staff_dashboard_view, name='staff_complaint'),
    path('staff-update/<int:complaint_id>/', views.staff_update_complaint, name='staff_update_complaint'),
    path('staff/', views.staff_dashboard_view, name='staff_complaint'),
    path('mark-resolved/', views.mark_complaint_resolved, name='mark_resolved'),
]


