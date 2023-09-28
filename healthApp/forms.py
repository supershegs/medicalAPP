from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User,Appointment, Reminder, Consultant, HealthInformation

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2', 'phone_no', 'address', 'age', 'nationality', 'emergency_contact_name', 'emergency_contact_no', 'avatar']
		# fields = '__all__'
    password = forms.CharField(widget=forms.PasswordInput)  # Add this line to override the password field

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
    
class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = User
		fields = ['name', 'email', 'phone_no', 'age', 'address', 'nationality', 'emergency_contact_name', 'emergency_contact_no', 'avatar']
		# fields = '__all__'

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'description', 'date', 'time']

class reminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'date', 'time']
        
class ConsultantForm(forms.ModelForm):
    class Meta:
        model = Consultant
        fields = ['name', 'contact_number', 'area_of_specialization', 'avatar']

class HealthInformationForm(forms.ModelForm):
    class Meta:
        model = HealthInformation
        fields = ['health_condition', 'drugs_prescribed', 'complaints','consultant','call_consultant', 'height','body_weight','heart_rate','existing_conditions','blood_group', 'blood_pressure']