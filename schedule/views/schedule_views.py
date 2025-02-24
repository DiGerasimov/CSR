from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime, timedelta
from django.db.models import Q
from django.utils import timezone

from ..models import *
from ..serializers import ScheduleSerializer, SpecialistListSerializer

@swagger_auto_schema(
    method='get',
    operation_description="Получение расписания",
    manual_parameters=[
        openapi.Parameter('start_date', openapi.IN_QUERY, description="Начальная дата", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        openapi.Parameter('end_date', openapi.IN_QUERY, description="Конечная дата", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        openapi.Parameter('specialist_id', openapi.IN_QUERY, description="ID специалиста", type=openapi.TYPE_STRING),
        openapi.Parameter('position', openapi.IN_QUERY, description="Должность специалиста", type=openapi.TYPE_STRING),
        openapi.Parameter('view', openapi.IN_QUERY, description="Вид отображения (week/month)", type=openapi.TYPE_STRING),
        openapi.Parameter('all', openapi.IN_QUERY, description="Выгрузить все расписание", type=openapi.TYPE_BOOLEAN),
    ],
    responses={200: ScheduleSerializer(many=True)}
)
@api_view(['GET'])
def get_schedule(request):
    try:
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        specialist_id = request.query_params.get('specialist_id')
        position = request.query_params.get('position')
        view = request.query_params.get('view', 'week')
        all_schedules = request.query_params.get('all', '').lower() == 'true'

        if all_schedules:
            schedules = Schedule.objects.all()
        else:
            if not start_date:
                start_date = timezone.now().date()
            else:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            if not end_date:
                if view == 'week':
                    end_date = start_date + timedelta(days=6)
                elif view == 'month':
                    end_date = start_date.replace(day=1) + timedelta(days=32)
                    end_date = end_date.replace(day=1) - timedelta(days=1)
            else:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            schedules = Schedule.objects.filter(
                Q(time_start__date__range=[start_date, end_date]) |
                Q(time_end__date__range=[start_date, end_date])
            )

        if specialist_id:
            schedules = schedules.filter(specialists__id=specialist_id)

        if position:
            schedules = schedules.filter(specialists__position__name=position)

        serializer = ScheduleSerializer(schedules, many=True)
        schedule_data = serializer.data

        # Обновляем информацию о посещаемости
        for schedule in schedule_data:
            attendances = Attendance.objects.filter(schedule_id=schedule['id'])
            schedule['attendances'] = [
                {
                    'student_id': str(attendance.student.id),
                    'is_present': attendance.is_present
                } for attendance in attendances
            ]

        return Response(schedule_data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Schedule, Attendance, Student
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    operation_description="Обновление посещаемости для нескольких студентов",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['schedule_id', 'attendances'],
        properties={
            'schedule_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            'attendances': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'student_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
                        'is_present': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                )
            ),
        },
    ),
    responses={200: "Посещаемость успешно обновлена", 400: "Неверные данные"}
)
@api_view(['POST'])
def update_attendance(request):
    try:
        schedule_id = request.data.get('schedule_id')
        attendances = request.data.get('attendances', [])

        schedule = get_object_or_404(Schedule, id=schedule_id)
        
        for attendance_data in attendances:
            student_id = attendance_data.get('student_id')
            is_present = attendance_data.get('is_present')
            
            student = get_object_or_404(Student, id=student_id)
            
            Attendance.objects.update_or_create(
                schedule=schedule,
                student=student,
                defaults={'is_present': is_present}
            )

        return Response({"message": "Посещаемость успешно обновлена"}, status=status.HTTP_200_OK)
    except Schedule.DoesNotExist:
        return Response({"error": "Расписание не найдено"}, status=status.HTTP_404_NOT_FOUND)
    except Student.DoesNotExist:
        return Response({"error": "Студент не найден"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_description="Дублирование карточки расписания на следующие недели",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['schedule_id', 'weeks_count'],
        properties={
            'schedule_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            'weeks_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Количество недель для дублирования"),
        },
    ),
    responses={200: "Карточки успешно дублированы", 400: "Неверные данные"}
)
@api_view(['POST'])
def duplicate_schedule(request):
    try:
        schedule_id = request.data.get('schedule_id')
        weeks_count = int(request.data.get('weeks_count', 1))
        
        if weeks_count <= 0 or weeks_count > 52:  # Ограничение на количество недель (максимум год)
            return Response({"error": "Некорректное количество недель"}, status=status.HTTP_400_BAD_REQUEST)
            
        original_schedule = Schedule.objects.get(id=schedule_id)
        
        duplicated_schedules = []
        
        for week in range(1, weeks_count + 1):
            # Вычисляем новые даты начала и окончания (смещение на week недель)
            # Используем осведомленные о часовом поясе объекты datetime
            new_start_time = original_schedule.time_start + timedelta(weeks=week)
            new_end_time = original_schedule.time_end + timedelta(weeks=week)
            
            # Проверяем, существует ли уже карточка с такими же параметрами
            existing_schedule = Schedule.objects.filter(
                name=original_schedule.name,
                room=original_schedule.room,
                time_start=new_start_time,
                time_end=new_end_time
            ).first()
            
            if existing_schedule:
                continue  # Пропускаем создание дубликата
                
            # Создаем новую карточку расписания
            new_schedule = Schedule.objects.create(
                name=original_schedule.name,
                room=original_schedule.room,
                time_start=new_start_time,
                time_end=new_end_time,
                additional_info=original_schedule.additional_info
            )
            
            # Копируем связи со специалистами
            for specialist in original_schedule.specialists.all():
                new_schedule.specialists.add(specialist)
                
            # Копируем связи со студентами
            for student in original_schedule.students.all():
                new_schedule.students.add(student)
                
            # Не копируем посещаемость, как указано в требованиях
            
            duplicated_schedules.append(str(new_schedule.id))
        
        return Response({
            "message": f"Успешно создано {len(duplicated_schedules)} копий карточки расписания",
            "duplicated_schedules": duplicated_schedules
        }, status=status.HTTP_200_OK)
        
    except Schedule.DoesNotExist:
        return Response({"error": "Расписание не найдено"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)