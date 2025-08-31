from modeltranslation.translator import translator, TranslationOptions
from .models import EmailTemplate, CommunicationTip


class EmailTemplateTranslationOptions(TranslationOptions):
    fields = ('subject_line', 'greeting', 'body', 'closing', 'signature', 'description', 'cultural_notes')


class CommunicationTipTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'example', 'kurdish_context', 'common_mistakes')


translator.register(EmailTemplate, EmailTemplateTranslationOptions)
translator.register(CommunicationTip, CommunicationTipTranslationOptions)
