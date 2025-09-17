from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from cars.models import Car
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

class NewCarView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'new_car.html'
    success_url = '/cars/'

class CarView(DetailView):
    model = Car
    template_name = 'car_detail.html'

class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_update.html'
    success_url = '/cars/'

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'