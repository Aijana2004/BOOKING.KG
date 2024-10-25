from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class HotelPhotosInline(admin.TabularInline):
    model = HotelPhotos
    extra= 1


class RoomPhotosInline(admin.TabularInline):
    model = RoomPhotos
    extra= 1


@admin.register(Hotel)
class HotelAdmin(TranslationAdmin):
    inlines = [HotelPhotosInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Room)
admin.site.register(Booking)
