from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('owner/', views.owners, name='owners'),
    path('service/', views.service, name='service'),
    path('owners/<int:owner_id>', views.owner, name='owner'),
    path('search/', views.search, name='search'),
    path('cars/', views.cars, name='cars')

]
