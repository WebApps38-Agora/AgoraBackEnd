from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from user_profile.models import Profile

admin.site.unregister(Site)


class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')


admin.site.register(Site, SiteAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
