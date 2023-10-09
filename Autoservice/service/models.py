from django.db import models
import uuid 

# Create your models here.

class Mechanic(models.Model):
    name = models.CharField('Autoserviso darbuotojas', max_length=100, help_text='Įveskite serviso darbuotojo varda ir pavarde')

    def __str__(self):
        return self.name


Types = (
    ('diesel', 'Diesel'),
    ('petrol', 'Petrol'),
    ('gas', 'Gas'),
    ('electric', 'Electric'),
    )

class CarInfo(models.Model):
    car = models.CharField('Automobilio marke ir modelis', max_length=100)
    fuel_type = models.CharField(max_length=8, choices=Types, default='Petrol')
    engine = models.CharField(max_length=4, help_text='Automobilio darbinis turis cm3') 
    manufacture_year = models.DateField(auto_now=False, auto_now_add=False)
    plate = models.CharField('Automobilio numeriai', max_length=10)
    vin = models.CharField('Automobilio VIN kodas', max_length=17)
    failure = models.TextField('Automobilio gedimo aprasymas', max_length=1000, help_text='Trumpas gedimu aprasymas')
    mechanic = models.ForeignKey('Mechanic', on_delete=models.SET_NULL, null=True, help_text='Serviso darbuotojas atliekantis darbus')
    car_image = models.ImageField('Car image', upload_to='cars', null=True)

    def __str__(self):
        return f'{self.car} {self.plate}'
    
class Owner(models.Model):
    owner_name = models.CharField('Automobilio savininko vardas', max_length=20)
    owner_surname = models.CharField('Automobilio savininko pavarde', max_length=20)
    owner_car = models.ForeignKey('CarInfo', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.owner_name} {self.owner_surname}'

class CarStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus ID kiekvienam automobiliui')
    car = models.ForeignKey('CarInfo', on_delete=models.SET_NULL, null=True)
    due_finish = models.DateField('Automobilis planuojamas suremontuoti', null=True, blank=True)

    CAR_STATUS = (
        ('w', 'Laukia darbų pradžios'),
        ('i', 'Vyksta automobilio inspektavimas'),
        ('r', 'Remontuojamas automobilis'),
        ('f', 'Automobilis suremontuotas')
    )

    status = models.CharField(
        max_length=1,
        choices=CAR_STATUS,
        blank=True,
        default='w',
        help_text='Statusas',
    )
    class Meta:
        ordering = ['due_finish']

    def __str__(self):
        return f'{self.id} ({self.car})'