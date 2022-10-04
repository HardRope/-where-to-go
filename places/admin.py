from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Place, PlaceImage

@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    fields = (
        'title',
        'image',
        'preview',
    )

    readonly_fields = ("preview",)

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')

class PlaceImageInline(admin.TabularInline):
    model = PlaceImage

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    fields = (
        'title',
        'description_short',
        'description_long',
        'lng',
        'lat',)
    inlines = (PlaceImageInline,)

    # @admin.display(ordering='place__images', description='Images')
    # def get_images(self, obj):
    #     return obj.images.all()

