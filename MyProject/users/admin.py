from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Customize how the User appears in the Admin
class CustomUserAdmin(UserAdmin):
    model = User
    # This adds your custom fields to the User edit page in Admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_vendor', 'is_customer', 'store_name')}),
    )
    # This adds the fields to the 'Add User' page
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_vendor', 'is_customer', 'store_name')}),
    )

admin.site.register(User, CustomUserAdmin)