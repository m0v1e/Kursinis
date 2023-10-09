from django.contrib import admin
from .models import Mechanic, CarInfo, Owner, CarStatus

# Register your models here.

class CarInfoAdmin(admin.ModelAdmin):
    list_display = ('car', 'plate', 'mechanic')

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'owner_surname', 'owner_car')

admin.site.register(Mechanic)
admin.site.register(CarInfo, CarInfoAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(CarStatus)