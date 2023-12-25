
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from .models import Citizen

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)


from .google_sheets import insert_data_to_database

from .models import Citizen
from .google_sheets import read_data_from_google_sheets


def import_google_sheets_data(modeladmin, request, queryset):
    for citizen in queryset:
        insert_data_to_database(citizen)
    modeladmin.message_user(request, "Data imported from Google Sheets for selected Citizens.")


import_google_sheets_data.short_description = "Import Data from Google Sheets"


@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'name', 'email', 'address', 'phone', 'adhar', 'epic', 'no_response')
    search_fields = ('timestamp', 'name', 'email', 'address', 'phone', 'adhar', 'epic', 'no_response')
    ordering = ["timestamp"]




