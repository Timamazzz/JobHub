from enum import Enum


class JobTypeEnum(Enum):
    VACANCY = 'Вакансия'
    INTERNSHIP = 'Стажировка'


class JobCategoryEnum(Enum):
    MUNICIPAL_SERVICE = 'Муниципальная служба'


class JobActivityEnum(Enum):
    VOLUNTEERING = 'Волонтерство'
    SALES = 'Продажи'
    IT_SPECIALTIES = 'IT-специальности'
    MEDICINE = 'Медицина'
    MUNICIPAL_SERVICE = 'Муниципальная служба'
    COURIERS = 'Курьеры'
    AGRICULTURE = 'Сельское хозяйство'


class MunicipalityEnum(Enum):
    BELGOROD_REGION = 'Белгородская область'
    BELGOROD_DISTRICT = 'Белгородский район'
    BELGOROD_CITY = 'Город Белгород'
    ALEXEEVSKY_DISTRICT = 'Алексеевский городской округ'
    BORISOVSKY_DISTRICT = 'Борисовский район'
    VALUY_DISTRICT = 'Валуйский городской округ'
    VEYDELEVSKY_DISTRICT = 'Вейделевский район'
    VOLOKONOVSKY_DISTRICT = 'Волоконовский район'
    GUBKIN_DISTRICT = 'Губкинский городской округ'
    GRAYVORON_DISTRICT = 'Грайворонский городской округ'
    IVNYA_DISTRICT = 'Ивнянский район'
    KOROCHAN_DISTRICT = 'Корочанский район'
    KRASNOGVARDEISKY_DISTRICT = 'Красногвардейский район'
    KRASNOYARUZHSKY_DISTRICT = 'Краснояружский район'
    NOVOOSKOL_DISTRICT = 'Новооскольский городской округ'
    PROKHOROVSKY_DISTRICT = 'Прохоровский район'
    RAKITYANSKY_DISTRICT = 'Ракитянский район'
    ROVENSKY_DISTRICT = 'Ровеньский район'
    STAROOSKOLSKY_DISTRICT = 'Старооскольский городской округ'
    SHEBEKINSKY_DISTRICT = 'Шебекинский городской округ'
    CHERNYANSKY_DISTRICT = 'Чернянский район'
    YAKOVLEVSKY_DISTRICT = 'Яковлевский городской округ'
