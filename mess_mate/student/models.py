from calendar import monthrange
from django.db import models
from mess_app.models import CustomUser
# from django.utils import timezone
# from django.contrib.auth import get_user_model
# from mess_app.models import HostelBillSettings,Employee
# from datetime import date

# Create your models here.
class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # The user applying for leave (CustomUser)
    purpose = models.CharField(max_length=255)  # Purpose of the leave
    description = models.TextField()  # Description of the leave
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Status of the application
    applied_date = models.DateTimeField(auto_now_add=True)  # Automatically sets the date when the leave is applied
    start_date = models.DateField()  # Leave start date
    end_date = models.DateField()  # Leave end date

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.purpose}"

    class Meta:
        ordering = ['-applied_date'] 





class HostelBillDetail(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_details = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)
    billing_month = models.DateField()
    electricity = models.IntegerField(null=True,blank=True)
    broadband = models.IntegerField(null=True,blank=True)
    maintenence =models.IntegerField(null=True,blank=True)
    total = models.IntegerField(null=True,blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Change to DecimalField for precision
    transactionID = models.TextField(blank=True, default='')  # Store multiple transaction IDs

    status = models.CharField(max_length=20, choices=[
        ('paid', 'Paid'),
        ('mark_as_paid', 'mark_as_paid'),
        ('partially_paid', 'partially_paid'),
        ('unpaid','unpaid')
    ], default='unpaid')  # Default status set to 'unpaid'
    
    due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Amount due

    def __str__(self):
        return f"Bill for {self.student.first_name} {self.student.last_name} for {self.billing_month.strftime('%B %Y')}: {self.total_amount}"

    class Meta:
        ordering = ['-generated_date']





