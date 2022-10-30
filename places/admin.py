from django.contrib import admin
from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableStackedInline, SortableAdminBase

from .models import Place, Image


class PreviewMixin(object):
    def preview(self, obj):
        url = obj.image.url
        return mark_safe(f'<img src="{url}" style="max-height: 200px;">')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin, PreviewMixin):
    fields = (
        'place',
        'image',
        'position',
        'preview',
    )
    readonly_fields = ('preview',)


class ImageInline(SortableStackedInline, PreviewMixin):
    model = Image
    fields = ['image',  'preview', ]

    readonly_fields = ('preview',)

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj.images.count() else 2


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    fields = (
        'title',
        'description_short',
        'description_long',
        'lng',
        'lat',)
    inlines = (ImageInline,)
