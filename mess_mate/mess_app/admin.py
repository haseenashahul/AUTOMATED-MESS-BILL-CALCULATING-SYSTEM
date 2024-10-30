# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#        model = CustomUser
#        # Specify which fields to display in the admin panel
#        fieldsets = UserAdmin.fieldsets + (
#            (None, {'fields': ('phone_number', 'address', 'birth_date')}),
#        )

# admin.site.register(CustomUser,UserAdmin)
# from django.contrib import admin
# from .models import Book

# admin.site.register(Book)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,HostelBillSettings,Expenditure

class CustomUserAdmin(UserAdmin):
       model = CustomUser
       # Specify which fields to display in the admin panel
       fieldsets = UserAdmin.fieldsets + (
           (None, {'fields': ('dob', 'gender', 'address','course','reg_no','sem','start_year','end_year','ph_no','guard_name','guard_phn')}),
       )

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Employee)
# admin.site.register(EmployeeLeave)
admin.site.register(HostelBillSettings)
admin.site.register(Expenditure)