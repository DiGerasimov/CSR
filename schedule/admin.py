from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from .models import *
from django.utils.html import format_html

class CustomImportExportModelAdmin(ImportExportModelAdmin):
    def get_import_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    search_fields = ['full_name', 'contact_phone', 'contract_number', 'ippsu_number']
    list_filter = ['age_group', 'is_city', 'capacity_status', 'attendance_status', 'has_additional_education', 'has_sports', 'has_other_social_services', 'refused_diagnostics', 'refused_photo', 'family_composition', 'family_category', 'payment_type', 'has_summer_camp']
    list_display = ['full_name', 'birth_date', 'contact_phone', 'capacity_status', 'attendance_status']
    filter_horizontal = ['relatives']  # Добавлено для выбора родственников

@admin.register(Relative)
class RelativeAdmin(ImportExportModelAdmin):
    search_fields = ['full_name', 'relation']
    list_filter = ['relation']
    list_display = ['full_name', 'relation']


@admin.register(Specialist)
class SpecialistAdmin(ImportExportModelAdmin):
    search_fields = ['full_name', 'position']
    list_filter = ['position']
    list_display = ['full_name', 'position']

@admin.register(Room)
class RoomAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_filter = ['floor']

@admin.register(Position)
class PositionAdmin(ImportExportModelAdmin):
    search_fields = ['name']

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1
    
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'time_start', 'time_end', 'room', 'display_attendance_summary']
    list_filter = ['time_start', 'time_end', 'room', 'specialists']
    search_fields = ['name', 'room__name', 'specialists__full_name']
    filter_horizontal = ['students', 'specialists']
    
    readonly_fields = ['display_attendance_detail']
    inlines = [AttendanceInline]

    def display_attendance_summary(self, obj):
        attendances = Attendance.objects.filter(schedule=obj)
        total = attendances.count()
        present = attendances.filter(is_present=True).count()
        return f"Присутствует: {present}/{total}"
    
    display_attendance_summary.short_description = "Посещаемость"

    def display_attendance_detail(self, obj):
        attendances = Attendance.objects.filter(schedule=obj)
        attendance_info = [f"{att.student.full_name}: {'Присутствует' if att.is_present else 'Отсутствует'}" for att in attendances]
        return format_html("<br>".join(attendance_info))
    
    display_attendance_detail.short_description = "Детальная посещаемость"
    
@admin.register(Attendance)
class AttendanceAdmin(CustomImportExportModelAdmin):
    list_display = ['schedule', 'student', 'is_present']
    list_filter = ['schedule', 'is_present']
    search_fields = ['student__full_name', 'schedule__name']

admin.site.site_header = _("Администрирование CSR")
admin.site.site_title = _("Панель администратора CSR")
admin.site.index_title = _("Добро пожаловать в панель администратора CSR")