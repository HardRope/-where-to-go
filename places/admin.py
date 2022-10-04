from django.contrib import admin
from .models import Place, PlaceImage
# Register your models here.

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass

@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    pass