from django.contrib import admin
from .models import Client, Order, Country, Hotel, TravelPackage, Climate, PromoCode
from django import forms


# Настройка отображения модели Client в админке

class StaffOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'promo_code_discount']


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'user', 'address', 'birth_date', 'belarus_phone_number', 'total_orders',
        'total_spent')
    search_fields = ('first_name', 'last_name', 'user__username')

    def total_orders(self, obj):
        return obj.total_orders()

    total_orders.short_description = 'Number of Orders'

    def total_spent(self, obj):
        return obj.total_spent()

    total_spent.short_description = 'Total Spent'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'package', 'departure_date', 'status', 'final_price')
    list_filter = ('status', 'departure_date')
    search_fields = ('client__first_name', 'client__last_name', 'package__name')

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_staff and not request.user.is_superuser:
            kwargs['form'] = StaffOrderForm
        return super().get_form(request, obj, **kwargs)


# Настройка отображения модели Hotel в админке
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'rating', 'standard_room_price', 'vip_room_price')
    list_filter = ('country', 'rating')
    search_fields = ('name', 'country__name')


# Настройка отображения модели Country в админке
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_climate_winter', 'get_climate_spring', 'get_climate_summer', 'get_climate_autumn')

    def get_climate_winter(self, obj):
        return obj.climate_winter.description if obj.climate_winter else 'N/A'

    get_climate_winter.short_description = 'Climate Winter'

    def get_climate_spring(self, obj):
        return obj.climate_spring.description if obj.climate_spring else 'N/A'

    get_climate_spring.short_description = 'Climate Spring'

    def get_climate_summer(self, obj):
        return obj.climate_summer.description if obj.climate_summer else 'N/A'

    get_climate_summer.short_description = 'Climate Summer'

    def get_climate_autumn(self, obj):
        return obj.climate_autumn.description if obj.climate_autumn else 'N/A'

    get_climate_autumn.short_description = 'Climate Autumn'


# Настройка отображения модели TravelPackage в админке
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'country', 'duration_days', 'intermediate_price')
    list_filter = ('hotel', 'country', 'duration_days')
    search_fields = ('name', 'hotel__name', 'country__name')


# Настройка отображения модели Climate в админке
class ClimateAdmin(admin.ModelAdmin):
    list_display = ('season', 'description', 'avg_temperature', 'avg_humidity', 'avg_pressure')
    list_filter = ('season',)
    search_fields = ('description',)


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'valid_from', 'valid_to', 'active')
    search_fields = ('code',)
    list_filter = ('active', 'valid_from', 'valid_to')


admin.site.register(PromoCode, PromoCodeAdmin)

# Регистрация моделей в админке
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(TravelPackage, TravelPackageAdmin)
admin.site.register(Climate, ClimateAdmin)
