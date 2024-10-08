from django.db import models
from uuid import uuid4

from django.utils.translation import gettext_lazy as _



class Student(models.Model):
    CAPACITY_CHOICES = [
        ('capable', _('Дееспособный')),
        ('incapable', _('Недееспособный')),
        ('partially_incapable', _('Частично недееспособный')),
    ]
    ATTENDANCE_CHOICES = [
        ('attends', _('Ходит')),
        ('not_attends', _('Не ходит')),
        ('periodically', _('Периодически')),
    ]
    FAMILY_COMPOSITION_CHOICES = [
        ('complete', _('Полная')),
        ('incomplete', _('Неполная')),
    ]
    FAMILY_CATEGORY_CHOICES = [
        ('large', _('Многодетная')),
        ('low_income', _('Малообеспеченная')),
        ('normal', _('Нормальная')),
    ]
    PAYMENT_CHOICES = [
        ('paid', _('Платно')),
        ('free', _('Бесплатно')),
    ]
    
    GENDER_CHOICES = [
        ('male', _('Мужской')),
        ('female', _('Женский')),
    ]
    AGE_GROUP_CHOICES = [
        ('0-7', _('0-7 лет')),
        ('8-13', _('8-13 лет')),
        ('14-17', _('14-17 лет')),
        ('18', _('18+ лет')),
    ]
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4
    )
    STATUS_CHOICES = [
        ('actual', _('Актуальный')),
        ('in_process', _('В обработке')),
        ('finished', _('Закончил')),
    ]
    full_name = models.TextField(_("ФИО"), max_length=255, default="", blank=True , null=True)
    status = models.CharField(_("Статус"), max_length=20, choices=STATUS_CHOICES, default='actual', blank=True, null=True)
    gender = models.CharField(_("Пол"), max_length=10, choices=GENDER_CHOICES, default='male', blank=True , null=True)
    birth_date = models.DateField(_("Дата рождения"), null=True, blank=True)
    age_group = models.CharField(_("Возрастная группа"), max_length=5, choices=AGE_GROUP_CHOICES, default='18+', blank=True , null=True)
    debts = models.TextField(_("Долги"), default="", blank=True , null=True)
    note = models.TextField(_("Примечание"), blank=True, default="")
    residence_address = models.TextField(_("Адрес проживания"), default="", blank=True , null=True)
    registration_address = models.TextField(_("Адрес прописки"), blank=True , null=True, default="")
    is_city = models.BooleanField(_("Город/село"), choices=[(True, _("Город")), (False, _("Село"))], default=True, blank=True , null=True)
    contact_phone = models.CharField(_("Контактный телефон"), max_length=20, default="", blank=True , null=True)
    capacity_status = models.CharField(_("Установление недееспособности"), max_length=20, choices=CAPACITY_CHOICES, default='capable', blank=True , null=True)
    attendance_status = models.CharField(_("Отметка посещаемости"), max_length=20, choices=ATTENDANCE_CHOICES, default='attends', blank=True , null=True)
    has_education = models.TextField(_("Образование"), help_text=_("Школьное, ср.специальное"), blank=True , null=True, default="")
    has_additional_education = models.BooleanField(_("Доп.образование / Кружки"), default=False, blank=True , null=True)
    additional_education_name = models.TextField(_("Название кружков"), blank=True , null=True, default="")
    has_sports = models.BooleanField(_("Спорт"), default=False, blank=True , null=True)
    sports_name = models.TextField(_("Название спорта"), blank=True , null=True, default="")
    has_other_social_services = models.BooleanField(_("Услуги соцзащиты в др. учреждениях"), default=False, blank=True , null=True)
    refused_diagnostics = models.BooleanField(_("Отказ от диагностики СП"), default=False, blank=True , null=True)
    refused_photo = models.BooleanField(_("Отказ от фото"), default=False, blank=True , null=True)
    contract_number = models.CharField(_("№ Договора"), max_length=200, default="", blank=True , null=True)
    contract_date = models.DateField(_("Дата договора"), null=True, blank=True)
    ippsu_number = models.CharField(_("№ ИППСУ"), max_length=200, default="", blank=True , null=True)
    ippsu_date = models.DateField(_("Дата ИППСУ"), null=True, blank=True)
    certificate_202n = models.CharField(_("Справка 202Н"), max_length=200, default="", blank=True , null=True)
    disability_group = models.CharField(_("Группа инвалидности"), max_length=200, default="", blank=True , null=True)
    disease = models.CharField(_("Заболевание"), max_length=255, default="", blank=True , null=True)
    ipra_number = models.CharField(_("№ИПРА"), max_length=200, default="", blank=True , null=True)
    ipra_date = models.DateField(_("Дата ИПРА"), null=True, blank=True)
    limitation_degree = models.CharField(_("Степень ограничений"), max_length=255, default="", blank=True , null=True)
    mse_number = models.CharField(_("МСЭ №"), max_length=200, default="", blank=True , null=True)
    mse_date = models.DateField(_("Дата МСЭ"), null=True, blank=True)
    family_composition = models.CharField(_("Состав семьи"), max_length=20, choices=FAMILY_COMPOSITION_CHOICES, default='complete', blank=True , null=True)
    family_category = models.CharField(_("Категория семьи"), max_length=20, choices=FAMILY_CATEGORY_CHOICES, default='normal', blank=True , null=True)
    payment_type = models.CharField(_("Оплата услуг"), max_length=20, choices=PAYMENT_CHOICES, default='paid', blank=True , null=True)
    has_summer_camp = models.BooleanField(_("Лагерь/лето"), default=False, blank=True , null=True)
    summer_camp_note = models.TextField(_("Лагерь/лето примечание"), default="", blank=True , null=True)
    relatives = models.ManyToManyField('Relative', related_name='students', verbose_name=_("Родственники"), blank=True)
    district = models.CharField(_("Район"), max_length=255, blank=True, null=True)
    parent_contract_number = models.CharField(_("№ Договора родителя"), max_length=200, blank=True, null=True)
    parent_contract_date = models.DateField(_("Дата договора родителя"), null=True, blank=True)
    parent_ippsu_number = models.CharField(_("№ ИППСУ родителя"), max_length=200, blank=True, null=True)
    parent_ippsu_date = models.DateField(_("Дата ИППСУ родителя"), null=True, blank=True)
    parent_certificate_202n_date = models.DateField(_("Справка 202Н дата выдачи родителя"), null=True, blank=True)
    pmpk_date = models.DateField(_("ПМПК дата"), null=True, blank=True)
    pmpk_number = models.CharField(_("ПМПК номер"), max_length=200, blank=True, null=True)
    loyalty = models.BooleanField(_("Лояльность"), default=True, blank=True, null=True)
    specialist_change_refusal = models.BooleanField(_("Отказ от замены специалиста"), default=False, blank=True, null=True)
    additional_data = models.TextField(_("Дополнительные данные"), blank=True, null=True)


    class Meta:
        verbose_name = _("Обучающиеся")
        verbose_name_plural = _("Обучающиеся")
    def __str__(self) -> str:
        return f"{self.full_name} - ({self.get_age_group_display()})"
     
