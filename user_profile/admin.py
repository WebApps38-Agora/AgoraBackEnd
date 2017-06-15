from django.contrib import admin
from user_profile.models import Profile
from django.contrib.sites.models import Site

# Register your models here.
admin.register(Profile)

admin.site.unregister(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')

admin.site.register(Site, SiteAdmin)
