from calendar import monthrange
from decimal import Decimal
from django.db import IntegrityError
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .forms import CustomUserForm,HostelBillSettingsForm,ExpenditureForm
from .models import CustomUser,HostelBillSettings,Expenditure
from student.models import LeaveApplication,HostelBillDetail
from datetime import datetime,date
from django.db.models import Sum  
from collections import defaultdict,OrderedDict



def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate the user with email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_superuser:
                # If user is superuser, log them in
                login(request, user)
                return redirect('warden-dashboard')
            elif user:
                login(request, user)
                return redirect('student-dashboard')
            else:
                messages.error(request, 'You do not have superuser permissions.')
                return redirect('login')
        else:
            # Invalid credentials
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'login.html')


@never_cache
@login_required
def warden_dashboard(request):
     if request.user.is_authenticated:
       registered_users_count = CustomUser.objects.filter(is_superuser=False, is_active=False, past_stud=False).count()
    
    # Count of active users
       active_users_count = CustomUser.objects.filter(is_superuser=False,is_active=True,past_stud=False).count()
    
    # Count of past users
       past_users_count = CustomUser.objects.filter(is_superuser=False,is_active=False,past_stud=True).count()
       total_due = calculate_total_due_amount() 
    
    # Pass all counts to the template
     return render(request,'warden_dashboard.html',{'registered_users_count': registered_users_count,'active_users_count': active_users_count,
                                                    'past_users_count': past_users_count ,'total_due':total_due})


@never_cache
@login_required
def student_dashboard(request):
     if request.user.is_authenticated:
      bills = HostelBillDetail.objects.filter(student=request.user)
      
      return render(request,'student/dashboard.html',{'bills':bills})


def user_logout(request):
    logout(request)  # Logs out the user
    return redirect('login')  

#signup form 
def create_custom_user(request):
    if request.method == "POST":
        # print(request.POST)
        form = CustomUserForm(request.POST)
        
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.email  # Assign email to username
                user.save()
                return redirect('user_success')
            else:
                # If the form is not valid, capture and display errors
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)  # Add each field error to messages

                # Also add non-field errors, if any
                for error in form.non_field_errors():
                    messages.error(request, error)

        except IntegrityError as e:
            # Handle unique constraint violations
            if "UNIQUE constraint failed: mess_app_customuser.username" in str(e):
                messages.error(request, "A user with that email already exists.")
            else:
                messages.error(request, "An unexpected error occurred.")
            print(f"IntegrityError: {e}")
            return redirect('create_user')
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            print(f"Unexpected Error: {e}")
            return redirect('create_user')

        return redirect('create_user')  # Redirect to create_user if the form is not valid

    else:
        form = CustomUserForm()
    
    return render(request, 'signup.html', {'form': form})


# after signup wait for admin approvel
def user_success(request):
    return render(request, 'user_success.html')


def list_registered_users(request):
    # Fetch all users from the CustomUser model
    users = CustomUser.objects.filter(is_superuser=False,is_active=False,past_stud=False).order_by('course')  
    return render(request, 'registerd_users.html', {'users': users})



#warden accept user then set active is true
def accept_user(request, user_id):
    # Get the custom user by ID and set is_active to True
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    # messages.success(request, f"{user.first_name} {user.last_name} has been accepted and activated.")
    return redirect('registered-students') 


#warden reject student from registered student list
def reject_user(request, user_id):
    # Get the custom user by ID and set is_active to False
    user = get_object_or_404(CustomUser, id=user_id)
    # user.is_active = False
    # user.past_stud=False
    user.delete()
    messages.error(request, f"{user.first_name} {user.last_name} has been rejected and deactivated.")
    return redirect('registered-students')


def list_active_users(request):
    # Fetch all users from the CustomUser model
    users = CustomUser.objects.filter(is_superuser=False,is_active=True,past_stud=False).order_by('course')   
    # print(request.user.first_name)
    return render(request, 'students.html', {'users': users})


#for deleting active students
def delete_active_user(request, user_id):
    # Get the custom user by ID and set is_active to True
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.past_stud=True
    user.save()
    return redirect('active_students') 


def list_past_users(request):
    # Fetch all users from the CustomUser model
    users = CustomUser.objects.filter(is_superuser=False,is_active=False,past_stud=True).order_by('course') 

    return render(request, 'past_student.html', {'users': users})


def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def accept_leave(request, leave_id):
    leave = get_object_or_404(LeaveApplication, id=leave_id)
    leave.status = 'approved'
    leave.save()
    return redirect('leave_applications')  # Redirect to leave list or dashboard

@user_passes_test(is_admin)
def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveApplication, id=leave_id)
    leave.status = 'rejected'
    leave.save()
    return redirect('leave_applications')  # 




# @user_passes_test(is_admin)
# def add_employee(request):
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('employee_list')
#     else:
#         form = EmployeeForm()
#         employee = Employee.objects.all()
    
