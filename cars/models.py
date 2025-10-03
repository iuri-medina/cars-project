from django.db import models
from PIL import Image
import os
from django.core.files.base import ContentFile
from io import BytesIO

class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50, unique=True)
    state_code = models.CharField(max_length=2, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.state_code})'

class Car(models.Model):
    model = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='car_brand')
    state = models.ForeignKey(State, on_delete=models.PROTECT, related_name='car_state')
    factory_year = models.IntegerField(blank=True, null=True)
    model_year = models.IntegerField(blank=True, null=True)
    mileage = models.IntegerField(default=0)
    plate = models.CharField(max_length=10, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.model
    
    def get_main_image(self):
        """Retorna a imagem principal do carro ou a primeira disponível"""
        main_image = self.car_images.filter(is_main=True).first()
        if main_image and main_image.image:
            return main_image.image.url
        
        first_image = self.car_images.first()
        if first_image and first_image.image:
            return first_image.image.url
            
        return '/media/cars/nopicture.png'
    
class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_images')
    image = models.ImageField(upload_to='cars/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Imagem de {self.car.model} - Principal: {'Sim' if self.is_main else 'Nao'}"
    
    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'file'):
            # Verificar se é um arquivo HEIC
            if self.image.name.lower().endswith(('.heic', '.heif')):
                # Converter HEIC para JPEG
                try:
                    # Abrir a imagem HEIC
                    img = Image.open(self.image.file)
                    
                    # Converter para RGB se necessário
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Redimensionar se for muito grande (opcional)
                    if img.width > 1920 or img.height > 1920:
                        img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
                    
                    # Salvar como JPEG
                    output = BytesIO()
                    img.save(output, format='JPEG', quality=85, optimize=True)
                    output.seek(0)
                    
                    # Substituir o arquivo original
                    filename = os.path.splitext(self.image.name)[0] + '.jpg'
                    self.image.save(
                        filename,
                        ContentFile(output.getvalue()),
                        save=False
                    )
                except Exception as e:
                    print(f"Erro ao converter HEIC: {e}")
                    # Se falhar, continua com o arquivo original
                    pass
        
        super().save(*args, **kwargs)

class CarInventory(models.Model):
    cars_count = models.IntegerField()
    cars_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.cars_count} - {self.cars_value}'
    
