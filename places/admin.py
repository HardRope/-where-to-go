from django.contrib import admin
from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableStackedInline, SortableAdminBase

from .models import Place, Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = (
        'place',
        'image',
        'position',
        'preview',
    )
    readonly_fields = ("preview",)

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')

class ImageInline(SortableStackedInline):
    model = Image
    fields = ['image',  'preview', ]

    readonly_fields = ("preview",)

    def preview(self, model):
        return mark_safe(f'<img src="{model.image.url}" style="max-height: 200px;">')

    def get_extra(self, request, obj=model.place):
        extra = 2
        if obj:
            extra = 0
            return extra
        return extra

@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    fields = (
        'title',
        'description_short',
        'description_long',
        'lng',
        'lat',)
    inlines = (ImageInline,)
