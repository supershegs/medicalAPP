from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomeView.as_view(), name = 'index'),
    path("login", LoginView.as_view(), name = 'login'),
    path("register", RegisterView.as_view(), name = 'register'),
    path('dashboard', dashboardView.as_view(), name= 'dashboard'),
    path('profile', profileView.as_view(), name='profile'),
    path('image', imageView.as_view(), name= 'image'),
    path('history', historyView.as_view(), name='history'),
    path('reminder',reminderView.as_view(), name='reminder' ),
    path('reminder/create_appointment',create_appointmentView.as_view(), name='reminder_create_appointment' ),
    path('reminder/create_reminder',create_reminderView.as_view(), name='reminder_create_reminder'),
    path('consultants', consultant_listView.as_view(), name='consultant_list'),
    path('consultant/create', consultantView.as_view(), name='consultant_create'),
    path('health_information', HealthInformationView.as_view(), name='health_information'),
    path('health_information_creation', HealthInformationCreate.as_view(), name='health_information_creation'),
    path('health_information_update/<int:pk>/', HealthInformationUpdate.as_view(),name='health_information_update'),
    # path('consultants/add/', views.add_health_information, name='add_health_information'),
    path('activitiesTracker', activityView.as_view(), name='activitiesTracker'),
    path('logout', logoutView.as_view(), name='logout'),
    path('video', VideoView.as_view(), name='recommended_video'),
    path('about', AboutView.as_view(), name= 'about'),
    path('booking', bookView.as_view(), name='booking'),
    path('bookinglist', bookinglistView.as_view(), name='bookinglist'),
    path('deletelist', DeleteBookingView.as_view(), name= 'deletelist')
    # path('user', Userview.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

