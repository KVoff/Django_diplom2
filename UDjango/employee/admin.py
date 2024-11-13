# employee/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, EmployeeProfile
from .forms import EmployeeProfileAdminForm


class EmployeeAdmin(UserAdmin):
    model = Employee
    list_display = ('username', 'is_staff', 'is_superuser')
    search_fields = ('username',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': (
            'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'is_staff',
                'is_superuser',
                'groups', 'user_permissions')}
         ),
    )


class EmployeeProfileAdmin(admin.ModelAdmin):
    form = EmployeeProfileAdminForm
    list_display = ('user', 'position', 'department', 'hire_date')
    search_fields = ('user__username', 'position', 'department')


admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(Employee, EmployeeAdmin)
