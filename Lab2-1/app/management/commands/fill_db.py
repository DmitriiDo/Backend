import random

from django.core.management.base import BaseCommand
from minio import Minio

from ...models import *
from .utils import random_date, random_timedelta


def add_users():
    User.objects.create_user("user", "user@user.com", "1234")
    User.objects.create_superuser("root", "root@root.com", "1234")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234")

    print("Пользователи созданы")


def add_vehicles():
    Vehicle.objects.create(
        name="Титановый шаробалонн",
        category="Дополнительные запчасти",
        description="В августе 2018 года было сообщено, что первая товарная партия титановых шаробаллонов (ТШБ) для ракет-носителей «Ангара» отправлена с Воронежского механического завода (ВМЗ) в ПО «Полёт». Это первый комплект ТШБ российского производства: до 2014 года для российских ракет-носителей их поставлял завод «Южмаш» (Украина).",
        image="images/1.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Разгонный блок 'Бриз-М'",
        category="Разгонные блоки",
        description="В качестве верхней ступени предусмотрено применение разгонных блоков: «Бриз-КМ», «Бриз-М», кислородно-водородный среднего класса (КВСК) и кислородно-водородный тяжёлого класса (КВТК).",
        image="images/2.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Центральная вычислительная машина 'Бисер-6'",
        category="Электроника",
        description="«Бисер-6» предназначен для управления движением и бортовыми системами, а также для контроля полёта и формирования телеметрической информации. При решении задач навигации и наведения с помощью «Бисера-6» выполняются арифметические и логические операции, а также операции обмена информацией с внешними абонентами.",
        image="images/3.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Боковой ракетный модуль - урм 1",
        category="Универсальные ракетные модули",
        description="Носитель тяжелого класса «Ангара-5А» имеет первую ступень, образованную из пяти блоков на основе универсального ракетного модуля. Пять двигателей первой ступени запускаются при старте ракеты одновременно.",
        image="images/4.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Центральный ракетный модуль",
        category="Универсальные ракетные модули",
        description="В основу семейства носителей «Ангара» положен универсальный ракетный модуль (УРМ). В его состав входит блок баков окислителя, горючего и двигатель РД-191.",
        image="images/5.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Головной обтекатель",
        category="Головные модули",
        description="Задача головных обтекателей ракет-носителей – на момент старта и до вывода в космическое пространство – это защита космического аппарата от всех внешних факторов. Максимальной температурой головного обтекателя считается 175 градусов Цельсия по поверхности.",
        image="images/6.png",
        price=random.randint(10, 100)
    )

    client = Minio("minio:9000", "minio", "minio123", secure=False)
    client.fput_object('images', '1.png', "app/static/images/1.png")
    client.fput_object('images', '2.png', "app/static/images/2.png")
    client.fput_object('images', '3.png', "app/static/images/3.png")
    client.fput_object('images', '4.png', "app/static/images/4.png")
    client.fput_object('images', '5.png', "app/static/images/5.png")
    client.fput_object('images', '6.png', "app/static/images/6.png")
    client.fput_object('images', 'default.png', "app/static/images/default.png")

    print("Услуги добавлены")


def add_productions():
    users = User.objects.filter(is_superuser=False)
    moderators = User.objects.filter(is_superuser=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    vehicles = Vehicle.objects.all()

    for _ in range(30):
        status = random.randint(2, 5)
        add_production(status, vehicles, users, moderators)

    add_production(1, vehicles, users, moderators)

    print("Заявки добавлены")


def add_production(status, vehicles, users, moderators):
    production = Production.objects.create()
    production.status = status

    if production.status in [3, 4]:
        production.date_complete = random_date()
        production.date_formation = production.date_complete - random_timedelta()
        production.date_created = production.date_formation - random_timedelta()
    else:
        production.date_formation = random_date()
        production.date_created = production.date_formation - random_timedelta()

    production.owner = random.choice(users)
    production.moderator = random.choice(moderators)

    production.weight = random.randint(1000, 10000)

    for vehicle in random.sample(list(vehicles), 3):
        item = VehicleProduction(
            production=production,
            vehicle=vehicle,
            value=random.randint(1, 10)
        )
        item.save()

    production.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_vehicles()
        add_productions()



















