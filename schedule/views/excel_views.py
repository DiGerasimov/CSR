from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
from django.db import transaction

from ..models import *
from ..excel.export_utils import export_student_schedule_to_excel, export_all_students_to_excel
from ..excel.import_utils import upload_students_excel

@swagger_auto_schema(
    method='get',
    operation_description="Экспорт расписания Обучающиеся в Excel",
    responses={200: 'Excel файл с расписанием', 400: 'Ошибка при создании файла', 404: 'Обучающиеся не найден'}
)
@api_view(['GET'])
def export_student_schedule_to_excel_view(request, student_id):
    return export_student_schedule_to_excel(request, student_id)

@swagger_auto_schema(
    method='get',
    operation_description="Экспорт информации о всех Обучающиеся в Excel с фильтрацией по возрастной группе",
    manual_parameters=[
        openapi.Parameter('age_group', openapi.IN_QUERY, description="Возрастная группа", type=openapi.TYPE_STRING, enum=[choice[0] for choice in Student.AGE_GROUP_CHOICES]),
    ],
    responses={200: 'Excel файл со списком обучающиеся', 400: 'Ошибка при создании файла'}
)
@api_view(['GET'])
def export_all_students_to_excel_view(request):
    return export_all_students_to_excel(request)

@swagger_auto_schema(
    method='post',
    operation_description="Загрузка Excel-файла с данными обучающиеся",
    manual_parameters=[
        openapi.Parameter(
            name="file",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description="Excel файл с данными обучающиеся"
        ),
    ],
    responses={200: 'Данные успешно загружены', 400: 'Ошибка при обработке файла'}
)
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_students_excel_view(request):
    return upload_students_excel(request)

    
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from ..models import Specialist
from ..excel.export_utils import export_specialist_schedule_to_excel

@swagger_auto_schema(
    method='get',
    operation_description="Экспорт расписания специалиста в Excel",
    manual_parameters=[
        openapi.Parameter('period', openapi.IN_QUERY, description="Период расписания", type=openapi.TYPE_STRING, enum=['all', 'week', 'month']),
    ],
    responses={200: 'Excel файл с расписанием', 400: 'Ошибка при создании файла', 404: 'Специалист не найден'}
)
@api_view(['GET'])
def export_specialist_schedule_to_excel_view(request, specialist_id):
    specialist = get_object_or_404(Specialist, id=specialist_id)
    period = request.GET.get('period', 'all')
    
    now = timezone.now()
    if period == 'week':
        start_date = now - timedelta(days=now.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == 'month':
        start_date = now.replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    else:  # 'all'
        start_date = None
        end_date = None
    
    return export_specialist_schedule_to_excel(specialist, start_date, end_date)