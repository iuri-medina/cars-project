from django.db.models.signals import post_save, post_delete, pre_save
from django.db.models import Sum
from django.dispatch import receiver
from cars.models import Car, CarInventory, CarImage

def car_inventory_update():
    if Car.objects.first():
        cars_count = Car.objects.all().count()
        cars_value = Car.objects.aggregate(
            total_value=Sum('price')
        )['total_value']
    else:
        cars_count = 0
        cars_value = 0.0

    CarInventory.objects.create(
        cars_count=cars_count,
        cars_value=cars_value
    )

@receiver(post_save, sender=Car)
def car_post_save(sender, instance, created, **kwargs):
    car_inventory_update()

@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    car_inventory_update()

    # Deletar todas as imagens relacionadas ao carro
    for image in instance.car_images.all():
        if image.image:
            image.image.delete(save=False)  # Remove o arquivo físico
        image.delete()  # Remove o registro do banco

@receiver(post_delete, sender=CarImage)
def car_image_post_delete(sender, instance, **kwargs):
    """
    Remove o arquivo de imagem do sistema de arquivos quando 
    uma CarImage é deletada
    """
    if instance.image:
        instance.image.delete(save=False)