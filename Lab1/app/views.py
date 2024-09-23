from django.shortcuts import render

vehicles = [
    {
        "id": 1,
        "name": "Титановый шаробалонн",
        "description": "В августе 2018 года было сообщено, что первая товарная партия титановых шаробаллонов (ТШБ) для ракет-носителей «Ангара» отправлена с Воронежского механического завода (ВМЗ) в ПО «Полёт». Это первый комплект ТШБ российского производства: до 2014 года для российских ракет-носителей их поставлял завод «Южмаш» (Украина).",
        "price": 50,
        "category": "Дополнительные запчасти",
        "image": "http://localhost:9000/images/1.png"
    },
    {
        "id": 2,
        "name": "Разгонный блок 'Бриз-М'",
        "description": "В качестве верхней ступени предусмотрено применение разгонных блоков: «Бриз-КМ», «Бриз-М», кислородно-водородный среднего класса (КВСК) и кислородно-водородный тяжёлого класса (КВТК).",
        "price": 124,
        "category": "Разгонные блоки",
        "image": "http://localhost:9000/images/2.png"
    },
    {
        "id": 3,
        "name": "Центральная вычислительная машина 'Бисер-6'",
        "description": "Носитель тяжелого класса «Ангара-5А» имеет первую ступень, образованную из пяти блоков на основе универсального ракетного модуля. Пять двигателей первой ступени запускаются при старте ракеты одновременно.",
        "price": 44,
        "category": "Электроника",
        "image": "http://localhost:9000/images/3.png"
    },
    {
        "id": 4,
        "name": "Боковой ракетный модуль - урм 1",
        "description": "«Бисер-6» предназначен для управления движением и бортовыми системами, а также для контроля полёта и формирования телеметрической информации. При решении задач навигации и наведения с помощью «Бисера-6» выполняются арифметические и логические операции, а также операции обмена информацией с внешними абонентами.",
        "price": 67,
        "category": "Универсальные ракетные модули",
        "image": "http://localhost:9000/images/4.png"
    },
    {
        "id": 5,
        "name": "Центральный ракетный модуль",
        "description": "В основу семейства носителей «Ангара» положен универсальный ракетный модуль (УРМ). В его состав входит блок баков окислителя, горючего и двигатель РД-191.",
        "price": 32,
        "category": "Универсальные ракетные модули",
        "image": "http://localhost:9000/images/5.png"
    },
    {
        "id": 6,
        "name": "Головной обтекатель",
        "description": "Задача головных обтекателей ракет-носителей – на момент старта и до вывода в космическое пространство – это защита космического аппарата от всех внешних факторов. Максимальной температурой головного обтекателя считается 175 градусов Цельсия по поверхности.",
        "price": 54,
        "category": "Головные модули",
        "image": "http://localhost:9000/images/6.png"
    }
]

draft_production = {
    "id": 123,
    "status": "Черновик",
    "date_created": "12 сентября 2024г",
    "weight": "862",
    "vehicles": [
        {
            "id": 1,
            "count": 2
        },
        {
            "id": 2,
            "count": 4
        },
        {
            "id": 3,
            "count": 1
        }
    ]
}


def getProductById(vehicle_id):
    for vehicle in vehicles:
        if vehicle["id"] == vehicle_id:
            return vehicle


def getProducts():
    return vehicles


def searchProducts(vehicle_name):
    res = []

    for vehicle in vehicles:
        if vehicle_name.lower() in vehicle["name"].lower():
            res.append(vehicle)

    return res


def getDraftProduction():
    return draft_production


def getProductionById(production_id):
    return draft_production


def index(request):
    vehicle_name = request.GET.get("vehicle_name", "")
    vehicles = searchProducts(vehicle_name) if vehicle_name else getProducts()
    draft_production = getDraftProduction()

    context = {
        "vehicles": vehicles,
        "vehicle_name": vehicle_name,
        "vehicles_count": len(draft_production["vehicles"]),
        "draft_production": draft_production
    }

    return render(request, "home_page.html", context)


def vehicle(request, vehicle_id):
    context = {
        "id": vehicle_id,
        "vehicle": getProductById(vehicle_id),
    }

    return render(request, "vehicle_page.html", context)


def production(request, production_id):
    production = getProductionById(production_id)
    vehicles = [
        {**getProductById(vehicle["id"]), "count": vehicle["count"]}
        for vehicle in production["vehicles"]
    ]

    context = {
        "production": production,
        "vehicles": vehicles
    }

    return render(request, "production_page.html", context)
