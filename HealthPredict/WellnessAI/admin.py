from django.contrib import admin
from WellnessAI.models import Profile, Appointment, Contact, UserDetail, SymptomDetail, Doctor, updateData

# Register your models here.
admin.site.register(Profile)
admin.site.register(Appointment)

# class ContactAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'subject', 'created_at')  # Columns to display in the list view
#     search_fields = ('name', 'email', 'subject')  # Fields to search in the admin interface
#     list_filter = ('created_at',)  # Add filter options

admin.site.register(Contact)
admin.site.register(UserDetail)
admin.site.register(SymptomDetail)
admin.site.register(Doctor)
admin.site.register(updateData)