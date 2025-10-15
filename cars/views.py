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
        min_price_raw = self.request.GET.get('min_price')
        max_price_raw = self.request.GET.get('max_price')
        min_year_raw = self.request.GET.get('min_year')
        max_year_raw = self.request.GET.get('max_year')
        if search_model:
            cars = cars.filter(model__icontains=search_model)
        if search_brand:
            cars = cars.filter(brand__name=search_brand)
        if search_state:
            cars = cars.filter(state__name=search_state)
        
        def parse_price(value):
            """Parse price input accepting commas and dots as separators"""
            if not value:
                return None
            v = str(value).strip()
            import re
            v = re.sub(r"[^0-9,\.\-]", '', v)
            # Handle multiple separators: assume dots are thousands, commas are decimals
            if v.count(',') > 0 and v.count('.') > 0:
                v = v.replace('.', '')
                v = v.replace(',', '.')
            else:
                v = v.replace(',', '.')
            try:
                return float(v)
            except Exception:
                return None

        min_price = parse_price(min_price_raw)
        max_price = parse_price(max_price_raw)
        if min_price is not None:
            cars = cars.filter(price__gte=min_price)
        if max_price is not None:
            cars = cars.filter(price__lte=max_price)

        def parse_year(value):
            """Parse year input as integer"""
            if not value:
                return None
            v = str(value).strip()
            import re
            v = re.sub(r'[^0-9\-]', '', v)
            try:
                return int(v)
            except Exception:
                return None

        min_year = parse_year(min_year_raw)
        max_year = parse_year(max_year_raw)
        if min_year is not None:
            cars = cars.filter(factory_year__gte=min_year)
        if max_year is not None:
            cars = cars.filter(factory_year__lte=max_year)
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
        # Order images: main first, then others
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