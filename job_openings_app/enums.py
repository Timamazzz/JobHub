from enum import Enum


class JobType(Enum):
    VACANCY = 'Вакансия'
    INTERNSHIP = 'Стажировка'


class JobCategory(Enum):
    MUNICIPAL_SERVICE = 'Муниципальная служба'


class JobActivity(Enum):
    VOLUNTEERING = 'Волонтерство'
    SALES = 'Продажи'
    IT_SPECIALTIES = 'IT-специальности'
    MEDICINE = 'Медицина'
    MUNICIPAL_SERVICE = 'Муниципальная служба'
    COURIERS = 'Курьеры'
    AGRICULTURE = 'Сельское хозяйство'
