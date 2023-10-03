import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import *
from .models import *

from rest_framework import status

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import get_user_model


from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from decouple import config

from django.conf import settings
from isodate import parse_duration

from django.http import HttpResponseForbidden


# from django.http import HttpResponseRedirect

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated



# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


class AboutView(APIView):
    def get(self, request): 
        return render(request, 'about.html')
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
            appointments = Appointment.objects.filter(user=request.user)
            reminders = Reminder.objects.filter(user=request.user)
            health_info_list = HealthInformation.objects.filter(user=request.user)
            return render(request, 'dashboard.html', 
                          {'appointments': appointments,
                           'reminders': reminders,
                           'health_info_list': health_info_list
                           })
        return redirect('index')



class profileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request,'profile.html')
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
    

class HealthInformationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            health_info_list = HealthInformation.objects.filter(user= request.user)
            return render(request, 'health_information.html', {'health_info_list': health_info_list})
        else:
            return redirect('login')  # Redirect to login page if user is not authenticated
class HealthInformationCreate(View):
    def get(self, request):
        if request.user.is_authenticated:
            health_info_list = HealthInformation.objects.filter(user=request.user)
            if not health_info_list.exists():
                consultants =   Consultant.objects.all()
                return render(request, 'health_information_creation.html', {'consultants': consultants})
            else:
                print(health_info_list)
                return redirect('history')       
        else:
            return redirect('login')  
    
    def post(self, request):
        if request.user.is_authenticated:
            health_info_list = HealthInformation.objects.filter(user=request.user)
            if not health_info_list.exists():
                print('empty list')
                form = HealthInformationForm(request.POST, request.FILES)
                consultants =   Consultant.objects.all()

                if form.is_valid():
                    health_info = form.save(commit=False)
                    health_info.user = request.user
                    health_info.save()
                    return redirect('history')
                else:
                    print('invalid form submitted')
            else: 
                return redirect('history')
        else:
            return redirect('login')
        return render(request,'health_information_creation.html',  {
            'form': form,
            'consultants': consultants})
class HealthInformationUpdate(View): 
    def get(self, request, pk):
        if request.user.is_authenticated:
            health_info = HealthInformation.objects.get(pk=pk)
            print(health_info)
            if health_info.user == request.user:
                form = HealthInformationForm(instance=health_info)
                return render(request, 'health_information_update.html', {'form': form})
            else:
                return HttpResponseForbidden("You do not have permission to update this record.")
        else:
            return redirect('login')  
           
    def post(self, request, pk):
        if request.user.is_authenticated:
            health_info = HealthInformation.objects.filter(user=request.user,pk=pk)
            form = HealthInformationForm(request.POST, instance=health_info)
            consultants =   Consultant.objects.all()
            if form.is_valid():
                form.save()
                return redirect('health_information')
        else:
            return redirect('login')
        return render(request,'health_information_update.html',  
                      {'form': form,
                'health_info': health_info,
                'consultants': consultants} )



class logoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('login')

    
class historyView(View):
    def get(self, request):
        health_info_list = HealthInformation.objects.filter(user=request.user)
        if not health_info_list.exists():
            print('empty list')
            health_info_list = ''
        if request.user.is_authenticated:
            return render(request,'history.html', {'health_info_list': health_info_list})
        return redirect('index')

class activityView(View):
    def get(self, request):
        if request.user.is_authenticated:
            
            reminders = Reminder.objects.filter(user=request.user)
            reminder = Reminder.objects.filter(user=request.user).first()
        
            search_url = 'https://www.googleapis.com/youtube/v3/search'
            vides_ids = []
            video_url = 'https://www.googleapis.com/youtube/v3/videos'
            videos_list = []
            search_params = {
                'part': 'snippet',
                'q': 'how to improve your health and lifestyle',
                'key': settings.YOUTUBE_DATA_API_KEY,
                'maxResults': 3,
                'type': 'video'
            }
            res = requests.get(search_url, params=search_params)
            results = res.json()['items']
            for result in results:
                vides_ids.append(result['id']['videoId'])
            video_params = {
                'part': 'snippet, contentDetails',
                'key': settings.YOUTUBE_DATA_API_KEY,
                'id': ','.join(vides_ids)
            }
            res = requests.get(video_url, params=video_params)
            results = res.json()['items']
            for result in results:
                video_data = {
                    'title': result['snippet']['title'],
                    'id': result['id'],
                    'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                    'duration': parse_duration(result['contentDetails']['duration']),
                    'thumbnail': result['snippet']['thumbnails']['high']['url']

                }
                videos_list.append(video_data)
            videos = {
                'videos': videos_list
            }
            return render(request, 'activitiesTracker.html', context={'reminders': reminders, **videos})

        return redirect('index')    
            
