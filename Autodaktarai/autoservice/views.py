from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from .models import Mechanic, Owner, CarInfo, CarStatus
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import CarReviewForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. pa6tu {email} jau užregistruotas')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} sėkmingai užregistruotas')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')

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
    
class CarDetailView(FormMixin, generic.DetailView):
    model = CarInfo
    template_name = 'car_detail.html'
    form_class = CarReviewForm

    def get_success_url(self):
        return reverse('car-detail', kwargs={'pk': self.object.id})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        form.instance.car = self.object
        form.instance.owner = self.request.user
        form.save()
        return super(CarDetailView, self).form_valid(form)


class OwnedCarsByUserListView(LoginRequiredMixin, generic.ListView):
    model = CarStatus
    template_name = 'user_cars.html'
    paginate_by = 10


    def get_queryset(self):
        return CarStatus.objects.filter(owner=self.request.user).order_by('due_finish')

@login_required
def profilis(request):
    return render(request, 'profilis.html')