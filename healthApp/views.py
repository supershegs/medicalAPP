import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import CustomUserCreationForm, AppointmentForm, reminderForm,ConsultantForm,HealthInformationForm
from .models import Appointment, Reminder, Consultant,HealthInformation

from rest_framework import status

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import get_user_model


# from django.http import HttpResponseRedirect

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated



# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')
    
class RegisterView(APIView):
    def get(self, request): 
        return render(request, 'signup.html')
    
    def post(self, request):
        
        password = request.POST.get('password1')
        updated_data = request.POST.copy()
        updated_data['password'] = password
        form = CustomUserCreationForm(updated_data, request.FILES)

        if form.is_valid():
            user = form.save()
            token, created = Token.objects.get_or_create(user=user)
            message= 'Registration successful'
            # return redirect('login', {'message': message})
            # login(request, user) 
            # return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
            # return redirect('dashboard')
            login_url = reverse('login') + f'?message={message}'
            return redirect(login_url)
        return render(request, 'signup.html', {'form': form})
        # return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
 
class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            error = 'Please provide both email and password.'
            return render(request, 'login.html', {'error': error})

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            token = token.key  
            if token is not None:
                return redirect('dashboard')
            else:
                print("User is not authenticated with a token")
        else:
            error = 'Invalid credentials'
            return render(request, 'login.html', {'error': error})

            
class dashboardView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'dashboard.html')
        return redirect('index')


class profileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request,'profile.html')
        return redirect('index')

class historyView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request,'history.html')
        return redirect('index')

class imageView(View):
    def get(self, request):
        return render(request,'image.html')
    
class create_appointmentView(View):
    def get(self,request):
         if request.user.is_authenticated:
            appointments = Appointment.objects.filter(user=request.user)
            return render(request,'create_appointment.html',  {'appointments': appointments})
    
    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('reminder')
        return render(request, 'create_appointment.html', {'form': form})
    
class create_reminderView(View):
    def get(self,request):
         if request.user.is_authenticated:
            reminders = Reminder.objects.filter(user=request.user)
            return render(request,'create_reminder.html',  {'reminders': reminders})
    
    def post(self, request):
        form = reminderForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('reminder')
        return render(request, 'create_reminder.html', {'form': form})
        

class reminderView(View):
    def get(self, request):
        if request.user.is_authenticated:
            appointments = Appointment.objects.filter(user=request.user)
            reminders = Reminder.objects.filter(user=request.user)
            return render(request, 'reminder.html', {'appointments': appointments, 'reminders': reminders})
        return redirect('index')
    

class consultant_listView(View):
    def get(self, request):
        consultants =   Consultant.objects.all()
        return render(request, 'consultant_list.html', {'consultants': consultants})
class consultantView(View):
    def get(self, request):
        return render(request, 'create_consultant.html')
    
    def post(self, request):
        form = ConsultantForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('consultant_list')
        return render(request, 'create_consultant.html', {'form': form})
    

class health_information(View):
    def get(self, request):
        pass


class logoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('login')

    


        
        