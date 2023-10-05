from django.contrib import admin
from .models import Mechanic, CarInfo

# Register your models here.

class CarInfoAdmin(admin.ModelAdmin):
    list_display = ('car', 'plate', 'mechanic')

admin.site.register(Mechanic)
admin.site.register(CarInfo, CarInfoAdmin)