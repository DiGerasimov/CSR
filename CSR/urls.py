from django.urls import path
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from schedule.views.student_views import get_students_list, get_student_detail, get_student_age_groups
from schedule.views.specialist_views import get_specialist_detail, get_specialists_list, get_specialist_positions
from schedule.views.common_views import index
from schedule.views.excel_views import export_student_schedule_to_excel_view, export_all_students_to_excel_view, upload_students_excel_view, export_specialist_schedule_to_excel_view
from schedule.views.schedule_views import *

schema_view = get_schema_view(
    openapi.Info(
        title="CSR API",
        default_version='v1',
        description="API для Центра социальной реабилитации",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    
    # Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Student URLs
    path('students/', get_students_list, name='get_students_list'),
    path('students/<uuid:student_id>/', get_student_detail, name='get_student_detail'),
    path('students/age-groups/', get_student_age_groups, name='get_student_age_groups'),
    
    # Specialist URLs
    path('specialists/', get_specialists_list, name='get_specialists_list'),
    path('specialists/<uuid:specialist_id>/', get_specialist_detail, name='get_specialist_detail'),
    path('specialists/positions/', get_specialist_positions, name='get_specialist_positions'),
    path('specialists/<uuid:specialist_id>/export-schedule/', export_specialist_schedule_to_excel_view, name='export_specialist_schedule'),

    # Excel export/import URLs
    path('students/<uuid:student_id>/export-schedule/', export_student_schedule_to_excel_view, name='export_student_schedule'),
    path('students/export-all/', export_all_students_to_excel_view, name='export_all_students'),
    path('students/upload-excel/', upload_students_excel_view, name='upload_students_excel'),
    path('schedule/', get_schedule, name='get_schedule'),
    path('schedule/attendance/', update_attendance, name='update_attendance'),
    path('schedule/duplicate/', duplicate_schedule, name='duplicate_schedule'),

]