class Relative(models.Model):
    RELATION_CHOICES = [
        ('parent', _('Родитель')),
        ('legal_representative', _('Законный представитель')),
        ('disabled', _('Брат/сестра')),
    ]
    
    GENDER_CHOICES = [
        ('male', _('Мужской')),
        ('female', _('Женский')),
    ]

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4
    )
    full_name = models.TextField(_("ФИО"), max_length=255, default="", blank=True , null=True)
    gender = models.CharField(_("Пол"), max_length=10, choices=GENDER_CHOICES, default='male', blank=True , null=True)
    relation = models.CharField(_("Отношение"), max_length=200, choices=RELATION_CHOICES, default='parent', blank=True , null=True)

    
    class Meta:
        verbose_name = _("Родственник")
        verbose_name_plural = _("Родственники")
        
    def __str__(self) -> str:
        return f"{self.full_name} ({self.get_relation_display()})"
    
class Specialist(models.Model):
    GENDER_CHOICES = [
        ('male', _('Мужской')),
        ('female', _('Женский')),
    ]
    STATUS_CHOICES = [
        ('staff', _('Штатный')),
        ('guest', _('Гость')),
        ('dismissed', _('Уволен')),
    ]
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4
    )
    full_name = models.TextField(_("ФИО"), max_length=255, default="", blank=True , null=True)
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Должность"), to_field='id')
    status = models.CharField(_("Статус"), max_length=20, choices=STATUS_CHOICES, default='staff', blank=True, null=True)
    gender = models.CharField(_("Пол"), max_length=10, choices=GENDER_CHOICES, default='male', blank=True , null=True)

    class Meta:
        verbose_name = _("Специалист")
        verbose_name_plural = _("Специалисты")

    def __str__(self) -> str:
        return f"{self.full_name} ({self.position.name if self.position else 'Без должности'})"

class Position(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4
    )
    name = models.CharField(_("Название должности"), max_length=255, unique=True, blank=True , null=True)

    class Meta:
        verbose_name = _("Должность")
        verbose_name_plural = _("Должности")
        
    def __str__(self) -> str:
        return self.name
        
class Room(models.Model):
    FLOOR_CHOICES = [
        ('1', _('1')),
        ('2', _('2')),
    ]

    name = models.CharField(_("Название/номер"), max_length=255, default="", blank=True , null=True)
    floor = models.CharField(_("Этаж"), max_length=10, choices=FLOOR_CHOICES, default='1', blank=True , null=True)
    class Meta:
        verbose_name = _("Комната")
        verbose_name_plural = _("Комнаты")
        
    def __str__(self) -> str:
        return f"№ {self.name} ({self.get_floor_display()} этаж)"
        
class Schedule(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4
    )
    name = models.CharField(_("Название занятия"), max_length=255, default="", blank=True , null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Кабинет (номер)"), to_field='id', blank=True , null=True)
    students = models.ManyToManyField(Student, related_name='schedule_students', verbose_name=_("Обучающиеся"), blank=True)
    specialists = models.ManyToManyField(Specialist, verbose_name=_("Специалисты"), blank=True)
    time_start = models.DateTimeField(_("Время начала"), null=True, blank=True)
    time_end = models.DateTimeField(_("Время конца"), null=True, blank=True)


    class Meta:
        verbose_name = _("Расписание")
        verbose_name_plural = _("Расписания")
        
    def __str__(self) -> str:
        return f"№ {self.room} - ({self.time_start}:{self.time_end})"
    
class Attendance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4
    )
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField(_("Присутствовал"), default=False)

    class Meta:
        verbose_name = _("Посещаемость")
        verbose_name_plural = _("Посещаемость")
        unique_together = ('schedule', 'student')

    def __str__(self):
        return f"{self.student.full_name} - {self.schedule} - {'Присутствовал' if self.is_present else 'Отсутствовал'}"