from django.contrib import admin
from .models import CarMake, Dealer, CarModel


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "description")
    search_fields = ("name", "country")
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "car_make", "car_type", "year", "dealer")
    list_filter = ("car_make", "car_type", "year")
    search_fields = ("name", "car_make__name")


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "city", "state", "zip", "phone", "email")
    list_filter = ("state",)
    search_fields = ("full_name", "short_name", "city", "state", "zip")
