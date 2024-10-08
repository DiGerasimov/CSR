import pandas as pd
from datetime import datetime, timedelta
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

from ..models import Student

def parse_date(date_string):
    if pd.isna(date_string):
        return None
    
    date_string = str(date_string)
    
    if date_string.isdigit():
        try:
            return (datetime(1900, 1, 1) + timedelta(days=int(date_string) - 2)).date()
        except ValueError:
            return None
    
    match = re.search(r'\d{2}.\d{2}.\d{4}', date_string)
    if match:
        try:
            return datetime.strptime(match.group(), '%d.%m.%Y').date()
        except ValueError:
            return None
    
    return None

def get_capacity_status(value):
    if pd.isna(value):
        return 'capable'
    value = str(value).lower()
    if 'недееспособный' in value:
        return 'incapable'
    elif 'частично' in value:
        return 'partially_incapable'
    return 'capable'

def get_attendance_status(value):
    if pd.isna(value):
        return 'attends'
    value = str(value).lower()
    if 'не ходит' in value:
        return 'not_attends'
    elif 'периодически' in value:
        return 'periodically'
    return 'attends'

def get_family_composition(value):
    if pd.isna(value):
        return 'complete'
    return 'incomplete' if 'неполная' in str(value).lower() else 'complete'

def get_family_category(value):
    if pd.isna(value):
        return 'normal'
    value = str(value).lower()
    if 'многодетная' in value:
        return 'large'
    elif 'малообеспеченная' in value:
        return 'low_income'
    return 'normal'

def get_payment_type(value):
    if pd.isna(value):
        return 'paid'
    return 'free' if 'бесплатно' in str(value).lower() else 'paid'

def get_age_group(birth_date):
    if pd.isna(birth_date):
        return '18'
    birth_date = parse_date(birth_date)
    if birth_date is None:
        return '18'
    age = (datetime.now().date() - birth_date).days // 365
    if age < 8:
        return '0-7'
    elif age < 14:
        return '8-13'
    elif age < 18:
        return '14-17'
    return '18'

