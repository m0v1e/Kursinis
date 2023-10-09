from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Mechanic, CarInfo, Owner, CarStatus
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def index(request):

    car_count = CarStatus.objects.all().count()

    waiting_service = CarStatus.objects.filter(status='w').count()
    
    inspection_service = CarStatus.objects.filter(status='i').count()
    
    repair_service = CarStatus.objects.filter(status='r').count()

    finish_service = CarStatus.objects.filter(status='f').count()

    context = {
        'car_count' : car_count,
        'waiting_service' : waiting_service,
        'inspection_service' : inspection_service,
        'repair_service' : repair_service,
        'finish_service' : finish_service
    }

    return render(request, 'index.html', context=context)


def owners(request):
    paginator = Paginator(Owner.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_owners = paginator.get_page(page_number)
    context = {
        'owners' : paged_owners
    }
    print(owners)
    return render(request, 'owners.html', context=context)

def owner(request, owner_id):
    owner = get_object_or_404(Owner, pk=owner_id)

    context = {
        'owner' : owner
    }
    return render(request, 'owner.html', context=context)

def service(request):
    return render(request, 'service.html')

def search(request):
    query = request.GET.get('query')
    search_results = Owner.objects.filter(Q(owner_name__icontains=query) | Q(owner_surname__icontains=query))
    return render(request, 'search.html', {'owners': search_results, 'query' : query})

def cars(request):
    car_list = CarInfo.objects.all()
    context = {
        'car_list' : car_list
    }
    return render(request, 'cars.html', context=context)
