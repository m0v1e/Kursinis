from django.contrib import admin
from .models import Mechanic, Owner, CarInfo, CarStatus

class CarStatusInline(admin.TabularInline):
    model = CarStatus
    readonly_fields = ('id',)
    can_delete = False
    extra = 0

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'display_cars')

class CarInfoAdmin(admin.ModelAdmin):
    list_display = ('car', 'plate', 'car_owner', 'mechanic')
    inlines = [CarStatusInline]

class CarStatusAdmin(admin.ModelAdmin):
    list_display = ('car', 'status', 'owner', 'due_finish')
    list_editable = ('status', 'due_finish')
    list_filter = ('status', 'due_finish')
    search_fields = ('id', 'car__car')

    fieldsets = (
        ('Bendra', {'fields' : ('uuid', 'car')}),
        ('Suruošta', {'fields' : ('status', 'due_finish', 'owner')})
    )

# Register your models here.

admin.site.register(Mechanic)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(CarInfo, CarInfoAdmin)
admin.site.register(CarStatus, CarStatusAdmin)