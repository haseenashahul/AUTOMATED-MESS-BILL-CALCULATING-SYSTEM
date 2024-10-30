from django.urls import path
from . import views


urlpatterns = [
    path('profile',views.profile,name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('leave_applications/', views.leave_applications_list, name='leave_applications'),
     path('list_bills/', views.list_bills, name='list_bills'),
     path('pay_bill/<int:bill_id>/', views.accept_payment, name='pay_bill'),
]
