from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Mechanic, Owner, CarInfo, CarStatus
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

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'car_count' : car_count,
        'waiting_service' : waiting_service,
        'inspection_service' : inspection_service,
        'repair_service' : repair_service,
        'finish_service' : finish_service,
        'num_visits' : num_visits,
    }

    return render(request, 'index.html', context=context)

def search(request):
    query = request.GET.get('query')
    search_results = CarInfo.objects.filter(Q(car__icontains=query) | Q(plate__icontains=query))
    return render(request, 'search.html', {'cars' : search_results, 'query' : query})

def owners(request):

    paginator = Paginator(Owner.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_owners = paginator.get_page(page_number)
    context = {
        'owners' : paged_owners
    }
    return render(request, 'owners.html', context=context)

def owner(request, owner_id):
    owner = get_object_or_404(Owner, pk=owner_id)
    context = {
        'owner' : owner
    }
    return render(request, 'owner.html', context=context)

class CarListView(generic.ListView):
    model = CarInfo, CarStatus
    template_name = 'car_list.html'
    context_object_name = 'car_list'
    queryset = CarInfo.objects.all()
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)
        context['data'] = 'random text'
        return context
    
class CarDetailView(generic.DetailView):
    model = CarInfo
    template_name = 'car_detail.html'
