from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from cars.models import Car, CarInventory, Brand, State
from cars.forms import CarForm, CarImageFormSet


class CarsView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        cars = super().get_queryset().order_by('model')
        search_model = self.request.GET.get('search_model') 
        search_brand = self.request.GET.get('search_brand')
        search_state = self.request.GET.get('search_state')
        if search_model:
            cars = cars.filter(model__icontains=search_model)
        if search_brand:
            cars = cars.filter(brand__name=search_brand)
        if search_state:
            cars = cars.filter(state__name=search_state)
        return cars

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_inventory'] = CarInventory.objects.first()
        context['brands'] = Brand.objects.all()
        context['states'] = State.objects.all()
        return context

class CarView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ordenar imagens: principal primeiro, depois as outras
        car = self.object
        images = car.car_images.all().order_by('-is_main', 'id')
        context['ordered_images'] = images
        return context



@method_decorator(login_required, name='dispatch')
class NewCarView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'new_car.html'
    success_url = reverse_lazy('cars_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            print(f"POST data: {dict(self.request.POST)}")
            print(f"FILES data: {dict(self.request.FILES)}")
            context['formset'] = CarImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = CarImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(f"Form is valid: {form.is_valid()}")
        print(f"Formset is valid: {formset.is_valid()}")
        print(f"Formset errors: {formset.errors}")
        print(f"Formset non-form errors: {formset.non_form_errors()}")
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            images_saved = formset.save()
            print(f"Images saved: {len(images_saved)}")
            return redirect(self.get_success_url())
        else:
            # formset inválido -> renderiza novamente com os erros
            print("Formset is invalid, rendering with errors")
            return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_update.html'

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = CarImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = CarImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(formset)
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))



@method_decorator(login_required, name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'