from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from cars.models import Car, CarInventory
from cars.forms import CarForm

class CarsView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        cars = super().get_queryset().order_by('model')
        search_model = self.request.GET.get('search_model') 
        if search_model:
            cars = cars.filter(model__icontains=search_model)
        return cars

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_inventory'] = CarInventory.objects.first()
        return context

class CarView(DetailView):
    model = Car
    template_name = 'car_detail.html'

@method_decorator(login_required, name='dispatch')
class NewCarView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'new_car.html'
    success_url = '/cars/'

@method_decorator(login_required, name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_update.html'

    def get_success_url(self):
        # return f'/car/{self.object.pk}'
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'