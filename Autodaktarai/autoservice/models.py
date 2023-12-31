from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date
import pytz
utc=pytz.UTC
from tinymce.models import HTMLField
from PIL import Image

# Create your models here.

class Mechanic(models.Model):
    name = models.CharField('Autoserviso darbuotojas', max_length=100, help_text='Įveskite serviso darbuotojo vardą ir pavardę')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Mechanikas'
        verbose_name_plural = "Mechanikai"


Types = (
    ('diesel', 'Diesel'),
    ('petrol', 'Petrol'),
    ('gas', 'Gas'),
    ('electric', 'Electric'),
    )

class CarInfo(models.Model):
    car = models.CharField('Automobilio markė ir modelis', max_length=100)
    car_owner = models.ForeignKey('Owner', on_delete=models.SET_NULL, null=True, blank=True, related_name='cars')
    fuel_type = models.CharField(max_length=8, choices=Types, default='Petrol')
    engine = models.CharField(max_length=4, help_text='Automobilio darbinis turis cm3') 
    manufacture_year = models.DateField(auto_now=False, auto_now_add=False)
    plate = models.CharField('Automobilio numeriai', max_length=10)
    vin = models.CharField('Automobilio VIN kodas', max_length=17)
    summary = models.TextField('Automobilio gedimo aprasymas', max_length=1000, help_text='Trumpas gedimu aprasymas')
    mechanic = models.ForeignKey('Mechanic', on_delete=models.SET_NULL, null=True, help_text='Serviso darbuotojas atliekantis darbus')
    car_image = models.ImageField('Car image', upload_to='cars', null=True, blank=True)

    def __str__(self):
        return f'{self.car} {self.plate}, Atsakingas darbuotojas: {self.mechanic}.'
    
class Owner(models.Model):
    name = models.CharField('Automobilio savininko vardas', max_length=20)
    surname = models.CharField('Automobilio savininko pavarde', max_length=20)
    car = models.ForeignKey('CarInfo', on_delete=models.SET_NULL, null=True, blank=True,)
    description = HTMLField()

    def __str__(self):
        return f'{self.name} {self.surname}'
    
    def display_cars(self):
        sarasas = [self.car.car for car in self.cars.all()]
        return ','.join(sarasas)

class CarStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus ID kiekvienam automobiliui')
    car = models.ForeignKey('CarInfo', on_delete=models.SET_NULL, null=True)
    due_finish = models.DateField('Automobilis planuojamas suremontuoti', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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
    @property
    def is_overdue(self):
        if self.due_finish and date.today().replace(tzinfo=utc) > self.due_finish.replace(tzinfo=utc):
            return True
        return False
    
class CarReview(models.Model):
    car = models.ForeignKey('Carinfo', on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField("Gedimas", max_length=150)

    class Meta:
        verbose_name = 'Gedimas'
        verbose_name_plural = 'Gedimai'
        ordering = ['-date_created']

class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default='img/no-image.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} profilis'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)