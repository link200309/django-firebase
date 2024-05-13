from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Log, Tarea

@receiver(post_save, sender=Tarea)
@receiver(post_delete, sender=Tarea)
def registrar_cambio(sender, instance, created, **kwargs):
    modelo_afectado = ContentType.objects.get_for_model(sender)
    tipo_cambio = "creado" if created else "modificado" if kwargs.get('update_fields') else "eliminado"
    
    Log.objects.create(
        modelo_afectado=modelo_afectado,
        tipo_cambio=tipo_cambio,
    )
    
