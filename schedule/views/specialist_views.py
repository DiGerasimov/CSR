from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import Specialist, Position
from ..serializers import SpecialistListSerializer, SpecialistDetailSerializer, PositionSerializer

@swagger_auto_schema(
    method='get',
    operation_description="Получение полной информации о специалисте по ID",
    responses={200: SpecialistDetailSerializer(), 404: 'Специалист не найден'}
)
@api_view(['GET'])
def get_specialist_detail(request, specialist_id):
    try:
        specialist = get_object_or_404(Specialist, id=specialist_id)
        serializer = SpecialistDetailSerializer(specialist)
        return Response(serializer.data)
    except Specialist.DoesNotExist:
        return Response({'error': 'Специалист не найден'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="Получение списка специалистов с фильтрацией по должности",
    manual_parameters=[
        openapi.Parameter('position', openapi.IN_QUERY, description="Должность", type=openapi.TYPE_STRING),
    ],
    responses={200: SpecialistListSerializer(many=True)}
)
@api_view(['GET'])
def get_specialists_list(request):
    try:
        specialists = Specialist.objects.all().order_by('full_name')

        position = request.query_params.get('position')
        if position:
            specialists = specialists.filter(position__name=position)

        serializer = SpecialistListSerializer(specialists, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="Получение списка должностей специалистов",
    responses={200: PositionSerializer(many=True)}
)
@api_view(['GET'])
def get_specialist_positions(request):
    try:
        positions = Position.objects.all()
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)