def upload_students_excel(request):
    try:
        excel_file = request.FILES['file']
        
        xls = pd.ExcelFile(excel_file)
        
        sheet_names = xls.sheet_names
        
        with transaction.atomic():
            for sheet_name in sheet_names:
                df = pd.read_excel(xls, sheet_name)
                
                age_group = None
                if '0-7' in sheet_name:
                    age_group = '0-7'
                elif '8-13' in sheet_name:
                    age_group = '8-13'
                elif '14-17' in sheet_name:
                    age_group = '14-17'
                elif '18+' in sheet_name:
                    age_group = '18'
                
                for _, row in df.iterrows():
                    student_data = {
                        'full_name': row['Ф.И.О.'] if 'Ф.И.О.' in df.columns else '',
                        'birth_date': parse_date(row['Дата рождения']) if 'Дата рождения' in df.columns else None,
                        'debts': row['Долги'] if 'Долги' in df.columns and pd.notna(row['Долги']) else '',
                        'note': row['Примечание'] if 'Примечание' in df.columns and pd.notna(row['Примечание']) else '',
                        'residence_address': row['Адрес проживания / Адрес прописки'].split('/')[0].strip() if 'Адрес проживания / Адрес прописки' in df.columns and pd.notna(row['Адрес проживания / Адрес прописки']) else '',
                        'registration_address': row['Адрес проживания / Адрес прописки'].split('/')[1].strip() if 'Адрес проживания / Адрес прописки' in df.columns and pd.notna(row['Адрес проживания / Адрес прописки']) and '/' in row['Адрес проживания / Адрес прописки'] else '',
                        'is_city': row['Город / село'].lower() == 'город' if 'Город / село' in df.columns and pd.notna(row['Город / село']) else True,
                        'contact_phone': row['Контактный телефон'] if 'Контактный телефон' in df.columns and pd.notna(row['Контактный телефон']) else '',
                        'capacity_status': get_capacity_status(row['Установление недееспособности']) if 'Установление недееспособности' in df.columns else 'capable',
                        'attendance_status': get_attendance_status(row['Отметка посещаемости']) if 'Отметка посещаемости' in df.columns else 'attends',
                        'has_education': row['Образование (школьное, ср.специальное)'] if 'Образование (школьное, ср.специальное)' in df.columns and pd.notna(row['Образование (школьное, ср.специальное)']) else '',
                        'has_additional_education': pd.notna(row['Доп.образование / Кружки']) and row['Доп.образование / Кружки'].lower() != 'нет' if 'Доп.образование / Кружки' in df.columns else False,
                        'has_sports': pd.notna(row['Спорт']) and row['Спорт'].lower() != 'нет' if 'Спорт' in df.columns else False,
                        'has_other_social_services': pd.notna(row['Услуги соцзащиты в др. учреждениях']) and row['Услуги соцзащиты в др. учреждениях'].lower() != 'нет' if 'Услуги соцзащиты в др. учреждениях' in df.columns else False,
                        'refused_diagnostics': pd.notna(row['Отказ от диагностики СП']) and row['Отказ от диагностики СП'].lower() == 'отказ' if 'Отказ от диагностики СП' in df.columns else False,
                        'refused_photo': pd.notna(row['Отказ от фото']) and row['Отказ от фото'].lower() == 'отказ' if 'Отказ от фото' in df.columns else False,
                        'contract_number': row['№  Договора'] if '№  Договора' in df.columns and pd.notna(row['№  Договора']) else '',
                        'contract_date': parse_date(row['Дата догорова']) if 'Дата догорова' in df.columns else None,
                        'ippsu_number': row['№ ИППСУ'] if '№ ИППСУ' in df.columns and pd.notna(row['№ ИППСУ']) else '',
                        'ippsu_date': parse_date(row['Дата ИППСУ']) if 'Дата ИППСУ' in df.columns else None,
                        'certificate_202n': row['Справка 202Н'] if 'Справка 202Н' in df.columns and pd.notna(row['Справка 202Н']) else '',
                        'disability_group': row['Группа инвалидности'] if 'Группа инвалидности' in df.columns and pd.notna(row['Группа инвалидности']) else '',
                        'disease': row['Заболевание'] if 'Заболевание' in df.columns and pd.notna(row['Заболевание']) else '',
                        'ipra_number': row['№ИПРА'] if '№ИПРА' in df.columns and pd.notna(row['№ИПРА']) else '',
                        'ipra_date': parse_date(row['Дата ИПРА']) if 'Дата ИПРА' in df.columns else None,
                        'limitation_degree': row['Степень ограничений'] if 'Степень ограничений' in df.columns and pd.notna(row['Степень ограничений']) else '',
                        'mse_number': row['МСЭ № и дата'].split()[1] if 'МСЭ № и дата' in df.columns and pd.notna(row['МСЭ № и дата']) and len(row['МСЭ № и дата'].split()) > 1 else '',
                        'mse_date': parse_date(row['МСЭ № и дата']) if 'МСЭ № и дата' in df.columns else None,
                        'family_composition': get_family_composition(row['Состав семьи']) if 'Состав семьи' in df.columns else 'complete',
                        'family_category': get_family_category(row['Категория семьи']) if 'Категория семьи' in df.columns else 'normal',
                        'payment_type': get_payment_type(row['Оплата услуг']) if 'Оплата услуг' in df.columns else 'paid',
                        'has_summer_camp': pd.notna(row['Лагерь/лето']) and row['Лагерь/лето'].lower() != 'нет' if 'Лагерь/лето' in df.columns else False,
                        'summer_camp_note': row['Лагерь/лето'] if 'Лагерь/лето' in df.columns and pd.notna(row['Лагерь/лето']) else '',
                        'age_group': age_group or get_age_group(row['Дата рождения']) if 'Дата рождения' in df.columns and pd.notna(row['Дата рождения']) else '18',
                    }
                    
                    if student_data['full_name']:
                        Student.objects.update_or_create(
                            full_name=student_data['full_name'],
                            defaults=student_data
                        )
        
        return Response({'message': 'Данные успешно загружены'}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)