class VideoView(View):  
    def get(self, request):
        if request.user.is_authenticated:
            search_url = 'https://www.googleapis.com/youtube/v3/search'
            vides_ids = []
            video_url = 'https://www.googleapis.com/youtube/v3/videos'
            videos_list = []
            search_params = {
                'part': 'snippet',
                'q': 'how to improve your health and lifestyle',
                'key': settings.YOUTUBE_DATA_API_KEY,
                'maxResults': 10,
                'type': 'video'
            }
            res = requests.get(search_url, params=search_params)
            # print(res.json()) res.json()['items']['id']['videoId']
            results = res.json()['items']
            # print(results)
            for result in results:
                # print(result['id']['videoId']) to pick the video ID
                vides_ids.append(result['id']['videoId'])

            video_params = {
                'part': 'snippet, contentDetails',
                'key': settings.YOUTUBE_DATA_API_KEY,
                'id': ','.join(vides_ids)
            }
            res = requests.get(video_url, params=video_params)
            results = res.json()['items']
            for result in results:
                video_data = {
                    'title': result['snippet']['title'],
                    'id': result['id'],
                    'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                    'duration': parse_duration(result['contentDetails']['duration']),
                    'thumbnail': result['snippet']['thumbnails']['high']['url']

                }
                videos_list.append(video_data)
            videos = {
                'videos': videos_list
            }
            return render(request, 'video.html', context= videos)
        return redirect('index')
        
    def post(self, request):
        if request.user.is_authenticated:
            search_url = 'https://www.googleapis.com/youtube/v3/search'
            vides_ids = []
            video_url = 'https://www.googleapis.com/youtube/v3/videos'
            videos_list = []
            search_params = {
                'part': 'snippet',
                'q': request.POST['search'],
                'key': settings.YOUTUBE_DATA_API_KEY,
                'maxResults': 10,
                'type': 'video'
            }
            res = requests.get(search_url, params=search_params)
            results = res.json()['items']
            for result in results:
                vides_ids.append(result['id']['videoId'])


            video_params = {
                'part': 'snippet, contentDetails',
                'key': settings.YOUTUBE_DATA_API_KEY,
                'id': ','.join(vides_ids)
            }
            res = requests.get(video_url, params=video_params)
            results = res.json()['items']
            for result in results:
                video_data = {
                    'title': result['snippet']['title'],
                    'id': result['id'],
                    'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                    'duration': parse_duration(result['contentDetails']['duration']),
                    'thumbnail': result['snippet']['thumbnails']['high']['url']

                }
                videos_list.append(video_data)
            videos = {
                'videos': videos_list
            }
            return render(request, 'video.html', context= videos)
        return redirect('index')

class bookinglistView(View):
    def get(self, request):
        if request.user.is_authenticated:
            bookings = Booking.objects.filter(user=request.user).first()
            return render(request, 'bookinglist.html', {'bookings': bookings})
    def post(self, request):
        import pdb
        pdb.set_trace()
        bookings = Booking.objects.filter(user=request.user).first()
        if bookings and bookings.user == request.user:
            form = BookingForm(request.POST, instance=bookings)  # Pass the instance to the form
            if form.is_valid():
                form.save()  # This will update the existing booking
                return redirect('bookinglist')
            else:
                return render(request, 'bookinglist.html', {'form': form, 'booking': bookings})
        return redirect('booking_list')

    
class bookView(View):
    def get(self, request):
        if request.user.is_authenticated:
            consultants =   Consultant.objects.all()
            return render(request,'booking.html', {'consultants': consultants})
        return redirect('index')
    def post(self, request):
        if request.user.is_authenticated:
            consultants =   Consultant.objects.all()
            form = BookingForm(request.POST)
            bookings = Booking.objects.filter(user=request.user)
            if not bookings.exists():
                if not consultants.exists():
                    error = 'No active consultant'
                    return render(request,'booking.html', {'error': error})
                else: 
                    if form.is_valid():
                        booking = form.save(commit=False)
                        booking.user = request.user
                        booking.save()
                        message = 'Successfully booked we will contact you shortly'
                        return render(request, 'bookinglist.html', {'message': message})
                    return render(request,'booking.html', {'form': form, 'consultants': consultants})
            else:
                message= 'You have a pending booking, you can not create new booking, awaiting approval'
                return render(request, 'bookinglist.html', {'bookings': bookings, 'message': message})
                
class DeleteBookingView(View):
    def post(self, request):
        import pdb
        pdb.set_trace()
        if request.user.is_authenticated:
            booking = Booking.objects.filter(user=request.user).first()
            if booking and booking.user == request.user:
                booking.delete()
            return redirect('booking')  

# class UpdateBookingView(View):
#     def get(self, request):
#         booking = Booking.objects.filter(user=request.user).first()
#         if booking and booking.user == request.user:
#             form = BookingForm(instance=booking)
#             return render(request, 'update_booking.html', {'form': form, 'booking': booking})
#         return redirect('booking')
    