from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from app.models import Vehicle, Production, VehicleProduction


def index(request):
    vehicle_name = request.GET.get("vehicle_name", "")
    vehicles = Vehicle.objects.filter(status=1)

    if vehicle_name:
        vehicles = vehicles.filter(name__icontains=vehicle_name)

    draft_production = get_draft_production()

    context = {
        "vehicle_name": vehicle_name,
        "vehicles": vehicles
    }

    if draft_production:
        context["vehicles_count"] = len(draft_production.get_vehicles())
        context["draft_production"] = draft_production

    return render(request, "home_page.html", context)


def add_vehicle_to_draft_production(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)

    draft_production = get_draft_production()

    if draft_production is None:
        draft_production = Production.objects.create()
        draft_production.owner = get_current_user()
        draft_production.date_created = timezone.now()
        draft_production.save()

    if VehicleProduction.objects.filter(production=draft_production, vehicle=vehicle).exists():
        return redirect("/")

    item = VehicleProduction(
        production=draft_production,
        vehicle=vehicle
    )
    item.save()

    return redirect("/")


def vehicle_details(request, vehicle_id):
    context = {
        "vehicle": Vehicle.objects.get(id=vehicle_id)
    }

    return render(request, "vehicle_page.html", context)


def delete_production(request, production_id):
    if not Production.objects.filter(pk=production_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM vehicle_production WHERE production_id = %s", [production_id])
        cursor.execute("DELETE FROM productions WHERE id = %s", [production_id])

    return redirect("/")


def production(request, production_id):
    if not Production.objects.filter(pk=production_id).exists():
        return redirect("/")

    context = {
        "production": Production.objects.get(id=production_id),
    }

    return render(request, "production_page.html", context)


def get_draft_production():
    return Production.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()