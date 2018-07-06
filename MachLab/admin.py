from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from MachLab.models import Userinfo
class UserinfoInline(admin.StackedInline):
    model = Userinfo
    can_delete = False
    verbose_name_plural = 'Userinfos'

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    #form = UserChangeForm
    #add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        #('Personal info', {'fields': ('bio','url','location',)}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    #add_fieldsets = (
    #    (None, {
    #        'classes': ('wide',),
    #        'fields': ('email', 'username', 'password', 'location')}
    #    ),
    #)
    inlines = (UserinfoInline,)
    search_fields = ('email','username')
    ordering = ('email','username')
    filter_horizontal = ()

# Now register the new UserAdmin...
#admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)