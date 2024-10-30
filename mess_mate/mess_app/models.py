from django.contrib.auth.models import AbstractUser
from django.db import models

# from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
       # Add new fields here
       GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
       COURSE_CHOICES = [
        ('CSE', 'B.Tech(Computer Science Engineering) '),
        ('EC', 'B.Tech(Electronics & Communication Engineering)'),
        ('EEE', 'B.Tech(Electrical & Electronics Engineering)'),
        ('CHE', 'Diploma in Computer Hardware Engineering'),
        ('EL', 'Diploma in Electronics Engineering'),
        ('DEEE', 'Diploma in Electrical & Electronics Engineering'),
        ('MCA', 'MCA'),
    ]   
       email = models.EmailField(unique=True)
       dob=models.DateField(blank=False, null=True)
       gender=models.CharField(max_length=1, choices=GENDER_CHOICES,blank=False, null=True)
       address=models.TextField(blank=False, null=True)
       course = models.CharField(max_length=4, choices=COURSE_CHOICES,blank=False, null=True)
       reg_no=models.CharField(max_length=15,unique=True,blank=False, null=True)
       sem=models.PositiveIntegerField(blank=False, null=True)
       start_year = models.IntegerField(blank=False,null=True)
       end_year = models.IntegerField(blank=False,null=True)
       ph_no=models.CharField(max_length=15,blank=False, null=True)
       guard_name=models.CharField(max_length=100,blank=False, null=True)
       guard_phn=models.CharField(max_length=15,blank=False, null=True)
       is_active = models.BooleanField(default=False)
       past_stud= models.BooleanField(default=False,blank=True,null=True)
       
       
       def __str__(self):
          return self.first_name




class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.CharField(max_length=100)
    ph_no=models.CharField(max_length=15,blank=False, null=True)
    joined_date =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class EmployeeLeave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    reason = models.TextField()
    added_date =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leave for {self.employee.first_name}"
    



class HostelBillSettings(models.Model):
    perDay_fixedCharge = models.DecimalField(max_digits=10, decimal_places=2)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    electricity = models.DecimalField(max_digits=10, decimal_places=2)
    broadband = models.DecimalField(max_digits=10, decimal_places=2)
    maintenance = models.DecimalField(max_digits=10, decimal_places=2)
    emp_salary = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f"Hostel Bill Settings: Rent - {self.rent},Employee salary -{self.emp_salary} , Electricity - {self.electricity}, Broadband - {self.broadband}, Maintenance - {self.maintenance}"


    class Meta:
        verbose_name = "Hostel Bill Settings"
        verbose_name_plural = "Hostel Bill Settings"



class Expenditure(models.Model):
    EXPENDITURE_TYPES = [
        ('grocery', 'Grocery'),
        ('food', 'Food'),
        ('utility', 'Utility'),
        ('maintenance', 'Maintenance'),
        ('salary', 'Staff Salary'),
        ('miscellaneous', 'Miscellaneous'),
    ]
    
    expenditure_date = models.DateField()  # Date of the expenditure
    expenditure_type = models.CharField(max_length=20,choices=EXPENDITURE_TYPES)  # Type of expenditure
    description = models.TextField()  # Optional description of the expenditure
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount spent
    bill_image = models.ImageField(upload_to='bills/')  # Optional field to upload a bill image

    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the timestamp when the record is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updates the timestamp when the record is modified

    def __str__(self):
        return f"{self.expenditure_type} - {self.amount} on {self.expenditure_date}"