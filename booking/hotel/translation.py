from .models import Hotel
from modeltranslation.translator import TranslationOptions,register


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('name', 'description')