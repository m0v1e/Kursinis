from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('owners/', views.owners, name='owners'),
    path('owners/<int:owner_id>', views.owner, name='owner'),
    path('cars/', views.CarListView.as_view(), name='cars'),
    path('cars/<int:pk>', views.CarDetailView.as_view(), name='car-detail'),
    path('search/', views.search, name='search'),
]