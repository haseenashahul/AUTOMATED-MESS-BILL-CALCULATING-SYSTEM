from decimal import Decimal
from django.shortcuts import render
from django.db import IntegrityError
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mess_app.forms import CustomUserForm
from .models import LeaveApplication,HostelBillDetail
from .forms import LeaveApplicationForm


def profile(request):
    return render(request,'student/my-account.html')



@login_required
def edit_profile(request):
    user = request.user  # Get the current user

    if request.method == 'POST':
        # Fetch the form data from the request.POST object
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('ph_no')
        guardian_name = request.POST.get('guard_name')
        address = request.POST.get('address')
        guardian_phone = request.POST.get('guard_phn')
        semester = request.POST.get('sem')  # Assuming semester is an ID

        # Update user attributes
        user.first_name = first_name
        user.last_name = last_name
        user.ph_no = phone_number
        user.guard_name = guardian_name
        user.address = address
        user.guard_phn = guardian_phone
        user.sem = semester  # Assuming user has 'sem' field related to the semester

        # Save the updated user data
        user.save()

        # Redirect to the dashboard after saving
        return redirect('profile')

    # For GET request, return a pre-filled form in the template
    return render(request, 'student/my-account.html')

@login_required
def leave_applications_list(request):
    user = request.user

    # Handle form submission for adding new leave
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave_application = form.save(commit=False)
            leave_application.user = user  # Set the current user as the one applying for leave
            leave_application.save()
            return redirect('leave_applications')  # Redirect after successful submission
    else:
        form = LeaveApplicationForm()

    # If user is admin, show all leave applications
    if user.is_superuser:
        leaves = LeaveApplication.objects.all()
        return render(request, 'warden_leave_list.html', {
        'leaves': leaves,
        
            })
    else:
        leaves = LeaveApplication.objects.filter(user=user)
        return render(request, 'student/leave.html', {
        'leaves': leaves,
        'form': form
            })
    
    return None

   
@login_required  # Ensure the user is logged in
def list_bills(request):
    # Fetch bills based on whether the user is an admin or not
    if request.user.is_staff:  # Admin users can see all bills
        bills = HostelBillDetail.objects.all()
        return render(request, 'generatedBills.html', {'bills': bills})
    else:  # Regular users can only see their own bills
        bills = HostelBillDetail.objects.filter(student=request.user)
        return render(request, 'student/fees.html', {'bills': bills})





@login_required 
def accept_payment(request, bill_id):
    bill = get_object_or_404(HostelBillDetail, id=bill_id)  # Use get_object_or_404 for better error handling
    transaction_id = request.POST.get('transaction_id')
    amount = Decimal(request.POST.get('amount'))  # Ensure amount is a Decimal

    # Update paid_amount and due, but do not change the status
    bill.paid_amount = (bill.paid_amount or Decimal(0)) + amount  # Ensure to start with Decimal(0)
    
    # Calculate the due amount without changing the status
    bill.due = bill.total_amount - bill.paid_amount if bill.total_amount > bill.paid_amount else Decimal(0)
    
    # Save transaction ID
    bill.transactionID = transaction_id
    
    # Save the updated bill details
    bill.save()

    # Redirect to the appropriate view
    return redirect('list_bills') 