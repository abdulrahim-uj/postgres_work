from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'username',
                    'is_admin', 'is_staff', 'is_superadmin', 'is_active', 'is_deleted',
                    'created_date', 'modified_date')
    ordering = ('-date_joined',)
    list_display_links = ('email', 'username')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, CustomUserAdmin)


class UserProfileAdminView(admin.ModelAdmin):
    list_display = ('id', 'auto_id', 'user', 'address',
                    'country', 'state', 'city', 'pin_code',
                    'landmark', 'creator', 'updater', 'created_at', 'modified_at',
                    'is_deleted')
    ordering = ('-created_at',)
    list_display_links = ('user', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(UserProfile, UserProfileAdminView)
