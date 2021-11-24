from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import CustomUser
from django.core.management.base import BaseCommand


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Basic'),{'fields':('Full_Name','Gender','Marital_Status','Mother_Tongue','Mobile_No')}),
        # ,'date_of_birth'
        # (_("Physical Information"),{'fields':('Height','Complexion','Physical_Status','Body_Type')}),
        # (_("Professional Information"),{'fields':('Educational_Qualification','Employed_In','Occupation','Income')}),
        # (_('Astrology'),{'fields':('Astro_chart',)}),
        # (_("Culture"),{'fields':('Religious','Caste','Sub_Caste','Gothram')}),
        # (_("Location"),{"fields":('City','Taluk','District','State','Country')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','is_superuser')}
        ),
    )
    list_display = ('id','email', 'first_name', 'last_name', 'is_staff','is_superuser','is_active')
    list_filter = ('email', 'is_staff', 'is_active',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)



