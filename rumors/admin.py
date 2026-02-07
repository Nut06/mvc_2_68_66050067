from django.contrib import admin
from .models import User, Rumour, Report


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'role']
    list_filter = ['role']


@admin.register(Rumour)
class RumourAdmin(admin.ModelAdmin):
    list_display = ['rumour_id', 'title', 'status', 'credibility_score', 'created_date']
    list_filter = ['status']
    list_editable = ['status']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'rumour', 'report_type', 'report_date']
    list_filter = ['report_type']
