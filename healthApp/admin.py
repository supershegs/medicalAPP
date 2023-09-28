
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Appointment, Reminder,Consultant, HealthInformation
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('name', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone_no', 'age', 'address', 'nationality',
                           'emergency_contact_name', 'emergency_contact_no', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')})
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'phone_no', 'age', 'address', 'nationality', 'emergency_contact_name', 'emergency_contact_no', 'avatar', 'is_staff', 'is_active')
        }),
    )

    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Appointment)
admin.site.register(Reminder)
admin.site.register(Consultant)
admin.site.register(HealthInformation)
