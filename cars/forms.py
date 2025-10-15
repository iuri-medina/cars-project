from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory, inlineformset_factory
from cars.models import Brand, Car, CarImage

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 15000:
            self.add_error('price', 'Valor mínimo do veículo deve ser de R$ 15.000')
        return price
    
    def clean_factory_year(self):
        factory_year = self.cleaned_data.get('factory_year')
        if factory_year < 1975:
            self.add_error('factory_year', 'Não é possível cadastrar carros fabricados antes de 1975')
        return factory_year
    
class BaseCarImageFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        mains = 0
        has_images = False
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                # Check for images (new upload or existing)
                if form.cleaned_data.get("image") or (hasattr(form, 'instance') and form.instance.pk and form.instance.image):
                    has_images = True
                    if form.cleaned_data.get("is_main", False):
                        mains += 1
        
        # Require main image only if there are images
        if has_images:
            if mains == 0:
                raise ValidationError("Selecione uma imagem principal.")
            if mains > 1:
                raise ValidationError("Apenas uma imagem pode ser principal.")


CarImageFormSet = inlineformset_factory(
    Car, CarImage,
    fields=['image', 'is_main'],
    extra=9,
    can_delete=True,
    formset=BaseCarImageFormSet
)