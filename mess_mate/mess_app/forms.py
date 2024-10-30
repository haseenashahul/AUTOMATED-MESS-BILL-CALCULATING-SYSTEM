from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,HostelBillSettings,Expenditure
from django import forms

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'dob', 'gender', 'address', 'course',
            'reg_no', 'sem', 'start_year', 'end_year', 'email', 'ph_no',
            'guard_name', 'guard_phn', 'password1', 'password2'
        )
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'reg_no': forms.TextInput(attrs={'class': 'form-control'}),
            'sem': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'end_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'ph_no': forms.TextInput(attrs={'class': 'form-control'}),
            'guard_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guard_phn': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.dob = self.cleaned_data['dob']
        user.gender = self.cleaned_data['gender']
        user.address = self.cleaned_data['address']
        user.course = self.cleaned_data['course']
        user.reg_no = self.cleaned_data['reg_no']
        user.sem = self.cleaned_data['sem']
        user.start_year = self.cleaned_data['start_year']
        user.end_year = self.cleaned_data['end_year']
        user.ph_no = self.cleaned_data['ph_no']
        user.guard_name = self.cleaned_data['guard_name']
        user.guard_phn = self.cleaned_data['guard_phn']
        
        
        if commit:
            user.save()
        return user


# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = ['first_name', 'last_name', 'email', 'salary', 'position','ph_no']


# class EmployeeLeaveForm(forms.ModelForm):
#     class Meta:
#         model = EmployeeLeave
#         fields = ['employee', 'date_from', 'date_to', 'reason']
#         widgets = {
#             'employee': forms.Select(attrs={'class': 'form-control'}),
#             'date_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'date_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter reason', 'rows': 3}),
#         }

class HostelBillSettingsForm(forms.ModelForm):
    class Meta:
        model = HostelBillSettings
        fields = ['perDay_fixedCharge', 'rent', 'electricity', 'broadband', 'maintenance','emp_salary']


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['expenditure_date', 'expenditure_type', 'description', 'amount', 'bill_image']
        
        widgets = {
            'expenditure_date': forms.DateInput(attrs={'type': 'date'}),  # Date picker for the expenditure date
            'expenditure_type': forms.Select(),  # Dropdown for selecting expenditure type
            'description': forms.Textarea(attrs={'rows': 3}),  # Text area for the description field
            'amount': forms.NumberInput(attrs={'step': '0.01'}),  # Number input for amount with decimal step
        }

    # Customizing the form to make the bill image optional
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bill_image'].required = False