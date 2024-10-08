from rest_framework import serializers
from .models import Student, Relative, Specialist, Position
from django.utils.translation import gettext as _
from rest_framework import serializers


class RelativeSerializer(serializers.ModelSerializer):
    relation_display = serializers.SerializerMethodField()
    gender_display = serializers.SerializerMethodField()

    class Meta:
        model = Relative
        fields = ['full_name', 'gender_display', 'relation', 'relation_display']

    def get_relation_display(self, obj):
        return obj.get_relation_display()

    def get_gender_display(self, obj):
        return obj.get_gender_display()

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['name']

class StudentListSerializer(serializers.ModelSerializer):
    age_group_display = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'age_group', 'age_group_display']

    def get_age_group_display(self, obj):
        return obj.get_age_group_display()

from rest_framework import serializers
from .models import Student, Relative, Specialist, Position, Schedule, Room
from django.utils.translation import gettext as _
from datetime import date, datetime

class StudentDetailSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    relatives = RelativeSerializer(many=True, read_only=True)
    gender_display = serializers.SerializerMethodField()
    age_group_display = serializers.SerializerMethodField()
    capacity_status_display = serializers.SerializerMethodField()
    attendance_status_display = serializers.SerializerMethodField()
    family_composition_display = serializers.SerializerMethodField()
    family_category_display = serializers.SerializerMethodField()
    payment_type_display = serializers.SerializerMethodField()
    is_city_display = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'full_name', 'status_display', 'gender_display', 'birth_date', 'age_group_display',
            'debts', 'note', 'residence_address', 'registration_address', 'is_city_display',
            'contact_phone', 'capacity_status_display', 'attendance_status_display',
            'has_education', 'has_additional_education', 'additional_education_name',
            'has_sports', 'sports_name', 'has_other_social_services',
            'refused_diagnostics', 'refused_photo', 'contract_number', 'contract_date',
            'ippsu_number', 'ippsu_date', 'certificate_202n', 'disability_group', 'disease',
            'ipra_number', 'ipra_date', 'limitation_degree', 'mse_number', 'mse_date',
            'family_composition_display', 'family_category_display', 'payment_type_display',
            'has_summer_camp', 'summer_camp_note', 'relatives',
            'district', 'parent_contract_number', 'parent_contract_date', 'parent_ippsu_number',
            'parent_ippsu_date', 'parent_certificate_202n_date', 'pmpk_date', 'pmpk_number',
            'loyalty', 'specialist_change_refusal'
        ]

    def get_specialists(self, obj):
        schedules = Schedule.objects.filter(students=obj)
        specialists = set()
        for schedule in schedules:
            specialists.update(schedule.specialists.all())
        return [{'full_name': specialist.full_name, 'position': specialist.position.name if specialist.position else None} for specialist in specialists]

    def get_gender_display(self, obj):
        return obj.get_gender_display()

    def get_age_group_display(self, obj):
        return obj.get_age_group_display()

    def get_capacity_status_display(self, obj):
        return obj.get_capacity_status_display()

    def get_attendance_status_display(self, obj):
        return obj.get_attendance_status_display()

    def get_family_composition_display(self, obj):
        return obj.get_family_composition_display()

    def get_family_category_display(self, obj):
        return obj.get_family_category_display()

    def get_payment_type_display(self, obj):
        return obj.get_payment_type_display()

    def get_is_city_display(self, obj):
        return _("Город") if obj.is_city else _("Село")

    def get_status_display(self, obj):
        return obj.get_status_display()
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        field_names = {
            'id': _("ID"),
            'full_name': _("ФИО"),
            'status_display': _("Статус"),
            'gender_display': _("Пол"),
            'birth_date': _("Дата рождения"),
            'age_group_display': _("Возрастная группа"),
            'debts': _("Долги"),
            'note': _("Примечание"),
            'residence_address': _("Адрес проживания"),
            'registration_address': _("Адрес прописки"),
            'is_city_display': _("Город/село"),
            'contact_phone': _("Контактный телефон"),
            'capacity_status_display': _("Установление недееспособности"),
            'attendance_status_display': _("Отметка посещаемости"),
            'has_education': _("Образование"),
            'has_additional_education': _("Доп.образование / Кружки"),
            'additional_education_name': _("Название кружков"),
            'has_sports': _("Спорт"),
            'sports_name': _("Название спорта"),
            'has_other_social_services': _("Услуги соцзащиты в др. учреждениях"),
            'refused_diagnostics': _("Отказ от диагностики СП"),
            'refused_photo': _("Отказ от фото"),
            'contract_number': _("№ Договора"),
            'contract_date': _("Дата договора"),
            'ippsu_number': _("№ ИППСУ"),
            'ippsu_date': _("Дата ИППСУ"),
            'certificate_202n': _("Справка 202Н"),
            'disability_group': _("Группа инвалидности"),
            'disease': _("Заболевание"),
            'ipra_number': _("№ИПРА"),
            'ipra_date': _("Дата ИПРА"),
            'limitation_degree': _("Степень ограничений"),
            'mse_number': _("МСЭ №"),
            'mse_date': _("Дата МСЭ"),
            'family_composition_display': _("Состав семьи"),
            'family_category_display': _("Категория семьи"),
            'payment_type_display': _("Оплата услуг"),
            'has_summer_camp': _("Лагерь/лето"),
            'summer_camp_note': _("Лагерь/лето примечание"),
            'relatives': _("Родственники"),
            'district': _("Район"),
            'parent_contract_number': _("№ Договора родителя"),
            'parent_contract_date': _("Дата договора родителя"),
            'parent_ippsu_number': _("№ ИППСУ родителя"),
            'parent_ippsu_date': _("Дата ИППСУ родителя"),
            'parent_certificate_202n_date': _("Справка 202Н дата выдачи родителя"),
            'pmpk_date': _("ПМПК дата"),
            'pmpk_number': _("ПМПК номер"),
            'loyalty': _("Лояльность"),
            'specialist_change_refusal': _("Отказ от замены специалиста"),
        }

        boolean_fields = [
            'has_additional_education', 'has_sports', 'has_other_social_services',
            'refused_diagnostics', 'refused_photo', 'has_summer_camp',
            'loyalty', 'specialist_change_refusal'
        ]
        for field in boolean_fields:
            ret[field] = _("Да") if ret[field] else _("Нет")

        date_fields = ['birth_date', 'contract_date', 'ippsu_date', 'ipra_date', 'mse_date',
                       'parent_contract_date', 'parent_ippsu_date', 'parent_certificate_202n_date', 'pmpk_date']
        for field in date_fields:
            if ret[field]:
                if isinstance(ret[field], (date, datetime)):
                    ret[field] = ret[field].strftime("%d.%m.%Y")
                elif isinstance(ret[field], str):
                    pass
                else:
                    pass

        for key, value in ret.items():
            if value is None or value == "":
                ret[key] = _("-")

        return {field_names.get(key, key): value for key, value in ret.items()}
    
class SpecialistListSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    gender_display = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = ['id', 'full_name', 'gender_display', 'position']

    def get_gender_display(self, obj):
        return obj.get_gender_display()

class SpecialistDetailSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    gender_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = ['id', 'full_name', 'gender_display', 'position', 'status_display']

    def get_gender_display(self, obj):
        return obj.get_gender_display()

    def get_status_display(self, obj):
        return obj.get_status_display()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        field_names = {
            'id': _("id"),
            'full_name': _("ФИО"),
            'status_display': _("Статус"),
            'gender_display': _("Пол"),
            'position': _("Должность"),
        }

        # Обработка пустых полей
        for key, value in ret.items():
            if value is None or value == "":
                ret[key] = _("-")

        # Обработка поля position
        if 'position' in ret and ret['position']:
            ret['position'] = ret['position']['name']

        return {field_names.get(key, key): value for key, value in ret.items()}
    
class AgeGroupSerializer(serializers.Serializer):
    value = serializers.CharField()
    display = serializers.CharField()
    
class StudentRelativesSerializer(serializers.ModelSerializer):
    relatives = RelativeSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['relatives']
        
        

from rest_framework import serializers
from .models import Schedule, Student, Specialist, Room, Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['student', 'is_present']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name']

class ScheduleSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField()
    students = StudentSerializer(many=True)
    specialists = serializers.StringRelatedField(many=True)
    attendances = AttendanceSerializer(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'name', 'room', 'students', 'specialists', 'time_start', 'time_end', 'attendances']