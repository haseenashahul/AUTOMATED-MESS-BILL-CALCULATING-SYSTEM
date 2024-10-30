from django.urls import path
from . import views


urlpatterns = [
    path('',views.user_login,name='login'),
    path('warden/',views.warden_dashboard,name='warden-dashboard'),
    path('create_user/', views.create_custom_user, name='create_user'),#student registration
    path('user_success/', views.user_success, name='user_success'),#after registration waiting for admin approval
    path('student/',views.student_dashboard,name='student-dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('registered-students/', views.list_registered_users, name='registered-students'),#registered students
    path('accept-user/<int:user_id>/', views.accept_user, name='accept_user'),
    path('reject-user/<int:user_id>/', views.reject_user, name='reject_user'),
    path('active_students/', views.list_active_users, name='active_students'),#active student(can login)
    path('delete_active_user/<int:user_id>/', views.delete_active_user, name='delete_active_user'),
    path('past_students/', views.list_past_users, name='past_students'),#vacated students
    path('leave/accept/<int:leave_id>/', views.accept_leave, name='accept_leave'),
    path('leave/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    # path('employee_list', views.add_employee, name='employee_list'),
    # path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    # path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    # path('add_employee_leave/', views.add_employee_leave, name='add_employee_leave'),
    path('expenditure_list/', views.expenditure_list, name='expenditure_list'),
    path('hostel_bill_settings/', views.hostel_bill_settings, name='hostel_bill_settings'),
    path('generate_bill/', views.generate_bill, name='generate_bill'),
    path('approve_payment/<int:bill_id>/', views.approve_payment, name='approve_payment'),

]