#     return render(request, 'employee_list.html', {'employees':employee,'form': form})



# @user_passes_test(is_admin)
# def delete_employee(request, employee_id):
#     employee = get_object_or_404(Employee, id=employee_id)
#     employee.delete()
#     return redirect('employee_list')


# @user_passes_test(is_admin)
# def update_employee(request, employee_id):
#     employee = get_object_or_404(Employee, id=employee_id)
#     if request.method == 'POST':
#         employee.email = request.POST.get('email')
#         employee.salary = request.POST.get('salary')
#         employee.position = request.POST.get('position')
#         employee.ph_no = request.POST.get('ph_no')
#         employee.save()
#         return redirect('employee_list')  # Redirect to the employee list or another page after saving
    


# @user_passes_test(is_admin)
# def add_employee_leave(request):
#     if request.method == 'POST':
#         form = EmployeeLeaveForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the leave data
#             return redirect('add_employee_leave')  # Redirect after successful submission
#     else:
#         form = EmployeeLeaveForm()
#         emp_leave = EmployeeLeave.objects.all()

#     return render(request, 'employee_leave.html', {'emp_leaves':emp_leave,'form': form})



def expenditure_list(request):
    if request.method == 'POST':
        form = ExpenditureForm(request.POST, request.FILES)
        # print(request.POST)  
        if form.is_valid():
            form.save()
            return redirect('expenditure_list')  # Replace with the name of the view or URL to redirect after saving
    else:
        form = ExpenditureForm()


    # Retrieve and order all expenditures by date
    expenditures = Expenditure.objects.all().order_by('expenditure_date')
    monthly_expenditures = defaultdict(list)

     # Group expenditures by month and year and calculate monthly totals
    for expense in expenditures:
        month_year = expense.expenditure_date.strftime('%m/%Y')  # Example:9/2024
        monthly_expenditures[month_year].append(expense)

    # Calculate the total for each month and attach it to the monthly_expenditures dictionary
    monthly_expenditures_with_totals = {}
    for month, expenses in monthly_expenditures.items():
        total = sum(exp.amount for exp in expenses)
        monthly_expenditures_with_totals[month] = {
            'expenses': expenses,
            'total': total
        }

        # Sort the monthly expenditures by month in descending order
    sorted_monthly_expenditures = OrderedDict(sorted(monthly_expenditures_with_totals.items(), key=lambda x: x[0], reverse=True))


    # Pass the modified monthly_expenditures_with_totals to the template
    return render(request, 'expenditure_form.html', {
        'form': form,
        'monthly_expenditures': sorted_monthly_expenditures,
    })



@user_passes_test(is_admin)
def hostel_bill_settings(request):
    # Retrieve the first (or only) instance of HostelBillSettings, or create a default one if none exists
    current_year = datetime.now().year
    year_range = list(range(current_year - 5, current_year + 1))  
    settings = HostelBillSettings.objects.first()
        

    if request.method == 'POST':
        form = HostelBillSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()  # Save the updated settings
            return redirect('hostel_bill_settings')  # Redirect to avoid form resubmission
    else:
        form = HostelBillSettingsForm(instance=settings)

    return render(request, 'bill_settings.html', {'form': form, 'settings': settings,'current_year': current_year , 'year_range': year_range, })





def generate_bill(request):
    if request.method == "POST":
        month = request.POST.get('month')
        year = request.POST.get('year')
        
        # Create a date object for the first day of the selected month
        selected_month = datetime(year=int(year), month=int(month), day=1)
        print(selected_month)#print first day of given month  eg:1/12/2024
        # Call the function to generate and save the bill
        generate_and_save_bill_for_month(selected_month)
        
        # Redirect to a success page or render a success message
        return redirect('hostel_bill_settings')  # Replace 'some_success_page' with your actual success page URL or name

    # Optionally, render a form again or an error page if it's not a POST request
    return None  # Replace 'your_template.html' with your actual template




def generate_and_save_bill_for_month(selected_month):
    first_day = selected_month.replace(day=1)  #1/12/2024
    last_day = selected_month.replace(day=monthrange(selected_month.year, selected_month.month)[1])
    
    # Get the active students from the custom user model
    User = get_user_model()
    active_students = User.objects.filter(is_active=True, is_staff=False)  # Assuming non-staff are students
    print(active_students.count())
    
    for student in active_students:
        # Calculate the current month's bill
        total_bill, total, electricity, broadband, maintenance = calculate_bill(student, selected_month.year, selected_month.month)

        # Check for previous dues
        previous_dues = HostelBillDetail.objects.filter(student=student, status__in=['unpaid', 'partially_paid']).aggregate(Sum('due'))['due__sum'] or 0

        # Update total bill to include previous dues
        total_bill += previous_dues
        
        # Determine the status
        status = 'unpaid' if previous_dues > 0 else 'paid'  # Default to unpaid if there are previous dues
        
        # Save the bill details
        bill_detail = HostelBillDetail(
            student=student,
            total_amount=total_bill,
            billing_month=first_day,
            bill_details=f" Grand Total Amount: {total_bill}\nTotal : {total}\n electricity:{electricity}\n broadband:{broadband}\n maintenence:{maintenance}",
            electricity=electricity,
            broadband=broadband,
            maintenence=maintenance,
            total=total,
            status='unpaid',  # Set the status based on previous dues
            due=previous_dues  # Set the due amount
        )
        bill_detail.save()
        print(f"Bill generated and saved for {student.first_name} for {first_day.strftime('%B %Y')}: {total_bill}")




