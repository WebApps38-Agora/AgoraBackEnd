from django.contrib import admin
from notifications.models import Notification, NotifiedUsers

admin.site.register(Notification)
admin.site.register(NotifiedUsers)
