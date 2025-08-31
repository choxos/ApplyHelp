from modeltranslation.translator import translator, TranslationOptions
from .models import Country, University, StudyProgram, Scholarship


class CountryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'kurdish_population', 'kurdish_organizations')


class UniversityTranslationOptions(TranslationOptions):
    fields = ('kurdish_students_info', 'kurdish_friendly_supervisors')


class StudyProgramTranslationOptions(TranslationOptions):
    fields = ('description', 'career_prospects', 'language_requirements', 'other_requirements')


class ScholarshipTranslationOptions(TranslationOptions):
    fields = ('description', 'eligibility_criteria', 'application_process', 'required_documents')


translator.register(Country, CountryTranslationOptions)
translator.register(University, UniversityTranslationOptions)
translator.register(StudyProgram, StudyProgramTranslationOptions)
translator.register(Scholarship, ScholarshipTranslationOptions)
