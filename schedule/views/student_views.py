from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import *
from ..serializers import StudentListSerializer, StudentDetailSerializer, AgeGroupSerializer

@swagger_auto_schema(
    method='get',
    operation_description="Получение списка обучающиеся с фильтрацией по возрастной группе",
    manual_parameters=[
        openapi.Parameter('age_group', openapi.IN_QUERY, description="Возрастная группа", type=openapi.TYPE_STRING, enum=[choice[0] for choice in Student.AGE_GROUP_CHOICES]),
    ],
    responses={200: StudentListSerializer(many=True)}
)
@api_view(['GET'])
def get_students_list(request):
    try:
        students = Student.objects.all().order_by('full_name')

        age_group = request.query_params.get('age_group')
        if age_group in dict(Student.AGE_GROUP_CHOICES):
            students = students.filter(age_group=age_group)

        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="Получение полной информации о обучающиеся по ID",
    responses={200: StudentDetailSerializer(), 404: 'обучающиеся не найден'}
)
@api_view(['GET'])
def get_student_detail(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)
        serializer = StudentDetailSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({'error': 'обучающиеся не найден'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="Получение списка возрастных групп обучающиеся",
    responses={200: AgeGroupSerializer(many=True)}
)
@api_view(['GET'])
def get_student_age_groups(request):
    try:
        age_groups = [{'value': choice[0], 'display': choice[1]} for choice in Student.AGE_GROUP_CHOICES]
        serializer = AgeGroupSerializer(age_groups, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)