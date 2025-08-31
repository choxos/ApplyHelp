from modeltranslation.translator import translator, TranslationOptions
from .models import ResourceCategory, Guide


class ResourceCategoryTranslationOptions(TranslationOptions):
    fields = ('description',)


class GuideTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'content', 'meta_description', 'keywords')


translator.register(ResourceCategory, ResourceCategoryTranslationOptions)
translator.register(Guide, GuideTranslationOptions)