def calculate_bill(student, year, month):
    # Get the current bill settings
    total_bill = 0
    settings = HostelBillSettings.objects.first()
    User = get_user_model()
    # emp_salary = Employee.objects.all()
    # total_salary = sum(salary.salary for salary in emp_salary)
    # print('totalsalry',total_salary)

    active_students_count = User.objects.filter(is_active=True, is_staff=False).count()

    
    # Calculate rent per user and employee salary
    rent_per_user = (settings.rent) / active_students_count if active_students_count > 0 else 0
    emp_salary_per_user = (settings.emp_salary) / active_students_count if active_students_count > 0 else 0
    


    print('rentperuser',rent_per_user)
    print('empsal',emp_salary_per_user)
    print('fixedcharge',settings.perDay_fixedCharge)
    print('ele',settings.electricity)
    print('main',settings.maintenance)
    print('bro',settings.broadband)
    # print('sal split',(total_salary / active_students_count))
     # Assuming a fixed charge for the month
    electricity = settings.electricity
    maintenance = settings.maintenance
    broadband = settings.broadband
    # salary_split = total_salary / active_students_count if active_students_count > 0 else 0


    enrollment_date = student.date_joined 
    print(enrollment_date) # Adjust this according to your model
    days_present = 0
    if enrollment_date:
        # Check if enrolled within the billing month
        if enrollment_date.year == year and enrollment_date.month == month:
            days_in_month = monthrange(year, month)[1] #total no. of days in month eg:30 or 31
            days_present = days_in_month - (enrollment_date.day - 1)  # Days from enrollment to end of month
        else:
            # If enrolled before the billing month, consider all days in the month
            days_present = monthrange(year, month)[1]
    # Calculate total bill
    print(days_present,'dayssssss')
    fixed_charge =settings.perDay_fixedCharge * (30 if days_present in [30, 31] else days_present) #take 30days if present day is 30 or 31 else take presented days
    total=rent_per_user + emp_salary_per_user + fixed_charge
    total_bill = rent_per_user + emp_salary_per_user + fixed_charge + settings.electricity + settings.maintenance + settings.broadband 
    print("total=",total)
    print('grand_total',total_bill)
    # Calculate approved leave days
    approved_leaves = LeaveApplication.objects.filter(
        user=student,
        status='approved',
        start_date__year=year,
        start_date__month=month
    )

    leave_days = 0
    for leave in approved_leaves:
        leave_start = max(leave.start_date, date(year, month, 1)) #compare leave start_date and first days mess_bill_month eg:max(10-10-2024,1-10-24)
        leave_end = min(leave.end_date, date(year, month, monthrange(year, month)[1])) #compare leave end date and last day of mess_bill_month eg:min(15-10-24,30-10-24) .output is 15-10-24
        leave_days += (leave_end - leave_start).days + 1

    # Calculate leave deductions
    print(leave_days,"laeve days")
    leave_deduction = 0
    if leave_days >= 30:
        total_bill = rent_per_user  # Example fixed charge, adjust as needed
        total = rent_per_user
        electricity=0
        maintenance =0
        broadband=0
    elif leave_days > 0:
        leave_deduction = ((leave_days // 5) * 2)* settings.perDay_fixedCharge
    print(leave_deduction,"laeve deudfgdf")
    total_bill=total_bill-leave_deduction
    print(total_bill)
    return total_bill ,total-leave_deduction,electricity,broadband,maintenance





#to get total due of all the students it will display in warden dashboard
def calculate_total_due_amount():
    # Fetch all hostel bill details
    total_due = HostelBillDetail.objects.aggregate(Sum('due'))['due__sum'] or 0
    return total_due



def approve_payment(request, bill_id):
    bill = get_object_or_404(HostelBillDetail, id=bill_id)

    # Check if the user is a warden
    if request.user.is_staff:  # Adjust this condition based on your user model
        # Change the bill status based on the payment
        if bill.paid_amount >= bill.total_amount:
            bill.status = 'paid'
        else:
            bill.status = 'partially_paid'

        # Save the updated status
        bill.save()

    return redirect('list_bills')  